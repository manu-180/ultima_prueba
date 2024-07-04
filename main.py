from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Montar la carpeta 'public' para servir archivos estáticos
app.mount("/", StaticFiles(directory="public", html=True), name="public")

@app.get("/api/hello")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
