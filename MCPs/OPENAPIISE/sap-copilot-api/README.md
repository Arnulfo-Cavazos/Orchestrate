# SAP Copilot API

API REST para consultar datos de SAP simulados (materiales, inventario, órdenes de producción) usando bases de datos CSV. Diseñado para ser consumido por agentes conversacionales de IA.

## 🎯 Características

- **Consulta de Materiales**: Buscar y filtrar materiales del catálogo
- **Inventario en Tiempo Real**: Consultar stock disponible por almacén
- **Órdenes de Producción**: Ver estado y progreso de órdenes
- **Análisis de Cobertura**: Calcular días de cobertura de inventario basado en demanda

## 📋 Requisitos

- Python 3.8+
- pip

## 🚀 Instalación

1. **Clonar o navegar al directorio del proyecto**
```bash
cd sap-copilot-api
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
```

3. **Activar entorno virtual**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 🏃 Ejecución

### Modo Desarrollo
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Modo Producción
```bash
python app/main.py
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación API

Una vez iniciado el servidor, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔌 Endpoints Principales

### 1. Consultar Materiales
```
GET /api/materials
```

**Parámetros:**
- `material_id` (opcional): ID del material
- `material_name` (opcional): Nombre del material (búsqueda parcial)

**Ejemplo:**
```bash
curl "http://localhost:8000/api/materials?material_id=MAT001"
```

### 2. Consultar Stock de Inventario
```
GET /api/inventory/stock
```

**Parámetros:**
- `material_id` (opcional): ID del material
- `warehouse` (opcional): Código del almacén (ej: "001")
- `min_quantity` (opcional): Cantidad mínima disponible

**Ejemplo:**
```bash
curl "http://localhost:8000/api/inventory/stock?material_id=MAT005&warehouse=001"
```

**Pregunta en lenguaje natural:**
> "¿Cuánto stock tengo del material MAT005 en el almacén 001?"

### 3. Consultar Órdenes de Producción
```
GET /api/production/orders
```

**Parámetros:**
- `status` (opcional): Estado (IN_PROGRESS, COMPLETED, PLANNED)
- `warehouse` (opcional): Almacén
- `due_within_days` (opcional): Órdenes que vencen en X días
- `priority` (opcional): Prioridad (HIGH, MEDIUM, LOW)

**Ejemplo:**
```bash
curl "http://localhost:8000/api/production/orders?due_within_days=7&status=IN_PROGRESS"
```

**Pregunta en lenguaje natural:**
> "¿Qué órdenes de producción vencen esta semana?"

### 4. Análisis de Cobertura de Inventario
```
GET /api/inventory/coverage
```

**Parámetros:**
- `material_id` (opcional): ID del material
- `warehouse` (opcional): Almacén
- `days` (opcional, default=30): Días de cobertura a analizar

**Ejemplo:**
```bash
curl "http://localhost:8000/api/inventory/coverage?days=30"
```

**Pregunta en lenguaje natural:**
> "¿Cuál es mi cobertura de inventario para los próximos 30 días?"

## 📊 Estructura de Datos

### Archivos CSV

- **materials.csv**: Catálogo de materiales
- **inventory.csv**: Stock actual por almacén
- **production_orders.csv**: Órdenes de producción
- **demand_forecast.csv**: Pronóstico de demanda

## 🌐 Integración con Agentes de IA

### Ejemplo de Integración con Orchestrate

1. **Exponer la API localmente**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. **Usar ngrok o similar para exponer públicamente (desarrollo)**
```bash
ngrok http 8000
```

3. **Configurar el agente con la URL de OpenAPI**
```
https://tu-url.ngrok.io/openapi.json
```

### Ejemplo de Prompts para el Agente

El agente puede responder preguntas como:

- "¿Cuánto stock tengo del material MAT005 en el almacén 001?"
- "¿Qué órdenes de producción vencen esta semana?"
- "¿Cuál es mi cobertura de inventario para los próximos 30 días?"
- "Muéstrame todos los materiales con stock bajo"
- "¿Qué órdenes están en progreso con prioridad alta?"

## 🔧 Personalización

### Agregar Más Datos

Edita los archivos CSV en la carpeta `data/`:
- `materials.csv`
- `inventory.csv`
- `production_orders.csv`
- `demand_forecast.csv`

### Agregar Nuevos Endpoints

Edita `app/main.py` y agrega nuevas funciones con el decorador `@app.get()` o `@app.post()`.

## 📝 Notas

- Los datos son simulados y se cargan desde archivos CSV
- La API está configurada con CORS abierto para desarrollo
- Para producción, configura CORS apropiadamente y usa HTTPS

## 🤝 Soporte

Para preguntas o problemas, contacta al equipo de desarrollo.

## 📄 Licencia

Este proyecto es para uso interno.