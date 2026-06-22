from sqlalchemy.orm import Session
from models.client import Client
from schemas.client import ClientCreate, ClientUpdate
from fastapi import HTTPException, status
from models.client import Client

def _validar_cliente(self, cliente_id: int):

    """Método interno auxiliar para verificar si un cliente existe en la BD."""
    client_exists = self.db.query(Client).filter(Client.id == cliente_id).first()
    if not client_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operación inválida: El cliente con ID {cliente_id} no existe."
        )

def create(self, client_in: ClientCreate):

    """Crea un nuevo cliente a partir del esquema de entrada y lo persiste."""
    # 1. VALIDACIÓN: Asegurar que la cliente asignada al nuevo cliente exista
    self._validar_cliente(client_in.cliente_id)

    # 2. PERSISTENCIA: Si la cliente existe, procedemos a guardar el cliente
    db_client = Client(**client_in.model_dump())

    self.db.add(db_client) # Agrega el nuevo cliente a la sesion de trabajo
    self.db.commit()# Guarda los cambios en la base de datos
    self.db.refresh(db_client) # Refresca el objeto con los datos actualizados (como el ID generado)
    return db_client

def update(self, client_id: int, client_in: ClientUpdate):

    """Actualiza un cliente existente con los campos enviados."""
    db_client = self.get_by_id(client_id)
    if db_client:
        # Solo actualiza los campos que fueron enviados (exclude_unset=True)
        update_data = client_in.model_dump(exclude_unset=True)

        # === VALIDACIÓN DE LA LLAVE FORÁNEA ===
        # Si el usuario intenta modificar la cliente del cliente, verificamos que sea válida
        if "cliente_id" in update_data:
            self._validar_cliente(update_data["clientes_id"])
        # ======================================
        for key, value in update_data.items():
            setattr(db_client, key, value)
        self.db.commit() # Guarda los cambios en la base de datos
        self.db.refresh(db_client) # Refresca el objeto con los datos actualizados
    return db_client
class ClientService:
    """Agrupa las operaciones CRUD de clientes sobre una sesion de BD."""

    def __init__(self, db: Session):
        """Recibe una sesion de SQLAlchemy ya creada por la capa de conexion."""
        self.db = db

    def get_all(self):
        """Devuelve todas las clientes almacenadas."""
        return self.db.query(Client).all()

    def get_by_id(self, client_id: int):
        """Busca un cliente por su identificador y devuelve el primero que coincida."""
        return self.db.query(Client).filter(Client.id == client_id).first()
    
    def create(self, client_in: ClientCreate):
        """Crea un nuevo cliente a partir del esquema de entrada y lo persiste."""
        db_client = Client(**client_in.model_dump())
        self.db.add(db_client) # Agrega el nuevo cliente a la sesion de trabajo
        self.db.commit()# Guarda los cambios en la base de datos
        self.db.refresh(db_client) # Refresca el objeto con los datos actualizados (como el ID generado)
        return db_client

def update(self, client_id: int, client_in: ClientUpdate):
    """Actualiza un cliente existente con los campos enviados."""
    db_client = self.get_by_id(client_id)
    if db_client:
        # Solo actualiza los campos que fueron enviados (exclude_unset=True)
        update_data = client_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_client, key, value)
        self.db.commit() # Guarda los cambios en la base de datos
        self.db.refresh(db_client) # Refresca el objeto con los datos actualizados
    return db_client

def delete(self, client_id: int):
    """Elimina un cliente por ID y devuelve True si la operacion se completo."""
    db_client = self.get_by_id(client_id)
    if db_client:
        self.db.delete(db_client)# Elimina la cliente de la sesion de trabajo
        self.db.commit()# Guarda los cambios en la base de datos
        return True
    return False