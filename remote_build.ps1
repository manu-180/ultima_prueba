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
reflex export --frontend-only

# Listar archivos en el directorio actual para depuración antes de verificar el archivo
Write-Host "Listando archivos en el directorio actual después de reflex export"
Get-ChildItem

# Verificar si frontend.zip existe
if (Test-Path -Path "frontend.zip") {
    Write-Host "frontend.zip encontrado, extrayendo archivos"
    # Crear el directorio public si no existe
    if (!(Test-Path -Path "public")) {
        New-Item -ItemType Directory -Path "public"
    }
    # Extraer el contenido de frontend.zip a public
    Expand-Archive -Path "frontend.zip" -DestinationPath "public" -Force
    # Eliminar el archivo frontend.zip
    Write-Host "Removiendo frontend.zip"
    Remove-Item -Path "frontend.zip" -Force
} else {
    Write-Host "Error: frontend.zip no encontrado, abortando"
    exit 1
}

# Añadir cambios a git
Write-Host "Adding changes to git"
git add .

# Hacer commit de los cambios
Write-Host "Committing changes"
git commit -m "Adjust workflow for Windows environment"

# Hacer push de los cambios
Write-Host "Pushing changes"
git push
