from typing import List

from fastapi import APIRouter, status, HTTPException
from schemas.product import ProductBase, ProductCreate, ProductUpdate, ProductOut

#Base de datos simulada
productos=[
{"id":1,"nombre":"Lapiz No.2","stock":5,"precio":2000},
{"id":2,"nombre":"Borrador Miga Pan","stock":10,"precio":1200}
]

router = APIRouter()

#Consulta general
@router.get("/",response_model=List[ProductOut])
async def obtener_productos():
    """Retorna la lista completa de productos almacenados en la base de datos simulada."""
    return productos

#Consulta específica
@router.get("/{id}")
def obtener_producto(id:int):
    """
    Busca y retorna un producto específico según su ID.
    Si no existe un producto con ese ID, lanza una excepción HTTP 404.
    """
    producto = next((p for p in productos if p["id"]==id), None)
    if not producto:
        raise HTTPException(status_code=404, message="Producto no encontrado")
    return producto

#Agregar un producto
@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def crear_producto(new_product: ProductCreate):
    """
    Crea un nuevo producto y lo agrega a la base de datos simulada.
    Genera automáticamente un ID único incrementando el mayor ID existente.
    Retorna el producto recién creado con su ID asignado.
    """
    #Lógica de incremento del id
    nuevo_id= max(p["id"] for p in productos) + 1 if productos else 1

    #Desempaquetar el new_product
    nuevo_producto= {**new_product.model_dump(), "id":nuevo_id}
    #Guardar
    productos.append(nuevo_producto)
    return nuevo_producto

@router.put("/{id}", response_model=ProductOut)
async def actualizar_producto(id:int, producto:ProductUpdate):
    """
    Actualiza los campos de un producto existente identificado por su ID.
    Solo modifica los campos enviados en el cuerpo de la solicitud (campos no enviados se
    conservan).
    Si no existe un producto con ese ID, lanza una excepción HTTP 404.
    """
    for i, p in enumerate(productos):
        if p["id"]==id:
            update_data= producto.model_dump(exclude_unset=True)
            productos[i].update(update_data)
            return productos[i]

    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(producto_id: int):
    """
    Elimina un producto de la base de datos simulada según su ID.
    Si el producto es encontrado, lo elimina y retorna una respuesta HTTP 204
    (sin contenido).
    Si no existe un producto con ese ID, lanza una excepción HTTP 404.
    """
    for i, p in enumerate(productos):
        if p["id"] == producto_id:
            productos.pop(i)
            return

    raise HTTPException(status_code=404, detail="Producto no encontrado")