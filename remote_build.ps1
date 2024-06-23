# python -m venv entorno_con_3.11
#  .\entorno_con_3.11\Scripts\Activate
python -m pip install --upgrade pip
pip install -r requirements.txt
reflex init
reflex export --frontend-only
Remove-Item -Recurse -Force public
mkdir public
Expand-Archive -Path frontend.zip -DestinationPath public
Remove-Item -Force frontend.zip
# deactivate
git add .
git commit -m "cambios"
git push 