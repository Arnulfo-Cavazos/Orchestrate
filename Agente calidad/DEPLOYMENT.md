# 🚀 Guía Rápida de Despliegue

Esta guía te ayudará a desplegar rápidamente la aplicación en GitHub y Render.

## 📦 Paso 1: Subir a GitHub

```bash
# Inicializar repositorio Git
git init

# Agregar todos los archivos
git add .

# Hacer commit inicial
git commit -m "Initial commit: Quality Control API for manufacturing"

# Crear rama main
git branch -M main

# Agregar repositorio remoto (reemplaza con tu URL)
git remote add origin https://github.com/TU-USUARIO/quality-control-api.git

# Subir código
git push -u origin main
```

## 🌐 Paso 2: Desplegar en Render

### 2.1 Crear cuenta en Render
1. Ve a https://render.com/
2. Regístrate con tu cuenta de GitHub

### 2.2 Crear nuevo Web Service
1. En el dashboard, haz clic en **"New +"** → **"Web Service"**
2. Conecta tu repositorio de GitHub
3. Selecciona el repositorio `quality-control-api`
4. Render detectará automáticamente `render.yaml`

### 2.3 Configurar variables de entorno
En la sección **Environment**, agrega:

| Variable | Valor |
|----------|-------|
| `GMAIL_USER` | tu-email@gmail.com |
| `GMAIL_APP_PASSWORD` | tu-app-password-16-caracteres |
| `ALERT_TO` | destinatario@example.com |

### 2.4 Desplegar
1. Haz clic en **"Create Web Service"**
2. Espera a que termine el build (2-3 minutos)
3. Tu API estará disponible en: `https://tu-servicio.onrender.com`

## ✅ Paso 3: Verificar Despliegue

```bash
# Verificar salud del servicio
curl https://tu-servicio.onrender.com/health

# Ver proveedores en riesgo (ya incluye datos de muestra)
curl https://tu-servicio.onrender.com/tool/alertas-pendientes

# Ver ranking de proveedores
curl https://tu-servicio.onrender.com/tool/ranking

# Opcional: Reinicializar datos de prueba
curl -X POST https://tu-servicio.onrender.com/seed
```

**Nota:** La aplicación ya incluye archivos CSV con datos de muestra, por lo que no es necesario ejecutar `/seed` en el primer despliegue.

## 📧 Paso 4: Configurar Gmail App Password

### Generar App Password:
1. Ve a https://myaccount.google.com/security
2. Activa **"Verificación en dos pasos"** (si no está activada)
3. Busca **"Contraseñas de aplicaciones"**
4. Selecciona **"Correo"** y **"Otro dispositivo"**
5. Nombra: "Quality Control API"
6. Copia la contraseña de 16 caracteres
7. Pégala en Render como `GMAIL_APP_PASSWORD`

## 🔄 Actualizaciones Futuras

Cada vez que hagas cambios:

```bash
git add .
git commit -m "Descripción de cambios"
git push
```

Render desplegará automáticamente los cambios.

## 🐛 Solución de Problemas

### Error: "Application failed to start"
- Verifica que todas las variables de entorno estén configuradas
- Revisa los logs en Render Dashboard

### Error: "Failed to send email"
- Verifica que el App Password sea correcto
- Asegúrate de que la verificación en dos pasos esté activada
- Verifica que `GMAIL_USER` sea una cuenta de Gmail válida

### Archivos CSV no persisten en Render Free
- Render Free tier reinicia el servicio periódicamente
- Los cambios en los archivos CSV se perderán en cada reinicio
- Los archivos CSV originales con datos de muestra se restauran en cada deploy
- Usa `/seed` para reinicializar datos de prueba después de un reinicio
- Para persistencia de datos, considera upgrade a plan pagado o usar una base de datos externa

## 📊 Endpoints Disponibles

Una vez desplegado, puedes acceder a:

- **Documentación interactiva**: `https://tu-servicio.onrender.com/docs`
- **Health check**: `https://tu-servicio.onrender.com/health`
- **Ranking**: `https://tu-servicio.onrender.com/tool/ranking`
- **Alertas**: `https://tu-servicio.onrender.com/tool/alertas-pendientes`

## 🎯 Próximos Pasos

1. Integra la API con tu orquestador de agentes
2. Configura webhooks si es necesario
3. Monitorea el uso en Render Dashboard
4. Considera upgrade a plan pagado para persistencia de datos

## 💡 Consejos

- El plan Free de Render duerme después de 15 minutos de inactividad
- La primera petición después de dormir puede tardar 30-60 segundos
- Usa `/seed` para reinicializar datos después de reinicios
- Guarda el App Password de Gmail en un lugar seguro

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en Render Dashboard
2. Verifica la documentación en README.md
3. Prueba localmente primero con `uvicorn main:app --reload`