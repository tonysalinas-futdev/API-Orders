from sqlalchemy import Integer, ForeignKey, String, DateTime,Column,Float, event
import datetime
from database import Base
from sqlalchemy.orm import relationship

#Modelo para los detalles de la orden por producto
class Order_Details(Base):
    __tablename__="order_details"
    id=Column(Integer, primary_key=True, autoincrement=True, index=True)
    product_name=Column(String, nullable=False, index=True)
    product_price=Column(Float, nullable=False)
    quantity=Column(Integer, nullable=False)
    total_price=Column(Float)
    order_id=Column(ForeignKey("orders.id"))
    order=relationship("Order", back_populates="order_details")

#Función para calcular el total price antes de guardar la tabla en la base de datos
@event.listens_for(Order_Details, "before_insert")
def calculate_total_price(mapper, connection, target):
    #Comprobamos que el precio y la cantidad no sean None y procedemos a calcular el precio total
    if target.product_price is not None and target.quantity is not None:
        target.total_price = target.product_price * target.quantity


#Modelo para las órdenes

class Order(Base):
    __tablename__="orders"
    id=Column(Integer, primary_key=True, autoincrement=True, index=True)
    date=Column(DateTime, default=datetime.datetime.utcnow)
    order_details=relationship("Order_Details", back_populates="order", cascade="all, delete-orphan")
    user_id=Column(Integer, index=True)
    status_id = Column(Integer, ForeignKey("status.id"))
    status=relationship("Status", back_populates="order")

#Modelo para el estado mde las órdenes
class Status(Base):
    __tablename__="status"
    id=Column(Integer, primary_key=True, autoincrement=True, index=True)
    name=Column(String)
    
    order=relationship("Order", back_populates="status")