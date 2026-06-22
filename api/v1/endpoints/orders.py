from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importamos la infraestructura
from core.database import get_db
from schemas.order import (
    OrderCreate,
    OrderDeleteResponse,
    OrderItemResponse,
    OrderListResponse,
    OrderUpdate,
)
from service.orders import OrderService

router = APIRouter()

#Consulta general
@router.get("/", response_model=OrderListResponse)
async def obtener_ordenes(db: Session = Depends(get_db)):
    """
    Llama al servicio para obtener la lista completa de ordenes.
    """
    service = OrderService(db)
    ordenes = service.get_all()
    return {
        "success": True,
        "message": "Ordenes obtenidos correctamente",
        "data": ordenes,
    }
    
#Consulta específica
@router.get("/{id}", response_model=OrderItemResponse)
def obtener_orden(id:int, db: Session = Depends(get_db)):
    """
    Busca y retorna un orden específico según su ID.
    Si no existe un orden con ese ID, lanza una excepción HTTP 404.
    """
    service = OrderService(db)
    orden = service.get_by_id(id)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrado")
    return {
        "success": True,
        "message": "Orden obtenido correctamente",
        "data": orden,
    }

#Agregar un orden
@router.post("/", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
async def crear_orden(new_order: OrderCreate,db: Session = Depends(get_db)):
    """
    Recibe los datos validados por Pydantic y los envía al servicio para persistencia.
    """
    service = OrderService(db)
    orden_creado = service.create(new_order)
    return {
        "success": True,
        "message": "Orden creado correctamente",
        "data": orden_creado,
  
    }
    
@router.put("/{id}", response_model=OrderItemResponse)
async def actualizar_orden(id:int, orden:OrderUpdate,db: Session = Depends(get_db)):
    """
    Realiza una actualización parcial. Solo se modifican los campos enviados.
    """
    service = OrderService(db)
    orden_actualizado = service.update(id, orden)
    if not orden_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo actualizar: Orden no encontrado"
        )
    return {
        "success": True,
        "message": "Orden actualizado correctamente",
        "data": orden_actualizado,
    }

@router.delete("/{orden_id}", response_model=OrderDeleteResponse)
async def eliminar_orden(orden_id: int, db: Session = Depends(get_db)):
    """
    Solicita al servicio la eliminación. Si tiene éxito, retorna 204 (No Content).
    """
    service = OrderService(db)
    exito = service.delete(orden_id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo eliminar: Orden no encontrado"
        )
    return {
        "success": True,
        "message": "Orden eliminado correctamente",
        "data": {"deleted_id": orden_id},
    }