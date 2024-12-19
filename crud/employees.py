
from schemas.employees import Employee, EmployeeAdd

from schemas.employees import EmployeePatch
from crud.dependensis import PaginationDep
from database import async_session_maker
from repositories.employees import EmployeesRepository
from exetions.exeption import EmployeeNotFoundException


def get_employees(
    pagination: PaginationDep,
    full_name: str
):
    with async_session_maker() as session:
        res = EmployeesRepository(session).get_all(
            full_name=full_name,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1)
        )
        return {"empl": res}


def get_one_employess(employees_id: int):
    with async_session_maker() as session:
        employees = EmployeesRepository(session).get_one(id=employees_id)
        if employees is None:
            raise EmployeeNotFoundException(404, detail="Сотрудник с таким id не найден")
        return {"status": "ok", "employees": employees}



def delete_employee(
    employee_id: int,
):
    async with async_session_maker() as session:
        EmployeesRepository(session).delete(id=employee_id)
        session.commit()


def create_employee(
    employee_data: EmployeeAdd):
    async with async_session_maker() as session:
        employees = EmployeesRepository(session).add(employee_data)

        session.commit()

    return {"status": "ok", "employees": employees}


def full_update_employee(
    employee_id: int,
    employee_data: EmployeeAdd,
):
    with async_session_maker() as session:
        EmployeesRepository(session).edit(employee_data, id=employee_id)
        session.commit()
        return {"status": "ok"}


def update_employee(
    employee_id: int,
    employee_data: EmployeePatch,
):
    with async_session_maker() as session:
        EmployeesRepository(session).edit(employee_data, exclude_unset=True, id=employee_id)
        session.commit()
        return {"status": "ok"}
