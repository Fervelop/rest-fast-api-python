from pydantic import BaseModel, Field
from typing import List, Optional
from schemas.client import ClientOut


# 1. Esquema Base: Lo que es común a todos
class OrderBase(BaseModel):
    id: int =Field(...,ge=0,examples=[10])
    client_id: int =Field(...,ge=0,examples=[10])


# 2. Esquema de Entrada: Lo que recibimos para crear un nuevo producto
class OrderCreate(OrderBase):
    pass

# 3. Esquema de Actualización: Lo que podemos modificar
class OrderUpdate(BaseModel):
    id: Optional[int] =Field(...,ge=0,examples=[10])
    client_id: Optional[int] =Field(None,ge=0,examples=[10])



# 4. Esquema de Salida: Lo que ve el cliente
class OrderOut(OrderBase):
    id:int
    
    #Para base de datos
    class Config:
        from_attributes= True

class OrderDeleteResponse(BaseModel):
    message: str

class OrderItemResponse(BaseModel):
    success: bool
    message: str    
    data: OrderOut

    class Config:
        from_attributes = True

class OrderListResponse(BaseModel):
    success: bool
    message: str    
    data: List[OrderOut] 