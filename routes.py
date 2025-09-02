from fastapi import APIRouter, Depends,status
import schemas, models, database, sqlalchemyrepo
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

router=APIRouter(prefix="/orders", tags=["Orders"])

async def get_db(db:AsyncSession=Depends(database.get_session)):
    return db

async def get_repo(session:AsyncSession=Depends(get_db)):
    return sqlalchemyrepo.SQLAlchemyRepository(session)


#Enpoint para crear una orden
@router.post("/create", response_model=schemas.JsonRespons, description="Endpoint para crear una orden", status_code=status.HTTP_201_CREATED)
async def create_order(model:schemas.OrderCreate, service:sqlalchemyrepo.SQLAlchemyRepository=Depends(get_repo)):
    await service.create(model)
    return {"message":"Orden creada exitosamente"}


#Enpoint para que el cliente obtenga una orden suya junto con sus detalles
@router.get("/get_client_order/{order_id}", response_model=schemas.OrderClientSend, summary="Endpoint para que el cliente obtenga los detalles de alguna orden suya")
async def get_client_order(order_id:int, service:sqlalchemyrepo.SQLAlchemyRepository=Depends(get_repo)):
    orden=await service.get_order_by_id(order_id)
    return orden

#Endpoint para que el admin obtenga una orden y sus detalles

@router.get("/get_order/{order_id}", response_model=schemas.OrderBase, summary="Endpoint para que el admin obtenga todo sobre una orden", status_code=status.HTTP_200_OK)
async def get_admin_order(order_id:int, service:sqlalchemyrepo.SQLAlchemyRepository=Depends(get_repo)):
    orden=await service.get_by_id(order_id)
    return orden



#Endpoint para obtener todos los detalles

@router.get("/get_all", response_model=List[schemas.OrderBase], summary="Endpoint para que el admin obtenga todas las órdenes", status_code=status.HTTP_200_OK)
async def get_all(service:sqlalchemyrepo.SQLAlchemyRepository=Depends(get_repo)):
    orden=await service.get_all()
    return orden

@router.put("/update_status/{order_id}", response_model=schemas.JsonRespons, summary="Endpoint para actualizar el estado de una orden", status_code=status.HTTP_200_OK)
async def update( order_id:int,request:schemas.StatusUpdate,service:sqlalchemyrepo.SQLAlchemyRepository=Depends(get_repo)):
    await service.update_status(order_id, request.status)
    return {"message":"Status actualizado exitosamente"}

@router.delete("/delete/{order_id}", response_model=schemas.JsonRespons, status_code=status.HTTP_200_OK, summary="Endpoint para eliminar una orden")
async def delete( order_id:int,service:sqlalchemyrepo.SQLAlchemyRepository=Depends(get_repo)):
    await service.delete(order_id)
    return {"message":"Orden eliminada exitosamente"}