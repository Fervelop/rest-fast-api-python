# main.py
from fastapi import FastAPI

# Crear la instancia de la aplicacion
app = FastAPI (
    title= "Mi API fgutierrez",
    description= "REST FAST API - ADSO",
    version= "1.0.0",
)

# Definir un endpoint

@app.get("/")
async def root():
    """Endpoint raiz que retorna un saludo"""
    return {"message": "¡Hola, FastAPI!"}

# Definir un endpoint con parametros

@app.get("/saludar/{nombre}")
def saludar(nombre: str):
    """Endpoint que saluda a la persona cuyo nombre se proporciona en la ruta"""
    if (nombre=="admin"):
        return {"message": f"Bienvenido al panel Admin!"}
    elif (nombre=="fer"):
        return {"message": f"¡Hola!, {nombre} bienvenida a tu home"}
    else:
        return {"message": f"{nombre}, ¡No tienes acceso!"}
