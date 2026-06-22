from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importamos la infraestructura
from core.database import get_db
from schemas.user import (
    UserCreate,
    UserDeleteResponse,
    UserItemResponse,
    UserListResponse,
    UserUpdate,
)
from service.users import UserService

router = APIRouter()

#Consulta general
@router.get("/", response_model=UserListResponse)
async def obtener_usuarios(db: Session = Depends(get_db)):
    """
    Llama al servicio para obtener la lista completa de usuarios.
    """
    service = UserService(db)
    usuarios = service.get_all()
    return {
        "success": True,
        "message": "Usuarios obtenidos correctamente",
        "data": usuarios,
    }
    
#Consulta específica
@router.get("/{id}", response_model=UserItemResponse)
def obtener_usuario(id:int, db: Session = Depends(get_db)):
    """
    Busca y retorna un usuario específico según su ID.
    Si no existe un usuario con ese ID, lanza una excepción HTTP 404.
    """
    service = UserService(db)
    usuario = service.get_by_id(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "success": True,
        "message": "Usuario obtenido correctamente",
        "data": usuario,
    }

#Agregar un usuario
@router.post("/", response_model=UserItemResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(new_user: UserCreate,db: Session = Depends(get_db)):
    """
    Recibe los datos validados por Pydantic y los envía al servicio para persistencia.
    """
    service = UserService(db)
    usuario_creado = service.create(new_user)
    return {
        "success": True,
        "message": "Usuario creado correctamente",
        "data": usuario_creado,
  
    }
    
@router.put("/{id}", response_model=UserItemResponse)
async def actualizar_usuario(id:int, usuario:UserUpdate,db: Session = Depends(get_db)):
    """
    Realiza una actualización parcial. Solo se modifican los campos enviados.
    """
    service = UserService(db)
    usuario_actualizado = service.update(id, usuario)
    if not usuario_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo actualizar: Usuario no encontrado"
        )
    return {
        "success": True,
        "message": "Usuario actualizado correctamente",
        "data": usuario_actualizado,
    }

@router.delete("/{usuario_id}", response_model=UserDeleteResponse)
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Solicita al servicio la eliminación. Si tiene éxito, retorna 204 (No Content).
    """
    service = UserService(db)
    exito = service.delete(usuario_id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo eliminar: Usuario no encontrado"
        )
    return {
        "success": True,
        "message": "Usuario eliminado correctamente",
        "data": {"deleted_id": usuario_id},
    }