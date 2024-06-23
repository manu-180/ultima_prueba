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

# Exportar solo el frontend de reflex y capturar la salida
Write-Host "Exportando reflex frontend"
$exportOutput = reflex export --frontend-only 2>&1
Write-Host $exportOutput

# Listar archivos en el directorio actual para depuración
Write-Host "Listando archivos en el directorio actual después de reflex export"
Get-ChildItem

# Listar archivos de manera recursiva para depuración
Write-Host "Listando archivos de manera recursiva después de reflex export"
Get-ChildItem -Recurse

# Verificar si cualquier archivo ZIP existe en el directorio actual
Write-Host "Verificando la existencia de cualquier archivo ZIP en el directorio actual"
$zipFile = Get-ChildItem -Recurse -Filter "*.zip" | Select-Object -First 1
if ($zipFile) {
    Write-Host "Archivo ZIP encontrado: $($zipFile.FullName)"
} else {
    Write-Host "Ningún archivo ZIP encontrado, abortando"
    exit 1
}

# Eliminar el directorio public si existe
Write-Host "Removiendo public directory"
Remove-Item -Recurse -Force public

# Crear un nuevo directorio public
Write-Host "Creando public directory"
New-Item -ItemType Directory -Path public

# Extraer el contenido del archivo ZIP encontrado a public
Write-Host "Extrayendo archivos del archivo ZIP encontrado"
Expand-Archive -Path $zipFile.FullName -DestinationPath public

# Eliminar el archivo ZIP
Write-Host "Removiendo el archivo ZIP"
Remove-Item -Force $zipFile.FullName

# Añadir cambios a git
Write-Host "Adding changes to git"
git add .

# Hacer commit de los cambios
Write-Host "Committing changes"
git commit -m "Adjust workflow for Windows environment"

# Hacer push de los cambios
Write-Host "Pushing changes"
git push
