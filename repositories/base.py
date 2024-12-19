from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update

from database import engine


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        employees = [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
        return employees

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        add_employees_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        print(add_employees_stmt.compile(engine, compile_kwargs={"literal_bins": True}))
        result = await self.session.execute(add_employees_stmt)
        model = result.scalars().one()
        employees = self.schema.model_validate(model, from_attributes=True)
        return employees

    async def edit(self, data: BaseModel, exclude_unset=False, **filter_by) -> None:
        # if employees is None:
        #     raise HTTPException(404,detail="Объект не найден")
        update_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))

        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        await self.session.execute(delete_stmt)
