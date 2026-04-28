# 🚀 Instrucciones Rápidas - SAP Copilot API

## Inicio Rápido (Windows)

### Opción 1: Usar el script automático
```bash
cd sap-copilot-api
run.bat
```

### Opción 2: Paso a paso
```bash
# 1. Ir al directorio
cd sap-copilot-api

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📍 URLs Importantes

Una vez iniciado el servidor:

- **API Base**: http://localhost:8000
- **Documentación Interactiva**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🧪 Pruebas Rápidas

### Probar en el navegador:

1. **Ver todos los materiales**:
   ```
   http://localhost:8000/api/materials
   ```

2. **Stock de un material específico**:
   ```
   http://localhost:8000/api/inventory/stock?material_id=MAT005&warehouse=001
   ```

3. **Órdenes que vencen en 7 días**:
   ```
   http://localhost:8000/api/production/orders?due_within_days=7
   ```

4. **Cobertura de inventario**:
   ```
   http://localhost:8000/api/inventory/coverage?days=30
   ```

### Probar con curl (PowerShell):

```powershell
# Materiales
curl http://localhost:8000/api/materials

# Stock específico
curl "http://localhost:8000/api/inventory/stock?material_id=MAT005&warehouse=001"

# Órdenes de producción
curl "http://localhost:8000/api/production/orders?status=IN_PROGRESS"

# Cobertura
curl "http://localhost:8000/api/inventory/coverage?days=30"
```

## 🌐 Exponer para Orchestrate

### Usar ngrok (Recomendado):

```bash
# 1. Descargar ngrok de https://ngrok.com/download

# 2. En otra terminal, ejecutar:
ngrok http 8000

# 3. Copiar la URL pública (ej: https://abc123.ngrok.io)

# 4. Usar en Orchestrate:
https://abc123.ngrok.io/openapi.json
```

## 📊 Datos de Ejemplo

### Materiales disponibles:
- MAT001: Tornillo M8x20
- MAT005: Motor Eléctrico 1HP
- MAT008: Carcasa Aluminio
- MAT015: Panel Control HMI

### Almacenes:
- 001: Almacén Principal
- 002: Almacén Secundario

### Estados de órdenes:
- IN_PROGRESS: En progreso
- COMPLETED: Completada
- PLANNED: Planeada

## 🔍 Preguntas de Ejemplo para el Agente

Una vez integrado con Orchestrate, prueba estas preguntas:

1. "¿Cuánto stock tengo del material MAT005 en el almacén 001?"
2. "¿Qué órdenes de producción vencen esta semana?"
3. "¿Cuál es mi cobertura de inventario para los próximos 30 días?"
4. "Muéstrame todos los materiales con stock crítico"
5. "¿Qué órdenes están en progreso con prioridad alta?"
6. "Dame el estado de la orden PO001"

## ⚠️ Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Asegúrate de activar el entorno virtual
venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "Address already in use"
```bash
# El puerto 8000 está ocupado, usa otro puerto:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Error: "FileNotFoundError: data/materials.csv"
```bash
# Asegúrate de estar en el directorio correcto:
cd sap-copilot-api
```

## 📝 Notas

- Los datos son simulados y se cargan desde archivos CSV
- Puedes modificar los CSV en la carpeta `data/` para agregar más datos
- La API se recarga automáticamente cuando cambias el código (modo --reload)

## 📚 Documentación Completa

- Ver `README.md` para documentación detallada
- Ver `GUIA_INTEGRACION.md` para integración con Orchestrate