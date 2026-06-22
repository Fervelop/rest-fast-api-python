# src/models/product.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class Order(Base):
    __tablename__ = "ordenes"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    # Relación virtual: Una orden pertenece a un cliente
    client = relationship("Client", back_populates="orders")
