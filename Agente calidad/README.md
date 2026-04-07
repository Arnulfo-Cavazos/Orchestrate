# Quality Control API - Sistema de Control de Calidad de Proveedores

Microservicio FastAPI especializado en control de calidad de proveedores para taller de manufactura. Permite registrar lotes de producción, monitorear proveedores en riesgo y enviar alertas automáticas por correo electrónico.

## 🚀 Características

- **Registro de Lotes**: Registra lotes de producción con cálculo automático de porcentaje de rechazo
- **Monitoreo de Proveedores**: Identifica proveedores en riesgo basado en lotes fallidos
- **Sistema de Alertas**: Envío de alertas por correo electrónico para proveedores en riesgo
- **Ranking de Proveedores**: Visualiza el desempeño de todos los proveedores
- **Archivos CSV**: Almacenamiento en archivos CSV con datos de muestra incluidos
- **API RESTful**: Endpoints JSON estructurados para integración con orquestadores

## 📋 Requisitos

- Python 3.11+
- Cuenta de Gmail con App Password habilitado

## 🔧 Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/quality-control-api.git
cd quality-control-api
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:

```env
GMAIL_USER=tu-email@gmail.com
GMAIL_APP_PASSWORD=tu-app-password-de-16-caracteres
ALERT_TO=destinatario@example.com
```

### 5. Generar Gmail App Password

Para enviar correos electrónicos, necesitas generar un **App Password** de Gmail:

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. En el menú lateral, selecciona **Seguridad**
3. En "Cómo inicias sesión en Google", activa la **Verificación en dos pasos** (si no está activada)
4. Una vez activada la verificación en dos pasos, regresa a **Seguridad**
5. Busca **Contraseñas de aplicaciones** (App Passwords)
6. Haz clic en **Contraseñas de aplicaciones**
7. En "Seleccionar app", elige **Correo**
8. En "Seleccionar dispositivo", elige **Otro (nombre personalizado)**
9. Escribe un nombre como "Quality Control API"
10. Haz clic en **Generar**
11. Copia la contraseña de 16 caracteres (sin espacios)
12. Pégala en tu archivo `.env` como `GMAIL_APP_PASSWORD`

**Nota**: La contraseña de aplicación es diferente a tu contraseña de Gmail normal. Nunca uses tu contraseña de Gmail directamente.

### 6. Ejecutar la aplicación

```bash
uvicorn main:app --reload
```

La API estará disponible en: http://localhost:8000

Documentación interactiva: http://localhost:8000/docs

### 7. Datos de muestra incluidos

La aplicación ya incluye archivos CSV con datos de muestra:
- **lotes.csv**: 10 lotes de 3 proveedores diferentes
- **alertas_log.csv**: Archivo vacío listo para registrar alertas

Proveedores incluidos:
- **Aceros del Norte**: Estado RIESGO (3 lotes fallidos)
- **Plásticos MX**: Estado NORMAL (0 lotes fallidos)
- **Herrajes Monterrey**: Estado RIESGO (2 lotes fallidos)

Si deseas reiniciar los datos, usa:
```bash
curl -X POST http://localhost:8000/seed
```

## 🌐 Despliegue en Render

### Paso 1: Preparar el repositorio en GitHub

1. Crea un nuevo repositorio en GitHub
2. Sube tu código:

```bash
git init
git add .
git commit -m "Initial commit: Quality Control API"
git branch -M main
git remote add origin https://github.com/tu-usuario/quality-control-api.git
git push -u origin main
```

### Paso 2: Crear servicio en Render

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Haz clic en **New +** → **Web Service**
3. Conecta tu repositorio de GitHub
4. Selecciona el repositorio `quality-control-api`
5. Render detectará automáticamente el archivo `render.yaml`

### Paso 3: Configurar variables de entorno

En la configuración del servicio en Render, agrega las siguientes variables de entorno:

- `GMAIL_USER`: tu-email@gmail.com
- `GMAIL_APP_PASSWORD`: tu-app-password-de-16-caracteres
- `ALERT_TO`: destinatario@example.com

**Importante**: Estas variables están marcadas como `sync: false` en `render.yaml`, por lo que debes configurarlas manualmente en el dashboard de Render.

### Paso 4: Desplegar

1. Haz clic en **Create Web Service**
2. Render comenzará a construir y desplegar tu aplicación
3. Una vez completado, recibirás una URL como: `https://quality-control-api.onrender.com`

### Paso 5: Verificar el despliegue

```bash
curl https://quality-control-api.onrender.com/health
```

### Paso 6: Inicializar datos de prueba

```bash
curl -X POST https://quality-control-api.onrender.com/seed
```

## 📚 Endpoints de la API

### GET /health
Verifica el estado del servicio.

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2026-04-07T16:00:00.000000",
  "database": "connected"
}
```

### GET /tool/proveedor/{nombre}
Obtiene información detallada de un proveedor.

**Ejemplo:**
```bash
curl http://localhost:8000/tool/proveedor/Aceros%20del%20Norte
```

**Respuesta:**
```json
{
  "proveedor": "Aceros del Norte",
  "estado": "RIESGO",
  "lotes_fallidos_30d": 3,
  "rechazo_promedio": 7.85,
  "total_lotes_30d": 4,
  "lotes_recientes": [...]
}
```

### GET /tool/ranking
Obtiene el ranking de todos los proveedores ordenados por desempeño.

**Ejemplo:**
```bash
curl http://localhost:8000/tool/ranking
```

**Respuesta:**
```json
[
  {
    "proveedor": "Aceros del Norte",
    "estado": "RIESGO",
    "lotes_fallidos_30d": 3,
    "rechazo_promedio": 7.85,
    "total_lotes_30d": 4
  },
  ...
]
```

### GET /tool/alertas-pendientes
Lista proveedores que requieren atención (estado RIESGO).

**Ejemplo:**
```bash
curl http://localhost:8000/tool/alertas-pendientes
```

**Respuesta:**
```json
[
  {
    "proveedor": "Aceros del Norte",
    "lotes_fallidos": 3,
    "rechazo_promedio": 7.85,
    "estado": "RIESGO"
  }
]
```

### POST /tool/registrar-lote
Registra un nuevo lote de producción.

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/tool/registrar-lote \
  -H "Content-Type: application/json" \
  -d '{
    "fecha": "2026-04-07",
    "proveedor": "Aceros del Norte",
    "material": "Acero inoxidable 304",
    "numero_lote": "AN-2026-005",
    "total_piezas": 1000,
    "piezas_rechazadas": 45,
    "turno": "Matutino",
    "operador": "Juan Pérez"
  }'
```

**Respuesta:**
```json
{
  "id": 11,
  "fecha": "2026-04-07",
  "proveedor": "Aceros del Norte",
  "material": "Acero inoxidable 304",
  "numero_lote": "AN-2026-005",
  "total_piezas": 1000,
  "piezas_rechazadas": 45,
  "porcentaje_rechazo": 4.5,
  "turno": "Matutino",
  "operador": "Juan Pérez",
  "creado_en": "2026-04-07T16:00:00.000000"
}
```

### POST /tool/enviar-alerta/{nombre}
Envía una alerta por correo electrónico para un proveedor en riesgo.

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/tool/enviar-alerta/Aceros%20del%20Norte
```

**Respuesta:**
```json
{
  "success": true,
  "proveedor": "Aceros del Norte",
  "mensaje": "Alerta enviada exitosamente para el proveedor Aceros del Norte",
  "correo_enviado_a": "destinatario@example.com",
  "fecha_envio": "2026-04-07T16:00:00.000000"
}
```

### POST /seed
Inicializa la base de datos con datos de prueba.

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/seed
```

## 🔍 Lógica de Riesgo

Un proveedor está en estado **RIESGO** si cumple:
- Tiene **2 o más lotes** con porcentaje de rechazo **mayor a 5%**
- En los **últimos 30 días**

De lo contrario, está en estado **NORMAL**.

## 📊 Estructura de los Archivos CSV

### lotes.csv
Contiene todos los lotes de producción registrados.

**Columnas:**
- `id`: Identificador único del lote
- `fecha`: Fecha del lote (YYYY-MM-DD)
- `proveedor`: Nombre del proveedor
- `material`: Tipo de material
- `numero_lote`: Número de lote del proveedor
- `total_piezas`: Total de piezas en el lote
- `piezas_rechazadas`: Piezas rechazadas por calidad
- `porcentaje_rechazo`: Porcentaje calculado automáticamente
- `turno`: Turno de producción (Matutino/Vespertino/Nocturno)
- `operador`: Nombre del operador
- `creado_en`: Timestamp de creación del registro

**Ejemplo:**
```csv
id,fecha,proveedor,material,numero_lote,total_piezas,piezas_rechazadas,porcentaje_rechazo,turno,operador,creado_en
1,2026-04-02,Aceros del Norte,Acero inoxidable 304,AN-2026-001,1000,85,8.5,Matutino,Juan Pérez,2026-04-07T11:30:00.000000
```

### alertas_log.csv
Registra todas las alertas enviadas por correo electrónico.

**Columnas:**
- `id`: Identificador único de la alerta
- `fecha`: Fecha de la alerta (YYYY-MM-DD)
- `proveedor`: Nombre del proveedor alertado
- `lotes_fallidos`: Número de lotes fallidos detectados
- `rechazo_prom`: Porcentaje promedio de rechazo
- `correo_enviado`: 1 si se envió, 0 si no
- `enviado_en`: Timestamp del envío del correo

**Ejemplo:**
```csv
id,fecha,proveedor,lotes_fallidos,rechazo_prom,correo_enviado,enviado_en
1,2026-04-07,Aceros del Norte,3,7.13,1,2026-04-07T12:00:00.000000
```

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **Python 3.11**: Lenguaje de programación
- **CSV**: Archivos CSV para almacenamiento de datos
- **Pydantic**: Validación de datos
- **smtplib**: Envío de correos electrónicos
- **Uvicorn**: Servidor ASGI

## 📝 Notas Importantes

- Los archivos CSV (`lotes.csv` y `alertas_log.csv`) ya incluyen datos de muestra
- Los archivos CSV se crean automáticamente si no existen
- No se requiere autenticación para los endpoints
- Los correos solo se envían manualmente mediante el endpoint `/tool/enviar-alerta/{nombre}`
- No hay schedulers automáticos; el orquestador debe llamar a los endpoints
- Las credenciales de Gmail deben configurarse en variables de entorno
- Los archivos CSV se suben al repositorio con datos de muestra

## 🤝 Integración con Orquestadores

Esta API está diseñada para ser consumida por orquestadores de agentes. Todos los endpoints retornan JSON estructurado con campos claros:

1. **Monitoreo**: Usa `/tool/alertas-pendientes` para obtener proveedores en riesgo
2. **Análisis**: Usa `/tool/proveedor/{nombre}` para obtener detalles de un proveedor
3. **Acción**: Usa `/tool/enviar-alerta/{nombre}` para enviar alertas
4. **Registro**: Usa `/tool/registrar-lote` para agregar nuevos lotes

## 📄 Licencia

MIT License

## 👤 Autor

Sistema de Control de Calidad - Taller de Manufactura