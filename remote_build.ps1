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

# Eliminar el directorio public si existe
Write-Host "Removiendo public directory"
Remove-Item -Recurse -Force public

# Crear un nuevo directorio public
Write-Host "Creando public directory"
New-Item -ItemType Directory -Path public

# Extraer el contenido de frontend.zip a public
Write-Host "Extrayendo frontend.zip to public"
Expand-Archive -Path frontend.zip -DestinationPath public

# Eliminar el archivo frontend.zip
Write-Host "Removiendo frontend.zip"
Remove-Item -Force frontend.zip

# Añadir cambios a git
Write-Host "Adding changes to git"
git add .

# Hacer commit de los cambios
Write-Host "Committing changes"
git commit -m "Adjust workflow for Windows environment"

# Hacer push de los cambios
Write-Host "Pushing changes"
git push
