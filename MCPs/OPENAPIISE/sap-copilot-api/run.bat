@echo off
echo ========================================
echo SAP Copilot API - Iniciando servidor
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo Creando entorno virtual...
    python -m venv venv
    echo.
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat
echo.

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
echo.

REM Iniciar servidor
echo Iniciando servidor en http://localhost:8000
echo Documentacion disponible en http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

@REM Made with Bob
