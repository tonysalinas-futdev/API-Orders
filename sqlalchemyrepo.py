
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession 
import schemas
from models import Order, Order_Details, Status


from fastapi import HTTPException




class SQLAlchemyRepository():
    #Iniciamos el modelo y la session
    def __init__(self, session:AsyncSession):
        self.session=session
        

    #Función para que el admin obtenga una orden según su id , con todos los datos 
    async def get_by_id(self,object_id):
        stmt=select(Order).options(
            selectinload(Order.order_details),
            selectinload(Order.status)).where(Order.id==object_id)

        
        result=await self.session.execute(stmt)
        object=result.scalar_one_or_none()
        if not object:
            raise HTTPException(status_code=404, detail="File not found")
        return object


    #Funcion para que el cliente obtenga una orden y sus detalles, sin mostrar datos sensibles
    async def get_order_by_id(self,order_id:int):
        stmt=select(Order).options(
            selectinload(Order.order_details),
            selectinload(Order.status)).where(Order.id==order_id)
        
        result=await self.session.execute(stmt)
        object=result.scalar_one_or_none()
        if not object:
            raise HTTPException(status_code=404, detail="File not found")
        data={
            "date":object.date,
            "status":object.status.name,
            "order_details":object.order_details
            
        }

        return schemas.OrderClientSend.model_validate(data)

    
    #Funcion para que el admin obtenga todas las ordenes
    async def get_all(self):
        stmt= stmt=select(Order).options(
            selectinload(Order.order_details),
            selectinload(Order.status))
        result=await self.session.execute(stmt)
        list_=result.scalars().all()
        return list_
        


    #Función utilizada para eliminar una orden
    async def delete(self, order_id: int)->None:
        objeto=await self.get_by_id(order_id)
        try:
            await self.session.delete(objeto)
            await self.session.commit()
        except  Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))



    #Funcion para que el cliente cree una nueva orden 
    async def create(self, object:schemas.OrderCreate):
        
        data=object.model_dump(exclude_none=True)

        stmt=select(Status).where(Status.name=="Pendiente")
        result=await self.session.execute(stmt)
        pending_status=result.scalar_one_or_none()
        order_details_data=data.get("order_details")
        order_details_obj=[Order_Details(**detalle) for detalle in order_details_data]
        data.pop("order_details")
        new_object=Order(**data, status=pending_status, order_details=order_details_obj)

        try:
            self.session.add(new_object)
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(new_object)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
        return new_object

    #Función para actualizar el estado de una orden
    async def update_status(self,order_id, new_status:str):
        order=await self.get_by_id(order_id)
        stmt=select(Status).where(Status.name==new_status)
        result=await self.session.execute(stmt)
        status=result.scalar_one_or_none()
        if not status:
            raise HTTPException(status_code=404,detail="No existe ningún status con ese nombre en la base de datos")
        order.status=status
        
        
        await self.session.commit()
