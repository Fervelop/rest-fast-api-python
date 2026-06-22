from sqlalchemy.orm import Session
from models.order import Order
from schemas.order import OrderCreate, OrderUpdate
from fastapi import HTTPException, status
from models.order import Order

def _validar_orden(self, orden_id: int):

    """Método interno auxiliar para verificar si una orden existe en la BD."""
    order_exists = self.db.query(Order).filter(Order.id == orden_id).first()
    if not order_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operación inválida: La orden con ID {orden_id} no existe."
        )

def create(self, order_in: OrderCreate):

    """Crea un nuevo orden a partir del esquema de entrada y lo persiste."""
    # 1. VALIDACIÓN: Asegurar que la orden asignada al nuevo orden exista
    self._validar_orden(order_in.orden_id)

    # 2. PERSISTENCIA: Si la orden existe, procedemos a guardar el orden
    db_order = Order(**order_in.model_dump())

    self.db.add(db_order) # Agrega el nuevo orden a la sesion de trabajo
    self.db.commit()# Guarda los cambios en la base de datos
    self.db.refresh(db_order) # Refresca el objeto con los datos actualizados (como el ID generado)
    return db_order

def update(self, order_id: int, order_in: OrderUpdate):

    """Actualiza una orden existente con los campos enviados."""
    db_order = self.get_by_id(order_id)
    if db_order:
        # Solo actualiza los campos que fueron enviados (exclude_unset=True)
        update_data = order_in.model_dump(exclude_unset=True)

        # === VALIDACIÓN DE LA LLAVE FORÁNEA ===
        # Si el usuario intenta modificar la orden del orden, verificamos que sea válida
        if "orden_id" in update_data:
            self._validar_orden(update_data["ordens_id"])
        # ======================================
        for key, value in update_data.items():
            setattr(db_order, key, value)
        self.db.commit() # Guarda los cambios en la base de datos
        self.db.refresh(db_order) # Refresca el objeto con los datos actualizados
    return db_order
class OrderService:
    """Agrupa las operaciones CRUD de ordens sobre una sesion de BD."""

    def __init__(self, db: Session):
        """Recibe una sesion de SQLAlchemy ya creada por la capa de conexion."""
        self.db = db

    def get_all(self):
        """Devuelve todas las ordens almacenadas."""
        return self.db.query(Order).all()

    def get_by_id(self, order_id: int):
        """Busca una orden por su identificador y devuelve el primero que coincida."""
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def create(self, order_in: OrderCreate):
        """Crea un nuevo orden a partir del esquema de entrada y lo persiste."""
        db_order = Order(**order_in.model_dump())
        self.db.add(db_order) # Agrega el nuevo orden a la sesion de trabajo
        self.db.commit()# Guarda los cambios en la base de datos
        self.db.refresh(db_order) # Refresca el objeto con los datos actualizados (como el ID generado)
        return db_order

def update(self, order_id: int, order_in: OrderUpdate):
    """Actualiza una orden existente con los campos enviados."""
    db_order = self.get_by_id(order_id)
    if db_order:
        # Solo actualiza los campos que fueron enviados (exclude_unset=True)
        update_data = order_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_order, key, value)
        self.db.commit() # Guarda los cambios en la base de datos
        self.db.refresh(db_order) # Refresca el objeto con los datos actualizados
    return db_order

def delete(self, order_id: int):
    """Elimina una orden por ID y devuelve True si la operacion se completo."""
    db_order = self.get_by_id(order_id)
    if db_order:
        self.db.delete(db_order)# Elimina la orden de la sesion de trabajo
        self.db.commit()# Guarda los cambios en la base de datos
        return True
    return False