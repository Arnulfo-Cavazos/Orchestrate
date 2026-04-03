from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
import os

app = FastAPI(
    title="Grupo Nasan - API de Inventario de Zapatos",
    description="API para consultar inventario y obtener recomendaciones de zapatos para watsonx Orchestrate",
    version="1.0.0",
    servers=[
        {
            "url": "https://tu-app.onrender.com",
            "description": "Servidor de producción en Render"
        },
        {
            "url": "http://localhost:8000",
            "description": "Servidor de desarrollo local"
        }
    ]
)

# Configurar CORS para permitir peticiones desde watsonx Orchestrate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class Zapato(BaseModel):
    id: int
    marca: str
    modelo: str
    tipo: str
    color: str
    talla_min: float
    talla_max: float
    precio: float
    stock: int
    genero: str
    descripcion: str
    imagen_url: str

class BusquedaResponse(BaseModel):
    total_resultados: int = Field(description="Número total de zapatos encontrados")
    zapatos: List[Zapato] = Field(description="Lista de zapatos que coinciden con la búsqueda")
    mensaje: str = Field(description="Mensaje descriptivo sobre los resultados")

class RecomendacionResponse(BaseModel):
    recomendaciones: List[Zapato] = Field(description="Lista de zapatos recomendados")
    razon: str = Field(description="Explicación de por qué se recomiendan estos zapatos")
    total: int = Field(description="Número total de recomendaciones")

# Cargar inventario desde CSV
def cargar_inventario():
    """Carga el inventario de zapatos desde el archivo CSV"""
    try:
        csv_path = "inventario_zapatos.csv"
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"No se encontró el archivo {csv_path}")
        
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print(f"Error al cargar inventario: {e}")
        return pd.DataFrame()

@app.get("/", tags=["Health"])
async def root():
    """Endpoint de verificación de salud de la API"""
    return {
        "status": "online",
        "servicio": "Grupo Nasan - API de Zapatos",
        "version": "1.0.0",
        "endpoints": {
            "buscar": "/buscar_zapatos",
            "recomendar": "/recomendar_zapatos",
            "docs": "/docs"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Verifica el estado de la API y la disponibilidad del inventario"""
    df = cargar_inventario()
    return {
        "status": "healthy",
        "inventario_cargado": len(df) > 0,
        "total_productos": len(df)
    }

@app.post(
    "/buscar_zapatos",
    response_model=BusquedaResponse,
    tags=["Búsqueda"],
    summary="Buscar zapatos en el inventario",
    description="Busca zapatos según criterios como marca, tipo, color, talla, precio y género. El agente de watsonx Orchestrate usa este endpoint para encontrar productos específicos."
)
async def buscar_zapatos(
    marca: Optional[str] = Query(None, description="Marca del zapato (Nike, Adidas, Puma, etc.)"),
    tipo: Optional[str] = Query(None, description="Tipo de zapato (Deportivo, Casual, Running, etc.)"),
    color: Optional[str] = Query(None, description="Color del zapato (Negro, Blanco, Azul, etc.)"),
    talla: Optional[float] = Query(None, description="Talla del zapato (22-30)"),
    precio_max: Optional[float] = Query(None, description="Precio máximo en pesos mexicanos"),
    genero: Optional[str] = Query(None, description="Género (Hombre, Mujer, Unisex)"),
    limite: int = Query(10, description="Número máximo de resultados a retornar", ge=1, le=50)
):
    """
    Busca zapatos en el inventario según los criterios especificados.
    
    Este endpoint permite al agente de watsonx Orchestrate buscar productos
    específicos basándose en las preferencias del cliente.
    """
    try:
        df = cargar_inventario()
        
        if df.empty:
            raise HTTPException(status_code=500, detail="No se pudo cargar el inventario")
        
        # Aplicar filtros
        resultado = df.copy()
        filtros_aplicados = []
        
        if marca:
            resultado = resultado[resultado['marca'].str.contains(marca, case=False, na=False)]
            filtros_aplicados.append(f"marca '{marca}'")
        
        if tipo:
            resultado = resultado[resultado['tipo'].str.contains(tipo, case=False, na=False)]
            filtros_aplicados.append(f"tipo '{tipo}'")
        
        if color:
            resultado = resultado[resultado['color'].str.contains(color, case=False, na=False)]
            filtros_aplicados.append(f"color '{color}'")
        
        if talla:
            resultado = resultado[(resultado['talla_min'] <= talla) & (resultado['talla_max'] >= talla)]
            filtros_aplicados.append(f"talla {talla}")
        
        if precio_max:
            resultado = resultado[resultado['precio'] <= precio_max]
            filtros_aplicados.append(f"precio máximo ${precio_max}")
        
        if genero:
            resultado = resultado[
                (resultado['genero'].str.contains(genero, case=False, na=False)) |
                (resultado['genero'].str.contains('Unisex', case=False, na=False))
            ]
            filtros_aplicados.append(f"género '{genero}'")
        
        # Limitar resultados
        resultado = resultado.head(limite)
        
        # Construir mensaje descriptivo
        if len(resultado) == 0:
            mensaje = f"No se encontraron zapatos con los criterios: {', '.join(filtros_aplicados) if filtros_aplicados else 'ninguno'}. Intenta con otros filtros."
        elif len(filtros_aplicados) == 0:
            mensaje = f"Se encontraron {len(resultado)} zapatos en el inventario completo."
        else:
            mensaje = f"Se encontraron {len(resultado)} zapatos que coinciden con: {', '.join(filtros_aplicados)}."
        
        # Convertir a lista de diccionarios
        zapatos_list = resultado.to_dict('records')
        
        return BusquedaResponse(
            total_resultados=len(zapatos_list),
            zapatos=zapatos_list,
            mensaje=mensaje
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar zapatos: {str(e)}")

@app.post(
    "/recomendar_zapatos",
    response_model=RecomendacionResponse,
    tags=["Recomendaciones"],
    summary="Obtener recomendaciones de zapatos",
    description="Proporciona recomendaciones personalizadas de zapatos según el uso previsto, presupuesto y preferencias del cliente. El agente usa este endpoint para sugerir productos."
)
async def recomendar_zapatos(
    uso: str = Query(..., description="Uso previsto: 'correr', 'casual', 'deporte', 'caminar', 'trabajo', 'skate', 'senderismo'"),
    presupuesto: Optional[float] = Query(None, description="Presupuesto máximo en pesos mexicanos"),
    genero: Optional[str] = Query(None, description="Género preferido (Hombre, Mujer, Unisex)"),
    limite: int = Query(5, description="Número de recomendaciones", ge=1, le=10)
):
    """
    Genera recomendaciones personalizadas de zapatos basadas en el uso y preferencias.
    
    Este endpoint permite al agente de watsonx Orchestrate proporcionar sugerencias
    inteligentes a los clientes según sus necesidades específicas.
    """
    try:
        df = cargar_inventario()
        
        if df.empty:
            raise HTTPException(status_code=500, detail="No se pudo cargar el inventario")
        
        # Mapear uso a tipos de zapatos
        mapeo_uso = {
            'correr': ['Running', 'Deportivo'],
            'casual': ['Casual'],
            'deporte': ['Deportivo', 'Training'],
            'caminar': ['Confort', 'Casual'],
            'trabajo': ['Casual', 'Confort'],
            'skate': ['Skate', 'Casual'],
            'senderismo': ['Outdoor', 'Deportivo']
        }
        
        uso_lower = uso.lower()
        tipos_recomendados = []
        
        # Buscar coincidencias en el mapeo
        for key, tipos in mapeo_uso.items():
            if key in uso_lower:
                tipos_recomendados.extend(tipos)
                break
        
        # Si no hay coincidencia exacta, usar todos los tipos
        if not tipos_recomendados:
            tipos_recomendados = df['tipo'].unique().tolist()
        
        # Filtrar por tipo
        resultado = df[df['tipo'].isin(tipos_recomendados)]
        
        # Filtrar por presupuesto
        if presupuesto:
            resultado = resultado[resultado['precio'] <= presupuesto]
        
        # Filtrar por género
        if genero:
            resultado = resultado[
                (resultado['genero'].str.contains(genero, case=False, na=False)) |
                (resultado['genero'].str.contains('Unisex', case=False, na=False))
            ]
        
        # Ordenar por popularidad (stock) y precio
        resultado = resultado.sort_values(['stock', 'precio'], ascending=[False, True])
        
        # Limitar resultados
        resultado = resultado.head(limite)
        
        # Construir razón de recomendación
        if len(resultado) == 0:
            razon = f"No se encontraron zapatos disponibles para '{uso}' con el presupuesto especificado. Intenta aumentar el presupuesto o cambiar los criterios."
        else:
            razon = f"Estos zapatos son ideales para {uso}. "
            if presupuesto:
                razon += f"Todos están dentro de tu presupuesto de ${presupuesto}. "
            razon += f"Ordenados por popularidad y mejor precio."
        
        # Convertir a lista de diccionarios
        recomendaciones_list = resultado.to_dict('records')
        
        return RecomendacionResponse(
            recomendaciones=recomendaciones_list,
            razon=razon,
            total=len(recomendaciones_list)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar recomendaciones: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# Made with Bob
