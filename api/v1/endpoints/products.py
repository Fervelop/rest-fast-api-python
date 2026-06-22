   
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importamos la infraestructura
from core.database import get_db
from schemas.product import (
    ProductCreate,
    ProductDeleteResponse,
    ProductItemResponse,
    ProductListResponse,
    ProductUpdate,
)
from service.products import ProductService

router = APIRouter()

#Consulta general
@router.get("/", response_model=ProductListResponse)
async def obtener_productos(db: Session = Depends(get_db)):
    """
    Llama al servicio para obtener la lista completa de productos.
    """
    service = ProductService(db)
    productos = service.get_all()
    return {
        "success": True,
        "message": "Productos obtenidos correctamente",
        "data": productos,
    }
    
#Consulta específica
@router.get("/{id}", response_model=ProductItemResponse)
def obtener_producto(id:int, db: Session = Depends(get_db)):
    """
    Busca y retorna un producto específico según su ID.
    Si no existe un producto con ese ID, lanza una excepción HTTP 404.
    """
    service = ProductService(db)
    producto = service.get_by_id(id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {
        "success": True,
        "message": "Producto obtenido correctamente",
        "data": producto,
    }

#Agregar un producto
@router.post("/", response_model=ProductItemResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(new_product: ProductCreate,db: Session = Depends(get_db)):
    """
    Recibe los datos validados por Pydantic y los envía al servicio para persistencia.
    """
    service = ProductService(db)
    producto_creado = service.create(new_product)
    return {
        "success": True,
        "message": "Producto creado correctamente",
        "data": producto_creado,
    }
    
@router.put("/{id}", response_model=ProductItemResponse)
async def actualizar_producto(id:int, producto:ProductUpdate,db: Session = Depends(get_db)):
    """
    Realiza una actualización parcial. Solo se modifican los campos enviados.
    """
    service = ProductService(db)
    producto_actualizado = service.update(id, producto)
    if not producto_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo actualizar: Producto no encontrado"
        )
    return {
        "success": True,
        "message": "Producto actualizado correctamente",
        "data": producto_actualizado,
    }

@router.delete("/{producto_id}", response_model=ProductDeleteResponse)
async def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Solicita al servicio la eliminación. Si tiene éxito, retorna 204 (No Content).
    """
    service = ProductService(db)
    exito = service.delete(producto_id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo eliminar: Producto no encontrado"
        )
    return {
        "success": True,
        "message": "Producto eliminado correctamente",
        "data": {"deleted_id": producto_id},
    }