from fastapi import APIRouter
from api.v1.endpoints import products, categories


api_router=APIRouter()
api_router.include_router(products.router, prefix="/products",
tags=["Productos"])

api_router.include_router(categories.router, prefix="/categories",
tags=["Categorias"])

api_router.include_router(clients.router, prefix="/clients",
tags=["Clientes"])

api_router.include_router(orders.router, prefix="/orders",
tags=["Ordenes"])

api_router.include_router(users.router, prefix="/users",
tags=["Usuarios"])