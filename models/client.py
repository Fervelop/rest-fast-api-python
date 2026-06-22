# src/models/client.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class Client(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Relación virtual: Un cliente tiene muchas órdenes
    orders = relationship("Order", back_populates="client")
