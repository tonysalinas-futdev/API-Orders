from models import Status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


#Función para inicializar nuestros roles básicos en la bd, debemos hacerlo por separado por si acaso solo algunos no se crearon por error
async def init_status(session:AsyncSession):
    status_names=["Pendiente","Entregado", "Cancelado","En espera", "Enviado"]
    stmt=select(Status).where(Status.name.in_(status_names))
    result=await session.execute(stmt)
    existing=result.scalars().all()
    existng_names=[st.name for st in existing]
    add_=[Status(name=nombre) for nombre in status_names if nombre not in existng_names]
    
    session.add_all(add_)
    await session.commit()

    