# Activar entorno virtual de Python
Write-Host "Activando entorno virtual"
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Actualizar pip
Write-Host "Actualizando pip"
python -m pip install --upgrade pip

# Instalar requerimientos
Write-Host "Instalando requirements"
pip install -r "requirements.txt"

# Inicializar reflex
Write-Host "Inicializando reflex"
reflex init

# Exportar solo el frontend de reflex
Write-Host "Exportando reflex frontend"
try {
    $exportOutput = reflex export --frontend-only 2>&1
    Write-Host "Salida de reflex export:"
    Write-Host $exportOutput
} catch {
    Write-Host "Error durante la exportación de reflex:"
    Write-Host $_
    exit 1
}

# Listar archivos en el directorio actual para depuración después de reflex export
Write-Host "Listando archivos en el"
