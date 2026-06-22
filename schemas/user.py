from pydantic import BaseModel, Field
from typing import List, Optional

# 1. Esquema Base: Lo que es común a todos
class UserBase(BaseModel):
    id: int =Field(...,ge=0,examples=[10])
    nombre: str =Field(...,max_length=70,min_length=3, example="Jennifer Andrea")
    email: str =Field(...,max_length=70,min_length=3, example="jennifer@example.com")
    
# 2. Esquema de Entrada: Lo que recibimos para crear un nuevo producto
class UserCreate(UserBase):
    pass

# 3. Esquema de Actualización: Lo que podemos modificar
class UserUpdate(BaseModel):
    id: Optional[int] =Field(...,ge=0,examples=[10])
    nombre: Optional[str] =Field(None,max_length=70,min_length=3, example="Jennifer Andrea")
    email: Optional[str] =Field(None,max_length=70,min_length=3, example="jennifer@example.com")

# 4. Esquema de Salida: Lo que ve el cliente
class UserOut(UserBase):
    id:int
    
    #Para base de datos
    class Config:
        from_attributes= True

class UserDeleteResponse(BaseModel):
    message: str

class UserItemResponse(BaseModel):
    success: bool
    message: str    
    data: UserOut

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    success: bool
    message: str    
    data: List[UserOut] 