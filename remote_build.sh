cd ultima_prueba
C:\Users\Manuel\Desktop\Folder\x\entorno_con_3.11\Scripts\python.exe -m pip install --upgrade pip 
pip install -r "requirements.txt"
reflex init
reflex export --frontend-only
Remove-Item -Recurse -Force public
mkdir public
Expand-Archive -Path frontend.zip -DestinationPath public
Remove-Item -Force frontend.zip
git add .
git commit -m "Adjust workflow for Windows environment"
git push