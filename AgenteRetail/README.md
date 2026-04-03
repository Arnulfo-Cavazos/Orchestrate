# API de Inventario de Zapatos

API REST desarrollada con FastAPI para gestionar el inventario de zapatos de Grupo Nasan e integrarse con watsonx Orchestrate.

## 📋 Características

- ✅ **Búsqueda de zapatos** por marca, tipo, color, talla, precio y género
- ✅ **Recomendaciones inteligentes** basadas en uso y preferencias
- ✅ **Inventario en CSV** fácil de actualizar
- ✅ **Especificación OpenAPI 3.0** para integración con watsonx Orchestrate
- ✅ **Listo para desplegar en Render** con configuración incluida
- ✅ **CORS habilitado** para peticiones desde cualquier origen

## 🚀 Despliegue Rápido en Render

### Paso 1: Subir a GitHub

```bash
# Inicializar repositorio Git
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit: Grupo Nasan API"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/grupo-nasan-api.git
git branch -M main
git push -u origin main
```

### Paso 2: Desplegar en Render

1. Ve a [Render.com](https://render.com) e inicia sesión
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente el archivo `render.yaml`
5. Click en **"Create Web Service"**
6. ¡Espera 2-3 minutos y tu API estará lista! 🎉

### Paso 3: Obtener tu URL

Una vez desplegado, Render te dará una URL como:
```
https://grupo-nasan-api-xxxx.onrender.com
```

**⚠️ IMPORTANTE:** Actualiza la URL en `openapi_spec.yaml`:
```yaml
servers:
  - url: https://tu-app-real.onrender.com  # ← Reemplaza con tu URL de Render
```

## 🔧 Desarrollo Local

### Requisitos

- Python 3.11+
- pip

### Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
python main.py
```

La API estará disponible en: `http://localhost:8000`

### Documentación Interactiva

Una vez ejecutando, visita:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 Endpoints de la API

### 1. Buscar Zapatos

**POST** `/buscar_zapatos`

Busca zapatos según criterios específicos.

**Parámetros de consulta:**
- `marca` (opcional): Nike, Adidas, Puma, etc.
- `tipo` (opcional): Deportivo, Casual, Running, etc.
- `color` (opcional): Negro, Blanco, Azul, etc.
- `talla` (opcional): Número entre 22 y 30
- `precio_max` (opcional): Precio máximo en MXN
- `genero` (opcional): Hombre, Mujer, Unisex
- `limite` (opcional): Número de resultados (default: 10)

**Ejemplo de uso:**
```bash
curl -X POST "http://localhost:8000/buscar_zapatos?marca=Nike&tipo=Running&precio_max=3000"
```

**Respuesta:**
```json
{
  "total_resultados": 3,
  "zapatos": [
    {
      "id": 2,
      "marca": "Nike",
      "modelo": "Revolution 6",
      "tipo": "Running",
      "color": "Negro",
      "talla_min": 22,
      "talla_max": 30,
      "precio": 1599.00,
      "stock": 55,
      "genero": "Unisex",
      "descripcion": "Tenis para correr económicos y cómodos",
      "imagen_url": "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2"
    }
  ],
  "mensaje": "Se encontraron 3 zapatos que coinciden con: marca 'Nike', tipo 'Running', precio máximo $3000."
}
```

### 2. Recomendar Zapatos

**POST** `/recomendar_zapatos`

Genera recomendaciones personalizadas según el uso previsto.

**Parámetros de consulta:**
- `uso` (requerido): correr, casual, deporte, caminar, trabajo, skate, senderismo
- `presupuesto` (opcional): Presupuesto máximo en MXN
- `genero` (opcional): Hombre, Mujer, Unisex
- `limite` (opcional): Número de recomendaciones (default: 5)

**Ejemplo de uso:**
```bash
curl -X POST "http://localhost:8000/recomendar_zapatos?uso=correr&presupuesto=2500"
```

**Respuesta:**
```json
{
  "recomendaciones": [
    {
      "id": 11,
      "marca": "Nike",
      "modelo": "Revolution 6",
      "tipo": "Running",
      "precio": 1599.00,
      ...
    }
  ],
  "razon": "Estos zapatos son ideales para correr. Todos están dentro de tu presupuesto de $2500. Ordenados por popularidad y mejor precio.",
  "total": 5
}
```

### 3. Health Check

**GET** `/health`

Verifica el estado de la API.

```bash
curl http://localhost:8000/health
```

## 🔗 Integración con watsonx Orchestrate

### Paso 1: Actualizar la especificación OpenAPI

Edita `openapi_spec.yaml` y reemplaza la URL del servidor:

```yaml
servers:
  - url: https://TU-URL-DE-RENDER.onrender.com
```

### Paso 2: Importar la tool en Orchestrate

```bash
# Usando el CLI de Orchestrate
orchestrate tools import -k openapi -f openapi_spec.yaml
```

### Paso 3: Usar la tool en tu agente

El agente de watsonx Orchestrate ahora puede:

1. **Buscar productos específicos** cuando el cliente dice:
   - "Busco tenis Nike para correr"
   - "Quiero zapatos negros casuales de menos de $2000"
   - "Necesito tenis talla 26"

2. **Dar recomendaciones** cuando el cliente dice:
   - "¿Qué zapatos me recomiendas para correr?"
   - "Necesito zapatos para el trabajo"
   - "Quiero algo cómodo para caminar"

## 📊 Inventario

El inventario se encuentra en `inventario_zapatos.csv` con 30 productos de ejemplo.

### Estructura del CSV:

```csv
id,marca,modelo,tipo,color,talla_min,talla_max,precio,stock,genero,descripcion,imagen_url
1,Nike,Air Max 270,Deportivo,Negro,22,30,2499.00,45,Unisex,Zapatillas deportivas...,https://...
```

### Actualizar el inventario:

1. Edita `inventario_zapatos.csv`
2. Haz commit y push a GitHub
3. Render redesplegará automáticamente

## 🛠️ Estructura del Proyecto

```
grupo-nasan-api/
├── main.py                 # Aplicación FastAPI principal
├── inventario_zapatos.csv  # Base de datos de productos
├── openapi_spec.yaml       # Especificación OpenAPI para Orchestrate
├── requirements.txt        # Dependencias de Python
├── render.yaml            # Configuración de despliegue en Render
├── .gitignore             # Archivos ignorados por Git
└── README.md              # Este archivo
```

## 🔒 Seguridad

- ✅ CORS habilitado para permitir peticiones desde watsonx Orchestrate
- ✅ Validación de parámetros con Pydantic
- ✅ Manejo de errores robusto
- ✅ Sin credenciales hardcodeadas

## 📝 Notas Importantes

1. **Render Free Tier**: El servicio gratuito de Render se "duerme" después de 15 minutos de inactividad. La primera petición después de esto puede tardar 30-60 segundos.

2. **Actualizar inventario**: Cualquier cambio en `inventario_zapatos.csv` requiere un nuevo despliegue en Render (automático con push a GitHub).

3. **Límites de la API**: 
   - Búsqueda: máximo 50 resultados
   - Recomendaciones: máximo 10 resultados

## 🐛 Troubleshooting

### Error: "No se pudo cargar el inventario"
- Verifica que `inventario_zapatos.csv` existe en el repositorio
- Revisa los logs en Render Dashboard

### Error: "CORS policy"
- La API ya tiene CORS habilitado para todos los orígenes
- Verifica que estás usando la URL correcta de Render

### La API no responde
- Verifica el estado en Render Dashboard
- La primera petición después de inactividad puede tardar

## 📞 Soporte

Para problemas o preguntas:
1. Revisa los logs en Render Dashboard
2. Verifica la documentación en `/docs`
3. Prueba los endpoints localmente primero

## 📄 Licencia

Este proyecto es para uso interno de Grupo Nasan.

---

**Desarrollado para Grupo Nasan** 🏃‍♂️👟
