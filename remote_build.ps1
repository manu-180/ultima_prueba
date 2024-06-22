#!/usr/bin/env pwsh

# Cambiar la política de ejecución para permitir scripts en PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Activar entorno virtual de Python
echo "Activando entorno virtual"
py -3 -m venv .venv
if ($?) { echo "Entorno virtual activado correctamente" } else { echo "Error al activar el entorno virtual"; exit 1 }

.\.venv\Scripts\Activate.ps1
if ($?) { echo "Entorno virtual activado" } else { echo "Error al activar el entorno virtual"; exit 1 }

# Actualizar pip
echo "Actualizando pip"
python -m pip install --upgrade pip
if ($?) { echo "pip actualizado correctamente" } else { echo "Error al actualizar pip"; exit 1 }

# Instalar requerimientos
echo "Instalando requirements"
pip install -r "requirements.txt"
if ($?) { echo "Requirements instalados correctamente" } else { echo "Error al instalar requirements"; exit 1 }

# Inicializar reflex
echo "Inicializando reflex"
reflex init
if ($?) { echo "Reflex inicializado correctamente" } else { echo "Error al inicializar reflex"; exit 1 }

# Exportar solo el frontend de reflex
echo "Exportando reflex frontend"
reflex export --frontend-only
if ($?) { echo "Frontend exportado correctamente" } else { echo "Error al exportar frontend"; exit 1 }

# Eliminar el directorio public si existe
echo "Removiendo public directory"
Remove-Item -Recurse -Force public
if ($?) { echo "Directorio public removido correctamente" } else { echo "Error al remover el directorio public"; exit 1 }

# Crear un nuevo directorio public
echo "Creando public directory"
mkdir public
if ($?) { echo "Directorio public creado correctamente" } else { echo "Error al crear el directorio public"; exit 1 }

# Extraer el contenido de frontend.zip a public
echo "Extrayendo frontend.zip to public"
Expand-Archive -Path frontend.zip -DestinationPath public
if ($?) { echo "frontend.zip extraído correctamente" } else { echo "Error al extraer frontend.zip"; exit 1 }

# Eliminar el archivo frontend.zip
echo "Removiendo frontend.zip"
Remove-Item -Force frontend.zip
if ($?) { echo "frontend.zip removido correctamente" } else { echo "Error al remover frontend.zip"; exit 1 }

# Añadir cambios a git
echo "Adding changes to git"
git add .
if ($?) { echo "Cambios añadidos a git correctamente" } else { echo "Error al añadir cambios a git"; exit 1 }

# Hacer commit de los cambios
echo "Committing changes"
git commit -m "Adjust workflow for Windows environment"
if ($?) { echo "Cambios commiteados correctamente" } else { echo "Error al commitear cambios"; exit 1 }

# Hacer push de los cambios
echo "Pushing changes"
git push
if ($?) { echo "Cambios pusheados correctamente" } else { echo "Error al pushear cambios"; exit 1 }
