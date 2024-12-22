from oauthlib.uri_validate import query
from pydantic import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from schemas.employees import Employee, EmployeeAdd, EmployeePost

from schemas.employees import EmployeePatch
from crud.dependensis import PaginationDep
from database import session_maker, engine
from repositories.employees import EmployeesRepository
from exetions.exeption_ import EmployeeNotFoundException
from models.employess import  EmployeesORM



# def get_all_employess(
#     page = 1,
#     per_page = 10
# ):
#     with session_maker() as session:
#         query = select(EmployeesORM).limit(per_page).offset(per_page * (page - 1))
#         print(query.compile(compile_kwargs={"literal_binds": True}))
#         result = session.execute(query)
#         result = result.scalars().all()
#         print(f"result: ",result)
#         emloyees = [Employee.model_validate(model, from_attributes=True) for model in result]
#         print(f"employees: {emloyees}")
#         return emloyees

def get_one_with_employees_full_name(full_name=None):
        with session_maker() as session:
            if not full_name:
                raise EmployeeNotFoundException(full_name=full_name)
            query = select(EmployeesORM.full_name.ilike(f"%{full_name}%"))
            result= session.execute(query).scalars().one_or_none()
            print(result)
            if result is None:
                raise EmployeeNotFoundException(f"Сотрудник с именем {full_name} не найден")
            print(f"result: ",result)
            empl =  Employee.model_validate(result, from_attributes=True)
            print(f"empl: ",empl)
            return empl



def delete_employee(
    employee_id: int,
):
    with session_maker() as session:
        EmployeesRepository(session).delete(id=employee_id)
        session.commit()

# Добавление сотрудника
def add_employee(employee_data: EmployeePost):
    with session_maker() as session:
        _employee_data = EmployeePost(**employee_data.model_dump())

        ext_employee = session.execute(select(EmployeesORM).filter_by(full_name=_employee_data.full_name)).scalar()
        if ext_employee:
            # Если сотрудник с таким именем уже существует, выбрасываем ошибку
            raise ValueError(f"Сотрудник с именем '{_employee_data.full_name}' уже существует.")

        try:
            add_employees_stmt = insert(EmployeesORM).values(**_employee_data.model_dump()).returning(EmployeesORM)
            print(add_employees_stmt.compile(engine, compile_kwargs={"literal_bins": True}))
            result = session.execute(add_employees_stmt)
            model = result.scalars().one()
            employees = Employee.model_validate(model, from_attributes=True)
            session.commit()
            return employees
        except IntegrityError as e:
            session.rollback()
            # В случае ошибки вставки (например, нарушение уникальности) возвращаем соответствующую ошибку
            raise ValueError(f"Ошибка при добавлении сотрудника: {str(e)}")






def full_update_employee(
    employee_id: int,
    employee_data: EmployeeAdd,
):
    with session_maker() as session:
        EmployeesRepository(session).edit(employee_data, id=employee_id)
        session.commit()
        return {"status": "ok"}


def update_employee(
    employee_id: int,
    employee_data: EmployeePatch,
):
    with session_maker() as session:
        EmployeesRepository(session).edit(employee_data, exclude_unset=True, id=employee_id)
        session.commit()
        return {"status": "ok"}
