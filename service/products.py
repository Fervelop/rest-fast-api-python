from sqlalchemy.orm import Session
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate
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

def create(self, product_in: ProductCreate):

    """Crea un nuevo producto a partir del esquema de entrada y lo persiste."""
    # 1. VALIDACIÓN: Asegurar que la categoría asignada al nuevo producto exista
    self._validar_categoria(product_in.categoria_id)

    # 2. PERSISTENCIA: Si la categoría existe, procedemos a guardar el producto
    db_product = Product(**product_in.model_dump())

    self.db.add(db_product) # Agrega el nuevo producto a la sesion de trabajo
    self.db.commit()# Guarda los cambios en la base de datos
    self.db.refresh(db_product) # Refresca el objeto con los datos actualizados (como el ID generado)
    return db_product

def update(self, product_id: int, product_in: ProductUpdate):

    """Actualiza un producto existente con los campos enviados."""
    db_product = self.get_by_id(product_id)
    if db_product:
        # Solo actualiza los campos que fueron enviados (exclude_unset=True)
        update_data = product_in.model_dump(exclude_unset=True)

        # === VALIDACIÓN DE LA LLAVE FORÁNEA ===
        # Si el usuario intenta modificar la categoría del producto, verificamos que sea válida
        if "categoria_id" in update_data:
            self._validar_categoria(update_data["categorias_id"])
        # ======================================
        for key, value in update_data.items():
            setattr(db_product, key, value)
        self.db.commit() # Guarda los cambios en la base de datos
        self.db.refresh(db_product) # Refresca el objeto con los datos actualizados
    return db_product
class ProductService:
    """Agrupa las operaciones CRUD de productos sobre una sesion de BD."""

    def __init__(self, db: Session):
        """Recibe una sesion de SQLAlchemy ya creada por la capa de conexion."""
        self.db = db

    def get_all(self):
        """Devuelve todos los productos almacenados."""
        return self.db.query(Product).all()

    def get_by_id(self, product_id: int):
        """Busca un producto por su identificador y devuelve el primero que coincida."""
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def create(self, product_in: ProductCreate):
        """Crea un nuevo producto a partir del esquema de entrada y lo persiste."""
        db_product = Product(**product_in.model_dump())
        self.db.add(db_product) # Agrega el nuevo producto a la sesion de trabajo
        self.db.commit()# Guarda los cambios en la base de datos
        self.db.refresh(db_product) # Refresca el objeto con los datos actualizados (como el ID generado)
        return db_product

def update(self, product_id: int, product_in: ProductUpdate):
    """Actualiza un producto existente con los campos enviados."""
    db_product = self.get_by_id(product_id)
    if db_product:
        # Solo actualiza los campos que fueron enviados (exclude_unset=True)
        update_data = product_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        self.db.commit() # Guarda los cambios en la base de datos
        self.db.refresh(db_product) # Refresca el objeto con los datos actualizados
    return db_product

def delete(self, product_id: int):
    """Elimina un producto por ID y devuelve True si la operacion se completo."""
    db_product = self.get_by_id(product_id)
    if db_product:
        self.db.delete(db_product)# Elimina el producto de la sesion de trabajo
        self.db.commit()# Guarda los cambios en la base de datos
        return True
    return False