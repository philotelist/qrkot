from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get_multi(
        self,
        session: AsyncSession,
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data["user_id"] = user.id
        obj_in_data["create_date"] = datetime.now()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @staticmethod
    def set_close(obj):
        obj.fully_invested = True
        obj.close_date = datetime.now()
        return obj
