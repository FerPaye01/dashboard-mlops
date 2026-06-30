# Script wrapper to run the Streamlit dashboard with local HF_HOME caching
# This avoids breaking the digital signature of venv\Scripts\Activate.ps1

$VenvDir = Join-Path $PSScriptRoot "venv"
$env:HF_HOME = Join-Path $VenvDir ".hf_cache"

Write-Host "Iniciando Selector de Modelos de IA Generativa..." -ForegroundColor Cyan
Write-Host "Variable HF_HOME configurada en: $env:HF_HOME" -ForegroundColor Gray

# Ejecutar streamlit directamente usando el binario del entorno virtual
& "$VenvDir\Scripts\streamlit.exe" run "$PSScriptRoot\app.py"
