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

# Listar archivos en el directorio actual para depuración
Write-Host "Listando archivos en el directorio actual después de reflex export"
Get-ChildItem

# Eliminar el directorio public si existe
Write-Host "Removiendo public directory"
Remove-Item -Recurse -Force public

# Crear un nuevo directorio public
Write-Host "Creando public directory"
New-Item -ItemType Directory -Path public

# Verificar si frontend.zip existe
if (Test-Path -Path frontend.zip) {
    Write-Host "frontend.zip encontrado, extrayendo archivos"
    # Extraer el contenido de frontend.zip a public
    Expand-Archive -Path frontend.zip -DestinationPath public
    # Eliminar el archivo frontend.zip
    Write-Host "Removiendo frontend.zip"
    Remove-Item -Force frontend.zip
} else {
    Write-Host "frontend.zip no encontrado, abortando"
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
