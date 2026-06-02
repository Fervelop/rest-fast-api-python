from sqlalchemy.orm import Session
from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate
from fastapi import HTTPException, status
from models.category import Category

def _validar_categoria(self, categoria_id: int):

    """Método interno auxiliar para verificar si una categoría existe en la BD."""
    category_exists = self.db.query(Category).filter(Category.id == categoria_id).first()
    if not category_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operación inválida: La categoría con ID {categoria_id} no existe."
        )

def create(self, category_in: CategoryCreate):

    """Crea un nuevo producto a partir del esquema de entrada y lo persiste."""
    # 1. VALIDACIÓN: Asegurar que la categoría asignada al nuevo producto exista
    self._validar_categoria(category_in.categoria_id)

    # 2. PERSISTENCIA: Si la categoría existe, procedemos a guardar el producto
    db_category = Category(**category_in.model_dump())

    self.db.add(db_category) # Agrega el nuevo producto a la sesion de trabajo
    self.db.commit()# Guarda los cambios en la base de datos
    self.db.refresh(db_category) # Refresca el objeto con los datos actualizados (como el ID generado)
    return db_category

def update(self, category_id: int, category_in: CategoryUpdate):

    """Actualiza una categoría existente con los campos enviados."""
    db_category = self.get_by_id(category_id)
    if db_category:
        # Solo actualiza los campos que fueron enviados (exclude_unset=True)
        update_data = category_in.model_dump(exclude_unset=True)

        # === VALIDACIÓN DE LA LLAVE FORÁNEA ===
        # Si el usuario intenta modificar la categoría del producto, verificamos que sea válida
        if "categoria_id" in update_data:
            self._validar_categoria(update_data["categorias_id"])
        # ======================================
        for key, value in update_data.items():
            setattr(db_category, key, value)
        self.db.commit() # Guarda los cambios en la base de datos
        self.db.refresh(db_category) # Refresca el objeto con los datos actualizados
    return db_category
class CategoryService:
    """Agrupa las operaciones CRUD de categorías sobre una sesion de BD."""

    def __init__(self, db: Session):
        """Recibe una sesion de SQLAlchemy ya creada por la capa de conexion."""
        self.db = db

    def get_all(self):
        """Devuelve todas las categorías almacenadas."""
        return self.db.query(Category).all()

    def get_by_id(self, category_id: int):
        """Busca una categoría por su identificador y devuelve el primero que coincida."""
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def create(self, category_in: CategoryCreate):
        """Crea un nuevo producto a partir del esquema de entrada y lo persiste."""
        db_category = Category(**category_in.model_dump())
        self.db.add(db_category) # Agrega el nuevo producto a la sesion de trabajo
        self.db.commit()# Guarda los cambios en la base de datos
        self.db.refresh(db_category) # Refresca el objeto con los datos actualizados (como el ID generado)
        return db_category

def update(self, category_id: int, category_in: CategoryUpdate):
    """Actualiza una categoría existente con los campos enviados."""
    db_category = self.get_by_id(category_id)
    if db_category:
        # Solo actualiza los campos que fueron enviados (exclude_unset=True)
        update_data = category_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        self.db.commit() # Guarda los cambios en la base de datos
        self.db.refresh(db_category) # Refresca el objeto con los datos actualizados
    return db_category

def delete(self, category_id: int):
    """Elimina una categoría por ID y devuelve True si la operacion se completo."""
    db_category = self.get_by_id(category_id)
    if db_category:
        self.db.delete(db_category)# Elimina la categoría de la sesion de trabajo
        self.db.commit()# Guarda los cambios en la base de datos
        return True
    return False