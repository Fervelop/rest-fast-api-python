from pydantic import BaseModel, Field
from typing import List, Optional

# 1. Esquema Base: Lo que es común a todos
class ProductBase(BaseModel):
    nombre: str =Field(...,max_length=70,min_length=3, example="Jennifer Andrea")
    stock: int=Field(...,ge=0,examples=[10])
    precio:float=Field(...,ge=0,examples=[2030.5])
    categoria_id: int #Agregamos el campo de categoría para relacionar el producto con su categoría (FK)
    
# 2. Esquema de Entrada: Lo que recibimos para crear un nuevo producto
class ProductCreate(ProductBase):
    pass

# 3. Esquema de Actualización: Lo que podemos modificar
class ProductUpdate(BaseModel):
    nombre: Optional[str] =Field(None,max_length=70,min_length=3, example="Jennifer Andrea")
    stock: Optional[int]=Field(None,ge=0,examples=[10])
    precio:Optional[float]=Field(None,ge=0,examples=[2030.5])

# 4. Esquema de Salida: Lo que ve el cliente
class ProductOut(ProductBase):
    id:int
    
    #Para base de datos
    class Config:
        from_attributes= True

class ProductDeleteResponse(BaseModel):
    message: str

class ProductItemResponse(BaseModel):
    success: bool
    message: str    
    data: ProductOut

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    success: bool
    message: str    
    data: List[ProductOut] 