@echo off
:: Script wrapper to run the Streamlit dashboard in cmd with local HF_HOME caching

set "HF_HOME=%~dp0venv\.hf_cache"
echo Iniciando Selector de Modelos de IA Generativa...
echo Variable HF_HOME configurada en: %HF_HOME%

:: Ejecutar streamlit directamente usando el binario del entorno virtual
"%~dp0venv\Scripts\streamlit.exe" run "%~dp0app.py"
pause
