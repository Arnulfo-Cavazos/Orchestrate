from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import sqlite3
import os
from contextlib import contextmanager
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Quality Control API", version="1.0.0")

# Database configuration
DB_NAME = "quality_control.db"

# Pydantic models
class RegistrarLoteRequest(BaseModel):
    fecha: str  # Format: YYYY-MM-DD
    proveedor: str
    material: str
    numero_lote: str
    total_piezas: int
    piezas_rechazadas: int
    turno: str
    operador: str

class LoteResponse(BaseModel):
    id: int
    fecha: str
    proveedor: str
    material: str
    numero_lote: str
    total_piezas: int
    piezas_rechazadas: int
    porcentaje_rechazo: float
    turno: str
    operador: str
    creado_en: str

class ProveedorResponse(BaseModel):
    proveedor: str
    estado: str  # NORMAL, RIESGO
    lotes_fallidos_30d: int
    rechazo_promedio: float
    total_lotes_30d: int
    lotes_recientes: List[LoteResponse]

class RankingItem(BaseModel):
    proveedor: str
    estado: str
    lotes_fallidos_30d: int
    rechazo_promedio: float
    total_lotes_30d: int

class AlertaPendiente(BaseModel):
    proveedor: str
    lotes_fallidos: int
    rechazo_promedio: float
    estado: str

class EnviarAlertaResponse(BaseModel):
    success: bool
    proveedor: str
    mensaje: str
    correo_enviado_a: str
    fecha_envio: str

# Database context manager
@contextmanager
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Initialize database
def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create lotes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                proveedor TEXT NOT NULL,
                material TEXT NOT NULL,
                numero_lote TEXT NOT NULL,
                total_piezas INTEGER NOT NULL,
                piezas_rechazadas INTEGER NOT NULL,
                porcentaje_rechazo REAL NOT NULL,
                turno TEXT NOT NULL,
                operador TEXT NOT NULL,
                creado_en TEXT NOT NULL
            )
        """)
        
        # Create alertas_log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alertas_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                proveedor TEXT NOT NULL,
                lotes_fallidos INTEGER NOT NULL,
                rechazo_prom REAL NOT NULL,
                correo_enviado INTEGER NOT NULL DEFAULT 0,
                enviado_en TEXT
            )
        """)
        
        conn.commit()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Helper functions
def calcular_porcentaje_rechazo(total_piezas: int, piezas_rechazadas: int) -> float:
    if total_piezas == 0:
        return 0.0
    return round((piezas_rechazadas / total_piezas) * 100, 2)

def obtener_lotes_proveedor_30d(proveedor: str):
    fecha_limite = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM lotes 
            WHERE proveedor = ? AND fecha >= ?
            ORDER BY fecha DESC
        """, (proveedor, fecha_limite))
        
        return cursor.fetchall()

def calcular_estado_proveedor(proveedor: str) -> dict:
    lotes = obtener_lotes_proveedor_30d(proveedor)
    
    lotes_fallidos = [l for l in lotes if l['porcentaje_rechazo'] > 5.0]
    total_lotes = len(lotes)
    
    if total_lotes == 0:
        rechazo_promedio = 0.0
    else:
        rechazo_promedio = round(sum(l['porcentaje_rechazo'] for l in lotes) / total_lotes, 2)
    
    estado = "RIESGO" if len(lotes_fallidos) >= 2 else "NORMAL"
    
    return {
        "estado": estado,
        "lotes_fallidos_30d": len(lotes_fallidos),
        "rechazo_promedio": rechazo_promedio,
        "total_lotes_30d": total_lotes,
        "lotes": lotes
    }

def enviar_correo_alerta(proveedor: str, info_proveedor: dict):
    gmail_user = os.getenv("GMAIL_USER")
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
    alert_to = os.getenv("ALERT_TO")
    
    if not all([gmail_user, gmail_app_password, alert_to]):
        raise ValueError("Missing email configuration in environment variables")
    
    # Prepare email content
    subject = f"⚠️ ALERTA DE CALIDAD - Proveedor: {proveedor}"
    
    body = f"""
{'='*60}
ALERTA DE CONTROL DE CALIDAD
{'='*60}

PROVEEDOR: {proveedor}
ESTADO: {info_proveedor['estado']}
FECHA DE ALERTA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
RESUMEN DEL PROVEEDOR
{'='*60}

- Lotes fallidos (últimos 30 días): {info_proveedor['lotes_fallidos_30d']}
- Porcentaje de rechazo promedio: {info_proveedor['rechazo_promedio']}%
- Total de lotes evaluados: {info_proveedor['total_lotes_30d']}

{'='*60}
DETALLE DE LOTES FALLIDOS (Rechazo > 5%)
{'='*60}

"""
    
    lotes_fallidos = [l for l in info_proveedor['lotes'] if l['porcentaje_rechazo'] > 5.0]
    
    for idx, lote in enumerate(lotes_fallidos, 1):
        body += f"""
Lote #{idx}:
  - Fecha: {lote['fecha']}
  - Número de lote: {lote['numero_lote']}
  - Material: {lote['material']}
  - Total piezas: {lote['total_piezas']}
  - Piezas rechazadas: {lote['piezas_rechazadas']}
  - Porcentaje rechazo: {lote['porcentaje_rechazo']}%
  - Turno: {lote['turno']}
  - Operador: {lote['operador']}
"""
    
    body += f"""
{'='*60}
ACCIÓN SUGERIDA
{'='*60}

Se recomienda:
1. Contactar inmediatamente al proveedor {proveedor}
2. Solicitar plan de acción correctiva
3. Revisar especificaciones de calidad del material
4. Considerar auditoría al proceso del proveedor
5. Evaluar proveedores alternativos si la situación persiste

{'='*60}
Este es un mensaje automático del Sistema de Control de Calidad
{'='*60}
"""
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = alert_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_app_password)
        server.send_message(msg)

# Endpoints
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }

@app.get("/tool/proveedor/{nombre}", response_model=ProveedorResponse)
async def obtener_proveedor(nombre: str):
    info = calcular_estado_proveedor(nombre)
    
    if info['total_lotes_30d'] == 0:
        raise HTTPException(status_code=404, detail=f"No se encontraron lotes para el proveedor: {nombre}")
    
    lotes_response = [
        LoteResponse(
            id=l['id'],
            fecha=l['fecha'],
            proveedor=l['proveedor'],
            material=l['material'],
            numero_lote=l['numero_lote'],
            total_piezas=l['total_piezas'],
            piezas_rechazadas=l['piezas_rechazadas'],
            porcentaje_rechazo=l['porcentaje_rechazo'],
            turno=l['turno'],
            operador=l['operador'],
            creado_en=l['creado_en']
        )
        for l in info['lotes']
    ]
    
    return ProveedorResponse(
        proveedor=nombre,
        estado=info['estado'],
        lotes_fallidos_30d=info['lotes_fallidos_30d'],
        rechazo_promedio=info['rechazo_promedio'],
        total_lotes_30d=info['total_lotes_30d'],
        lotes_recientes=lotes_response
    )

@app.get("/tool/ranking", response_model=List[RankingItem])
async def obtener_ranking():
    fecha_limite = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT proveedor FROM lotes 
            WHERE fecha >= ?
        """, (fecha_limite,))
        
        proveedores = [row['proveedor'] for row in cursor.fetchall()]
    
    ranking = []
    for proveedor in proveedores:
        info = calcular_estado_proveedor(proveedor)
        ranking.append(RankingItem(
            proveedor=proveedor,
            estado=info['estado'],
            lotes_fallidos_30d=info['lotes_fallidos_30d'],
            rechazo_promedio=info['rechazo_promedio'],
            total_lotes_30d=info['total_lotes_30d']
        ))
    
    # Sort by lotes_fallidos_30d descending, then by rechazo_promedio descending
    ranking.sort(key=lambda x: (x.lotes_fallidos_30d, x.rechazo_promedio), reverse=True)
    
    return ranking

@app.get("/tool/alertas-pendientes", response_model=List[AlertaPendiente])
async def obtener_alertas_pendientes():
    fecha_limite = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT proveedor FROM lotes 
            WHERE fecha >= ?
        """, (fecha_limite,))
        
        proveedores = [row['proveedor'] for row in cursor.fetchall()]
    
    alertas = []
    for proveedor in proveedores:
        info = calcular_estado_proveedor(proveedor)
        
        if info['estado'] == 'RIESGO':
            alertas.append(AlertaPendiente(
                proveedor=proveedor,
                lotes_fallidos=info['lotes_fallidos_30d'],
                rechazo_promedio=info['rechazo_promedio'],
                estado=info['estado']
            ))
    
    return alertas

@app.post("/tool/registrar-lote", response_model=LoteResponse)
async def registrar_lote(lote: RegistrarLoteRequest):
    porcentaje_rechazo = calcular_porcentaje_rechazo(lote.total_piezas, lote.piezas_rechazadas)
    creado_en = datetime.now().isoformat()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO lotes (
                fecha, proveedor, material, numero_lote, 
                total_piezas, piezas_rechazadas, porcentaje_rechazo,
                turno, operador, creado_en
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lote.fecha, lote.proveedor, lote.material, lote.numero_lote,
            lote.total_piezas, lote.piezas_rechazadas, porcentaje_rechazo,
            lote.turno, lote.operador, creado_en
        ))
        
        lote_id = cursor.lastrowid
        conn.commit()
    
    return LoteResponse(
        id=lote_id,
        fecha=lote.fecha,
        proveedor=lote.proveedor,
        material=lote.material,
        numero_lote=lote.numero_lote,
        total_piezas=lote.total_piezas,
        piezas_rechazadas=lote.piezas_rechazadas,
        porcentaje_rechazo=porcentaje_rechazo,
        turno=lote.turno,
        operador=lote.operador,
        creado_en=creado_en
    )

@app.post("/tool/enviar-alerta/{nombre}", response_model=EnviarAlertaResponse)
async def enviar_alerta(nombre: str):
    info = calcular_estado_proveedor(nombre)
    
    if info['total_lotes_30d'] == 0:
        raise HTTPException(status_code=404, detail=f"No se encontraron lotes para el proveedor: {nombre}")
    
    if info['estado'] != 'RIESGO':
        raise HTTPException(
            status_code=400, 
            detail=f"El proveedor {nombre} no está en estado de RIESGO. Estado actual: {info['estado']}"
        )
    
    try:
        enviar_correo_alerta(nombre, info)
        
        # Log the alert
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        enviado_en = datetime.now().isoformat()
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO alertas_log (
                    fecha, proveedor, lotes_fallidos, rechazo_prom, 
                    correo_enviado, enviado_en
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                fecha_actual, nombre, info['lotes_fallidos_30d'], 
                info['rechazo_promedio'], 1, enviado_en
            ))
            conn.commit()
        
        alert_to = os.getenv("ALERT_TO")
        
        return EnviarAlertaResponse(
            success=True,
            proveedor=nombre,
            mensaje=f"Alerta enviada exitosamente para el proveedor {nombre}",
            correo_enviado_a=alert_to,
            fecha_envio=enviado_en
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar alerta: {str(e)}")

@app.post("/seed")
async def seed_database():
    # Clear existing data
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lotes")
        cursor.execute("DELETE FROM alertas_log")
        conn.commit()
    
    hoy = datetime.now()
    
    # Proveedor 1: Aceros del Norte - RIESGO (3 lotes fallidos)
    lotes_aceros = [
        {
            "fecha": (hoy - timedelta(days=5)).strftime("%Y-%m-%d"),
            "proveedor": "Aceros del Norte",
            "material": "Acero inoxidable 304",
            "numero_lote": "AN-2026-001",
            "total_piezas": 1000,
            "piezas_rechazadas": 85,
            "turno": "Matutino",
            "operador": "Juan Pérez"
        },
        {
            "fecha": (hoy - timedelta(days=12)).strftime("%Y-%m-%d"),
            "proveedor": "Aceros del Norte",
            "material": "Acero al carbón A36",
            "numero_lote": "AN-2026-002",
            "total_piezas": 800,
            "piezas_rechazadas": 72,
            "turno": "Vespertino",
            "operador": "María González"
        },
        {
            "fecha": (hoy - timedelta(days=18)).strftime("%Y-%m-%d"),
            "proveedor": "Aceros del Norte",
            "material": "Acero galvanizado",
            "numero_lote": "AN-2026-003",
            "total_piezas": 1200,
            "piezas_rechazadas": 96,
            "turno": "Nocturno",
            "operador": "Carlos Ramírez"
        },
        {
            "fecha": (hoy - timedelta(days=25)).strftime("%Y-%m-%d"),
            "proveedor": "Aceros del Norte",
            "material": "Acero inoxidable 316",
            "numero_lote": "AN-2026-004",
            "total_piezas": 500,
            "piezas_rechazadas": 15,
            "turno": "Matutino",
            "operador": "Juan Pérez"
        }
    ]
    
    # Proveedor 2: Plásticos MX - NORMAL (0 lotes fallidos)
    lotes_plasticos = [
        {
            "fecha": (hoy - timedelta(days=3)).strftime("%Y-%m-%d"),
            "proveedor": "Plásticos MX",
            "material": "Polipropileno",
            "numero_lote": "PMX-2026-001",
            "total_piezas": 2000,
            "piezas_rechazadas": 40,
            "turno": "Matutino",
            "operador": "Ana López"
        },
        {
            "fecha": (hoy - timedelta(days=10)).strftime("%Y-%m-%d"),
            "proveedor": "Plásticos MX",
            "material": "PVC",
            "numero_lote": "PMX-2026-002",
            "total_piezas": 1500,
            "piezas_rechazadas": 45,
            "turno": "Vespertino",
            "operador": "Roberto Sánchez"
        },
        {
            "fecha": (hoy - timedelta(days=20)).strftime("%Y-%m-%d"),
            "proveedor": "Plásticos MX",
            "material": "Polietileno",
            "numero_lote": "PMX-2026-003",
            "total_piezas": 1800,
            "piezas_rechazadas": 54,
            "turno": "Nocturno",
            "operador": "Laura Martínez"
        }
    ]
    
    # Proveedor 3: Herrajes Monterrey - EN EL LÍMITE (2 lotes fallidos)
    lotes_herrajes = [
        {
            "fecha": (hoy - timedelta(days=7)).strftime("%Y-%m-%d"),
            "proveedor": "Herrajes Monterrey",
            "material": "Tornillos M8",
            "numero_lote": "HM-2026-001",
            "total_piezas": 5000,
            "piezas_rechazadas": 280,
            "turno": "Matutino",
            "operador": "Pedro Hernández"
        },
        {
            "fecha": (hoy - timedelta(days=14)).strftime("%Y-%m-%d"),
            "proveedor": "Herrajes Monterrey",
            "material": "Tuercas M8",
            "numero_lote": "HM-2026-002",
            "total_piezas": 5000,
            "piezas_rechazadas": 300,
            "turno": "Vespertino",
            "operador": "Sofía Torres"
        },
        {
            "fecha": (hoy - timedelta(days=22)).strftime("%Y-%m-%d"),
            "proveedor": "Herrajes Monterrey",
            "material": "Arandelas",
            "numero_lote": "HM-2026-003",
            "total_piezas": 10000,
            "piezas_rechazadas": 400,
            "turno": "Nocturno",
            "operador": "Miguel Ángel Ruiz"
        }
    ]
    
    # Insert all lotes
    todos_lotes = lotes_aceros + lotes_plasticos + lotes_herrajes
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        for lote_data in todos_lotes:
            porcentaje = calcular_porcentaje_rechazo(
                lote_data['total_piezas'], 
                lote_data['piezas_rechazadas']
            )
            creado_en = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO lotes (
                    fecha, proveedor, material, numero_lote, 
                    total_piezas, piezas_rechazadas, porcentaje_rechazo,
                    turno, operador, creado_en
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lote_data['fecha'], lote_data['proveedor'], lote_data['material'], 
                lote_data['numero_lote'], lote_data['total_piezas'], 
                lote_data['piezas_rechazadas'], porcentaje,
                lote_data['turno'], lote_data['operador'], creado_en
            ))
        
        conn.commit()
    
    return {
        "success": True,
        "mensaje": "Base de datos inicializada con datos de prueba",
        "proveedores_creados": [
            {
                "nombre": "Aceros del Norte",
                "estado": "RIESGO",
                "lotes_totales": len(lotes_aceros),
                "lotes_fallidos": 3
            },
            {
                "nombre": "Plásticos MX",
                "estado": "NORMAL",
                "lotes_totales": len(lotes_plasticos),
                "lotes_fallidos": 0
            },
            {
                "nombre": "Herrajes Monterrey",
                "estado": "RIESGO",
                "lotes_totales": len(lotes_herrajes),
                "lotes_fallidos": 2
            }
        ]
    }

# Made with Bob
