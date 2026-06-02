'''
from typing import List

from fastapi import APIRouter, status, HTTPException
from schemas.product import ProductBase, ProductCreate, ProductUpdate, ProductOut

#Base de datos simulada
productos=[
{"id":1,"nombre":"Lapiz No.2","stock":5,"precio":2000},
{"id":2,"nombre":"Borrador Miga Pan","stock":10,"precio":1200}
]

router = APIRouter()

#Consulta general
@router.get("/",response_model=List[ProductOut])
async def obtener_productos():
    """Retorna la lista completa de productos almacenados en la base de datos simulada."""
    return productos

#Consulta específica
@router.get("/{id}")
def obtener_producto(id:int):
    """
    Busca y retorna un producto específico según su ID.
    Si no existe un producto con ese ID, lanza una excepción HTTP 404.
    """
    producto = next((p for p in productos if p["id"]==id), None)
    if not producto:
        raise HTTPException(status_code=404, message="Producto no encontrado")
    return producto

#Agregar un producto
@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def crear_producto(new_product: ProductCreate):
    """
    Crea un nuevo producto y lo agrega a la base de datos simulada.
    Genera automáticamente un ID único incrementando el mayor ID existente.
    Retorna el producto recién creado con su ID asignado.
    """
    #Lógica de incremento del id
    nuevo_id= max(p["id"] for p in productos) + 1 if productos else 1

    #Desempaquetar el new_product
    nuevo_producto= {**new_product.model_dump(), "id":nuevo_id}
    #Guardar
    productos.append(nuevo_producto)
    return nuevo_producto

@router.put("/{id}", response_model=ProductOut)
async def actualizar_producto(id:int, producto:ProductUpdate):
    """
    Actualiza los campos de un producto existente identificado por su ID.
    Solo modifica los campos enviados en el cuerpo de la solicitud (campos no enviados se
    conservan).
    Si no existe un producto con ese ID, lanza una excepción HTTP 404.
    """
    for i, p in enumerate(productos):
        if p["id"]==id:
            update_data= producto.model_dump(exclude_unset=True)
            productos[i].update(update_data)
            return productos[i]

    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(producto_id: int):
    """
    Elimina un producto de la base de datos simulada según su ID.
    Si el producto es encontrado, lo elimina y retorna una respuesta HTTP 204
    (sin contenido).
    Si no existe un producto con ese ID, lanza una excepción HTTP 404.
    """
    for i, p in enumerate(productos):
        if p["id"] == producto_id:
            productos.pop(i)
            return

    raise HTTPException(status_code=404, detail="Producto no encontrado")
    '''
    
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importamos la infraestructura
from core.database import get_db
from schemas.category import (
    CategoryCreate,
    CategoryDeleteResponse,
    CategoryItemResponse,
    CategoryListResponse,
    CategoryUpdate,
)
from service.categories import CategoryService

router = APIRouter()

#Consulta general
@router.get("/", response_model=CategoryListResponse)
async def obtener_categorias(db: Session = Depends(get_db)):
    """
    Llama al servicio para obtener la lista completa de categorias.
    """
    service = CategoryService(db)
    categorias = service.get_all()
    return {
        "success": True,
        "message": "Categorias obtenidos correctamente",
        "data": categorias,
    }
    
#Consulta específica
@router.get("/{id}", response_model=CategoryItemResponse)
def obtener_categoria(id:int, db: Session = Depends(get_db)):
    """
    Busca y retorna un producto específico según su ID.
    Si no existe un producto con ese ID, lanza una excepción HTTP 404.
    """
    service = CategoryService(db)
    categoria = service.get_by_id(id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrado")
    return {
        "success": True,
        "message": "Categoria obtenido correctamente",
        "data": categoria,
    }

#Agregar un producto
@router.post("/", response_model=CategoryItemResponse, status_code=status.HTTP_201_CREATED)
async def crear_categoria(new_category: CategoryCreate,db: Session = Depends(get_db)):
    """
    Recibe los datos validados por Pydantic y los envía al servicio para persistencia.
    """
    service = CategoryService(db)
    categoria_creado = service.create(new_category)
    return {
        "success": True,
        "message": "Categoria creado correctamente",
        "data": categoria_creado,
  
    }
    
@router.put("/{id}", response_model=CategoryItemResponse)
async def actualizar_categoria(id:int, categoria:CategoryUpdate,db: Session = Depends(get_db)):
    """
    Realiza una actualización parcial. Solo se modifican los campos enviados.
    """
    service = CategoryService(db)
    categoria_actualizado = service.update(id, categoria)
    if not categoria_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo actualizar: Categoria no encontrado"
        )
    return {
        "success": True,
        "message": "Categoria actualizado correctamente",
        "data": categoria_actualizado,
    }

@router.delete("/{categoria_id}", response_model=CategoryDeleteResponse)
async def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """
    Solicita al servicio la eliminación. Si tiene éxito, retorna 204 (No Content).
    """
    service = CategoryService(db)
    exito = service.delete(categoria_id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo eliminar: Categoria no encontrado"
        )
    return {
        "success": True,
        "message": "Categoria eliminado correctamente",
        "data": {"deleted_id": categoria_id},
    }