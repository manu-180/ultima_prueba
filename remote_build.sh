# Cambiar directorio
echo "Changing directory to ultima_prueba"
cd C:\Users\Manuel\Desktop\Folder\ultima_prueba

echo "activando variable de entorno " 
py -3 -m venv .venv
.venv\Scripts\activate
# Actualizar pip
echo "actualizando pip"
C:\Users\Manuel\Desktop\Folder\ultima_prueba\entorno_con_3.11\Scripts\python -m pip install --upgrade pip

# Instalar requerimientos
echo "instalando requirements"
pip install -r "requirements.txt"

# Inicializar reflex
echo "Inicializando reflex"
reflex init

# Exportar solo el frontend de reflex
echo "Exportando reflex frontend"
reflex export --frontend-only

# Eliminar el directorio public si existe
echo "Removiendo public directory"
Remove-Item -Recurse -Force public

# Crear un nuevo directorio public
echo "Creando public directory"
mkdir public

# Extraer el contenido de frontend.zip a public
echo "Extrayendo frontend.zip to public"
Expand-Archive -Path frontend.zip -DestinationPath public

# Eliminar el archivo frontend.zip
echo "Removiendo frontend.zip"
Remove-Item -Force frontend.zip

# Añadir cambios a git
echo "Adding changes to git"
git add .

# Hacer commit de los cambios
echo "Committing changes"
git commit -m "Adjust workflow for Windows environment"

# Hacer push de los cambios
echo "Pushing changes"
git push