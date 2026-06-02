from pydantic import BaseModel, Field
from typing import List, Optional
from schemas.product import ProductOut

# 1. Esquema Base: Lo que es común a todos
class CategoryBase(BaseModel):
    id: int =Field(...,ge=0,examples=[10])
    nombre: str =Field(...,max_length=70,min_length=3, example="Papeleria")
    products: Optional[List["ProductOut"]] = None  # Relación con productos

# 2. Esquema de Entrada: Lo que recibimos para crear un nuevo producto
class CategoryCreate(CategoryBase):
    pass

# 3. Esquema de Actualización: Lo que podemos modificar
class CategoryUpdate(BaseModel):
    id: Optional[int] =Field(...,ge=0,examples=[10])
    nombre: Optional[str] =Field(None,max_length=70,min_length=3, example="Jennifer Andrea")
    products: Optional[List["ProductOut"]] = None  # Relación con productos

# 4. Esquema de Salida: Lo que ve el cliente
class CategoryOut(CategoryBase):
    id:int
    
    #Para base de datos
    class Config:
        from_attributes= True

class CategoryDeleteResponse(BaseModel):
    message: str

class CategoryItemResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CategoryListResponse(BaseModel):
    products: List[CategoryItemResponse]