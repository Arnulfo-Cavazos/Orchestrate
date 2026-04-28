# Guía de Integración con Agente Orchestrate

Esta guía explica cómo integrar la SAP Copilot API con tu agente conversacional en Orchestrate.

## 🎯 Objetivo

Permitir que tu agente responda preguntas en lenguaje natural sobre:
- Stock de materiales
- Órdenes de producción
- Cobertura de inventario

## 📋 Pasos de Integración

### 1. Iniciar la API Localmente

```bash
cd sap-copilot-api
run.bat
```

La API estará disponible en `http://localhost:8000`

### 2. Exponer la API Públicamente (Desarrollo)

Para que Orchestrate pueda acceder a tu API local, necesitas exponerla públicamente:

#### Opción A: Usar ngrok (Recomendado para desarrollo)

1. Descargar ngrok: https://ngrok.com/download
2. Ejecutar:
```bash
ngrok http 8000
```
3. Copiar la URL pública (ej: `https://abc123.ngrok.io`)

#### Opción B: Usar localtunnel

```bash
npm install -g localtunnel
lt --port 8000
```

### 3. Obtener el OpenAPI Schema

Accede a: `https://tu-url-publica/openapi.json`

Este archivo contiene toda la especificación de la API que necesita tu agente.

### 4. Configurar en Orchestrate

1. Ve a tu proyecto en Orchestrate
2. Navega a la sección de "Tools" o "Integraciones"
3. Agrega una nueva herramienta de tipo "OpenAPI"
4. Proporciona la URL del schema: `https://tu-url-publica/openapi.json`

### 5. Configurar el Prompt del Agente

Agrega instrucciones al prompt del agente:

```
Eres un asistente de planeación SAP. Tienes acceso a herramientas para consultar:

1. Materiales del catálogo
2. Inventario en tiempo real
3. Órdenes de producción
4. Análisis de cobertura de inventario

Cuando el usuario pregunte sobre stock, órdenes o inventario, usa las herramientas disponibles para obtener datos actualizados.

Ejemplos de preguntas que puedes responder:
- "¿Cuánto stock tengo del material MAT005 en el almacén 001?"
- "¿Qué órdenes de producción vencen esta semana?"
- "¿Cuál es mi cobertura de inventario para los próximos 30 días?"
- "Muéstrame materiales con stock crítico"
```

## 🔍 Ejemplos de Uso

### Ejemplo 1: Consultar Stock

**Usuario:** "¿Cuánto stock tengo del material MAT005 en el almacén 001?"

**El agente llamará:**
```
GET /api/inventory/stock?material_id=MAT005&warehouse=001
```

**Respuesta esperada:**
```json
[
  {
    "material_id": "MAT005",
    "material_name": "Motor Eléctrico 1HP",
    "warehouse": "001",
    "storage_location": "0003",
    "quantity": 85,
    "reserved_quantity": 15,
    "available_quantity": 70,
    "last_updated": "2026-04-26"
  }
]
```

**El agente responderá:**
> "Tienes 70 unidades disponibles del Motor Eléctrico 1HP (MAT005) en el almacén 001. El stock total es de 85 unidades, con 15 reservadas."

### Ejemplo 2: Órdenes que Vencen

**Usuario:** "¿Qué órdenes de producción vencen esta semana?"

**El agente llamará:**
```
GET /api/production/orders?due_within_days=7
```

**El agente responderá:**
> "Tienes 3 órdenes que vencen esta semana:
> 1. PO001 - Motor Eléctrico 1HP: 70% completado, vence el 28/04
> 2. PO006 - Válvula Solenoide 24V: 75% completado, vence el 29/04
> 3. PO003 - Placa Base Acero: 75% completado, vence el 30/04"

### Ejemplo 3: Cobertura de Inventario

**Usuario:** "¿Cuál es mi cobertura de inventario para los próximos 30 días?"

**El agente llamará:**
```
GET /api/inventory/coverage?days=30
```

**El agente responderá:**
> "Análisis de cobertura para 30 días:
> 
> ⚠️ CRÍTICO:
> - MAT015 (Panel Control HMI): 5.2 días de cobertura
> 
> ⚠️ BAJO:
> - MAT005 (Motor Eléctrico 1HP): 12.3 días de cobertura
> 
> ✅ ÓPTIMO:
> - MAT001 (Tornillo M8x20): 45.6 días de cobertura
> - MAT002 (Tuerca M8): 52.1 días de cobertura"

## 🛠️ Troubleshooting

### Error: "Cannot connect to API"

1. Verifica que la API esté corriendo: `http://localhost:8000`
2. Verifica que ngrok esté activo
3. Verifica que la URL en Orchestrate sea correcta

### Error: "Tool not found"

1. Verifica que el schema OpenAPI esté accesible
2. Refresca la configuración de herramientas en Orchestrate

### La API responde pero el agente no usa las herramientas

1. Verifica el prompt del agente
2. Asegúrate de que las herramientas estén habilitadas
3. Prueba con preguntas más específicas

## 🚀 Despliegue en Producción

Para producción, considera:

1. **Hosting**: Despliega la API en un servidor (AWS, Azure, GCP)
2. **HTTPS**: Usa certificados SSL
3. **Autenticación**: Agrega API keys o OAuth
4. **Rate Limiting**: Limita las peticiones por usuario
5. **Logging**: Implementa logs detallados
6. **Monitoreo**: Usa herramientas como Prometheus/Grafana

### Ejemplo con Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📞 Soporte

Para preguntas adicionales, contacta al equipo de desarrollo.