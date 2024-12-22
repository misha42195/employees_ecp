from sqlalchemy import select, func, insert

from database import engine
from repositories.base import BaseRepository
from models.employess import EmployeesORM
from schemas.employees import Employee

class EmployeesRepository(BaseRepository):
    model = EmployeesORM
    schema = Employee

    def get_all(self,
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

        result =  self.session.execute(query)
        return result.scalars().all()
