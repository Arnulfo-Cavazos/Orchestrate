# 🚀 Guía Rápida de Despliegue en Render

## Pasos para Desplegar en 5 Minutos

### 1️⃣ Subir a GitHub

```bash
# En la terminal, dentro de la carpeta del proyecto:

# Inicializar Git
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "API Grupo Nasan - Lista para desplegar"

# Crear repositorio en GitHub:
# - Ve a https://github.com/new
# - Nombre: grupo-nasan-zapatos-api
# - Descripción: API de inventario de zapatos para watsonx Orchestrate
# - Público o Privado (tu elección)
# - NO inicialices con README, .gitignore o licencia
# - Click en "Create repository"

# Conectar con GitHub (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/grupo-nasan-zapatos-api.git
git branch -M main
git push -u origin main
```

### 2️⃣ Desplegar en Render

1. **Ir a Render**: https://render.com
2. **Iniciar sesión** (o crear cuenta gratuita)
3. Click en **"New +"** (arriba derecha)
4. Seleccionar **"Web Service"**
5. Click en **"Connect a repository"**
6. **Autorizar GitHub** si es la primera vez
7. Buscar y seleccionar tu repositorio: **grupo-nasan-zapatos-api**
8. Render detectará automáticamente `render.yaml`
9. Click en **"Create Web Service"**
10. **¡Esperar 2-3 minutos!** ⏳

### 3️⃣ Obtener tu URL

Una vez que el despliegue termine (verás "Live" en verde):

1. Copia tu URL de Render, será algo como:
   ```
   https://grupo-nasan-zapatos-api-xxxx.onrender.com
   ```

2. **Probar la API**:
   ```bash
   # Reemplaza con tu URL real
   curl https://tu-url.onrender.com/health
   ```

### 4️⃣ Actualizar OpenAPI Spec

**MUY IMPORTANTE**: Actualiza el archivo `openapi_spec.yaml`:

```yaml
servers:
  - url: https://tu-url-real.onrender.com  # ← Cambia esto
```

Luego haz commit y push:
```bash
git add openapi_spec.yaml
git commit -m "Actualizar URL de producción"
git push
```

Render redesplegará automáticamente (1-2 minutos).

### 5️⃣ Importar en watsonx Orchestrate

```bash
# Usando el CLI de Orchestrate
orchestrate tools import -k openapi -f openapi_spec.yaml
```

O desde la UI de Orchestrate:
1. Tools → Import Tool
2. Seleccionar "OpenAPI"
3. Subir `openapi_spec.yaml`
4. Confirmar

## ✅ Verificación

### Probar la API directamente:

```bash
# Health check
curl https://tu-url.onrender.com/health

# Buscar Nike
curl -X POST "https://tu-url.onrender.com/buscar_zapatos?marca=Nike&limite=3"

# Recomendaciones para correr
curl -X POST "https://tu-url.onrender.com/recomendar_zapatos?uso=correr&limite=5"
```

### Ver documentación interactiva:

Abre en tu navegador:
```
https://tu-url.onrender.com/docs
```

## 🔄 Actualizar la API

Cada vez que hagas cambios:

```bash
git add .
git commit -m "Descripción de los cambios"
git push
```

Render redesplegará automáticamente en 1-2 minutos.

## 📊 Monitorear en Render

En el Dashboard de Render puedes ver:
- ✅ Estado del servicio (Live/Building/Failed)
- 📊 Logs en tiempo real
- 📈 Uso de recursos
- 🔄 Historial de despliegues

## ⚠️ Notas Importantes

1. **Free Tier de Render**:
   - El servicio se "duerme" después de 15 minutos sin uso
   - Primera petición después puede tardar 30-60 segundos
   - Esto es normal y no afecta la funcionalidad

2. **Actualizar Inventario**:
   - Edita `inventario_zapatos.csv`
   - Haz commit y push
   - Render redesplegará automáticamente

3. **Ver Logs**:
   - En Render Dashboard → Tu servicio → Logs
   - Útil para debugging

## 🐛 Problemas Comunes

### "Build failed"
- Revisa los logs en Render
- Verifica que `requirements.txt` está correcto
- Asegúrate que todos los archivos están en GitHub

### "Service unavailable"
- Espera 30-60 segundos (servicio despertando)
- Verifica en Render Dashboard que está "Live"

### "CORS error"
- Ya está configurado en el código
- Verifica que usas la URL correcta

## 📞 Ayuda

Si algo no funciona:
1. Revisa los logs en Render Dashboard
2. Prueba localmente primero: `python main.py`
3. Verifica que la URL en `openapi_spec.yaml` es correcta

---

**¡Listo! Tu API está en producción** 🎉