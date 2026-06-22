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