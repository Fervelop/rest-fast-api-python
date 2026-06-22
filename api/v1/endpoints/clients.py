from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importamos la infraestructura
from core.database import get_db
from schemas.client import (
    ClientCreate,
    ClientDeleteResponse,
    ClientItemResponse,
    ClientListResponse,
    ClientUpdate,
)
from service.clients import ClientService

router = APIRouter()

#Consulta general
@router.get("/", response_model=ClientListResponse)
async def obtener_clientes(db: Session = Depends(get_db)):
    """
    Llama al servicio para obtener la lista completa de clientes.
    """
    service = ClientService(db)
    clientes = service.get_all()
    return {
        "success": True,
        "message": "Clientes obtenidos correctamente",
        "data": clientes,
    }
    
#Consulta específica
@router.get("/{id}", response_model=ClientItemResponse)
def obtener_cliente(id:int, db: Session = Depends(get_db)):
    """
    Busca y retorna un cliente específico según su ID.
    Si no existe un cliente con ese ID, lanza una excepción HTTP 404.
    """
    service = ClientService(db)
    cliente = service.get_by_id(id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {
        "success": True,
        "message": "Cliente obtenido correctamente",
        "data": cliente,
    }

#Agregar un cliente
@router.post("/", response_model=ClientItemResponse, status_code=status.HTTP_201_CREATED)
async def crear_cliente(new_client: ClientCreate,db: Session = Depends(get_db)):
    """
    Recibe los datos validados por Pydantic y los envía al servicio para persistencia.
    """
    service = ClientService(db)
    cliente_creado = service.create(new_client)
    return {
        "success": True,
        "message": "Cliente creado correctamente",
        "data": cliente_creado,
  
    }
    
@router.put("/{id}", response_model=ClientItemResponse)
async def actualizar_cliente(id:int, cliente:ClientUpdate,db: Session = Depends(get_db)):
    """
    Realiza una actualización parcial. Solo se modifican los campos enviados.
    """
    service = ClientService(db)
    cliente_actualizado = service.update(id, cliente)
    if not cliente_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo actualizar: Cliente no encontrado"
        )
    return {
        "success": True,
        "message": "Cliente actualizado correctamente",
        "data": cliente_actualizado,
    }

@router.delete("/{cliente_id}", response_model=ClientDeleteResponse)
async def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Solicita al servicio la eliminación. Si tiene éxito, retorna 204 (No Content).
    """
    service = ClientService(db)
    exito = service.delete(cliente_id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo eliminar: Cliente no encontrado"
        )
    return {
        "success": True,
        "message": "Cliente eliminado correctamente",
        "data": {"deleted_id": cliente_id},
    }