# Activar entorno virtual de Python
Write-Host "Activando entorno virtual"
python -m venv entorno_con_3.11
.\entorno_con_3.11\Scripts\Activate

# Actualizar pip
Write-Host "Actualizando pip"
python -m pip install --upgrade pip

# Instalar requerimientos
Write-Host "Instalando requirements"
pip install -r requirements.txt

# Inicializar reflex
Write-Host "Inicializando reflex"
reflex init

# Configurar variable de entorno API_URL
Write-Host "Configurando variable de entorno API_URL"
$env:API_URL = "https://api.baackend.com"

# Exportar solo el frontend de reflex y capturar la salida
Write-Host "Exportando reflex frontend"
$exportOutput = & reflex export --frontend-only 2>&1
Write-Host "Salida de reflex export:"
Write-Host $exportOutput

# Verificar si frontend.zip se ha creado en el directorio raíz del proyecto
Write-Host "Listando archivos en el directorio raíz después de reflex export"
Get-ChildItem -Path . -Filter "frontend.zip"

# Verificar si frontend.zip existe en cualquier parte del proyecto
Write-Host "Verificando la existencia de frontend.zip en cualquier parte del proyecto"
$zipFile = Get-ChildItem -Recurse -Filter "frontend.zip" | Select-Object -First 1
if ($zipFile) {
    Write-Host "frontend.zip encontrado en: $($zipFile.FullName)"
} else {
    Write-Host "frontend.zip no encontrado, abortando"
    exit 1
}

# Eliminar el directorio public si existe
Write-Host "Removiendo public directory"
Remove-Item -Recurse -Force public

# Crear un nuevo directorio public
Write-Host "Creando public directory"
New-Item -ItemType Directory -Path public

# Extraer el contenido de frontend.zip a public
Write-Host "Extrayendo archivos de frontend.zip a public"
Expand-Archive -Path $zipFile.FullName -DestinationPath public

# El
