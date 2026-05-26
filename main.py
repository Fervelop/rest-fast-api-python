# main.py
from unittest.mock import Base
from core.database import Base, engine
from fastapi import APIRouter, FastAPI
from api.v1.api import api_router 

# Crea las tablas declaradas en los modelos si aun no existen.
Base.metadata.create_all(bind=engine)

# Crear la instancia de la aplicacion
app = FastAPI (
    title= "Mi API fgutierrez",
    description= "REST FAST API - ADSO",
    version= "1.0.0",
)

api_router=APIRouter()

# Conexión de todas las rutas bajo el prefijo /api/v1
app.include_router(api_router, prefix="/api/v1")

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



