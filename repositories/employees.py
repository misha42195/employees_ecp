from sqlalchemy import select, func, insert

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.employess import EmployeesORM
from src.schemas.employees import Employee

class EmployeesRepository(BaseRepository):
    model = EmployeesORM
    schema = Employee

    async def get_all(self,
                      full_name,
                      limit,
                      offset):
        query = select(EmployeesORM)
        if full_name:
            query = (query.filter(EmployeesORM.full_name.ilike(f"%{full_name}%"))
                     .limit(limit)
                     .offset(offset))
        else:
            query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return result.scalars().all()
