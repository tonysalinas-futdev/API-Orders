from pydantic import BaseModel, Field
from typing import List, Optional
import datetime
from fastapi.responses import JSONResponse

class StatusBase(BaseModel):
    id:int
    name:str


class OrderDetailsBase(BaseModel):
    id:int
    product_name:str
    product_price:float
    quantity:int
    order_id:int
    total_price:float

    class Config:
        from_attributes = True 



#Schema para modelo que solo puede ver el admin
class OrderBase(BaseModel):
    id:int
    date:datetime.datetime
    user_id:int
    order_details:Optional[List[OrderDetailsBase]]
    status:StatusBase
    class Config:
        from_attributes=True


#Schema con la info que puede ver el cliente
class OrderDetailsClientSend(BaseModel):
    product_name:str
    product_price:float
    quantity:int
    total_price:float
    class Config:
        from_attributes = True

#Info con la orden que va a ver el cliente
class OrderClientSend(BaseModel):
    date:datetime.datetime
    status:str
    order_details:List[OrderDetailsClientSend]
    class Config:
        from_attributes = True


class OrderDetailsCreate(BaseModel):
    product_name:str
    product_price:float
    quantity:int



class OrderCreate(BaseModel):
    user_id:int
    order_details:List[OrderDetailsCreate]



class JsonRespons(BaseModel):
    message:str

class StatusUpdate(BaseModel):
    status:str