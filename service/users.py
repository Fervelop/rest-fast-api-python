from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status
from models.user import User

def _validar_usuario(self, usuario_id: int):

    """Método interno auxiliar para verificar si una usuario existe en la BD."""
    user_exists = self.db.query(User).filter(User.id == usuario_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operación inválida: La usuario con ID {usuario_id} no existe."
        )

def create(self, user_in: UserCreate):

    """Crea un nuevo usuario a partir del esquema de entrada y lo persiste."""
    # 1. VALIDACIÓN: Asegurar que la usuario asignada al nuevo usuario exista
    self._validar_usuario(user_in.usuario_id)

    # 2. PERSISTENCIA: Si la usuario existe, procedemos a guardar el usuario
    db_user = User(**user_in.model_dump())

    self.db.add(db_user) # Agrega el nuevo usuario a la sesion de trabajo
    self.db.commit()# Guarda los cambios en la base de datos
    self.db.refresh(db_user) # Refresca el objeto con los datos actualizados (como el ID generado)
    return db_user

def update(self, user_id: int, user_in: UserUpdate):

    """Actualiza una usuario existente con los campos enviados."""
    db_user = self.get_by_id(user_id)
    if db_user:
        # Solo actualiza los campos que fueron enviados (exclude_unset=True)
        update_data = user_in.model_dump(exclude_unset=True)

        # === VALIDACIÓN DE LA LLAVE FORÁNEA ===
        # Si el usuario intenta modificar la usuario del usuario, verificamos que sea válida
        if "usuario_id" in update_data:
            self._validar_usuario(update_data["usuarios_id"])
        # ======================================
        for key, value in update_data.items():
            setattr(db_user, key, value)
        self.db.commit() # Guarda los cambios en la base de datos
        self.db.refresh(db_user) # Refresca el objeto con los datos actualizados
    return db_user
class UserService:
    """Agrupa las operaciones CRUD de usuarios sobre una sesion de BD."""

    def __init__(self, db: Session):
        """Recibe una sesion de SQLAlchemy ya creada por la capa de conexion."""
        self.db = db

    def get_all(self):
        """Devuelve todas las usuarios almacenadas."""
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        """Busca una usuario por su identificador y devuelve el primero que coincida."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create(self, user_in: UserCreate):
        """Crea un nuevo usuario a partir del esquema de entrada y lo persiste."""
        db_user = User(**user_in.model_dump())
        self.db.add(db_user) # Agrega el nuevo usuario a la sesion de trabajo
        self.db.commit()# Guarda los cambios en la base de datos
        self.db.refresh(db_user) # Refresca el objeto con los datos actualizados (como el ID generado)
        return db_user

def update(self, user_id: int, user_in: UserUpdate):
    """Actualiza una usuario existente con los campos enviados."""
    db_user = self.get_by_id(user_id)
    if db_user:
        # Solo actualiza los campos que fueron enviados (exclude_unset=True)
        update_data = user_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        self.db.commit() # Guarda los cambios en la base de datos
        self.db.refresh(db_user) # Refresca el objeto con los datos actualizados
    return db_user

def delete(self, user_id: int):
    """Elimina una usuario por ID y devuelve True si la operacion se completo."""
    db_user = self.get_by_id(user_id)
    if db_user:
        self.db.delete(db_user)# Elimina la usuario de la sesion de trabajo
        self.db.commit()# Guarda los cambios en la base de datos
        return True
    return False