from pydantic import BaseModel, Field
from typing import List, Optional
from schemas.order import OrderOut


# 1. Esquema Base: Lo que es común a todos
class ClientBase(BaseModel):
    id: int =Field(...,ge=0,examples=[10])
    nombre: str =Field(...,max_length=70,min_length=3, example="Papeleria")
    email: str =Field(...,max_length=70,min_length=3, example="papeleria@example.com")


# 2. Esquema de Entrada: Lo que recibimos para crear un nuevo producto
class ClientCreate(ClientBase):
    pass

# 3. Esquema de Actualización: Lo que podemos modificar
class ClientUpdate(BaseModel):
    id: Optional[int] =Field(...,ge=0,examples=[10])
    nombre: Optional[str] =Field(None,max_length=70,min_length=3, example="Papeleria")
    email: Optional[str] =Field(None,max_length=70,min_length=3, example="papeleria@example.com")


# 4. Esquema de Salida: Lo que ve el cliente
class ClientOut(ClientBase):
    id:int
    
    #Para base de datos
    class Config:
        from_attributes= True

class ClientDeleteResponse(BaseModel):
    message: str

class ClientItemResponse(BaseModel):
    success: bool
    message: str    
    data: ClientOut

    class Config:
        from_attributes = True

class ClientListResponse(BaseModel):
    success: bool
    message: str    
    data: List[ClientOut] 