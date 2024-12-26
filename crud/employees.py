from datetime import datetime, timedelta
from typing import List, Tuple

from sqlalchemy import select, insert, func, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from models.ecpes import EcpORM
from models.kriptoproies import KriptosORM
from schemas.employees import Employee, EmployeeAdd, EmployeePost

from schemas.employees import EmployeePatch

from database import session_maker, engine
from repositories.employees import EmployeesRepository
from exetions.exeption_ import EmployeeNotFoundException
from models.employess import EmployeesORM


def get_one_with_employees_full_name(full_name=None):
    with session_maker() as session:
        # query = select(EmployeesORM).where(EmployeesORM.full_name.ilike(f"%{full_name.lower()}%"))
        query = select(EmployeesORM).where(func.lower(EmployeesORM.full_name).like(f"%{full_name}%"))
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = session.execute(query)
        model = result.scalars().first()
        print(model)
        return model

    # Добавление сотрудника


def get_ecp_kriptopro_employee_name(full_name=None):
    with session_maker() as session:
        query = (select(EmployeesORM).
        options(joinedload(EmployeesORM.ecp),
                joinedload(EmployeesORM.kriptos)
                ).where(
            func.lower(EmployeesORM.full_name).like(f"%{full_name}%")))
        print(query.compile(compile_kwargs={"literal_binds": True}))

        result = session.execute(query)
        model = result.scalars().first()
        if model is None:
            raise ValueError(f"Сотрудник с ФИО '{full_name}' не найден.")
        print(model)
        return model

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


def get_employees_with_expiring_licenses() -> List[
    Tuple[EmployeesORM, List[EcpORM], List[KriptosORM]]]:
    """
    Возвращает список сотрудников с близким окончанием срока лицензии, а также их связанные объекты ECP и Kriptos.
    """
    current_date = datetime.now()
    date_limit = current_date + timedelta(days=20)

    with session_maker() as session:
        result = []

        # Получаем сотрудников с заканчивающимися лицензиями на ECP
        ecp_stmt = (
            select(EmployeesORM, EcpORM)
            .join(EcpORM, EmployeesORM.ecp)
            .where(EcpORM.finish_date <= date_limit)
        )
        ecps = session.execute(ecp_stmt).all()

        # Получаем сотрудников с заканчивающимися лицензиями на Kriptos
        kriptos_stmt = (
            select(EmployeesORM, KriptosORM)
            .join(KriptosORM, EmployeesORM.kriptos)
            .where(KriptosORM.finish_date <= date_limit)
        )
        kriptos = session.execute(kriptos_stmt).all()

        # Группируем результаты по сотрудникам
        employee_dict = {}

        for employee, ecp in ecps:
            if employee not in employee_dict:
                employee_dict[employee] = {"ecp": [], "kriptos": []}
            employee_dict[employee]["ecp"].append(ecp)

        for employee, kripto in kriptos:
            if employee not in employee_dict:
                employee_dict[employee] = {"ecp": [], "kriptos": []}
            employee_dict[employee]["kriptos"].append(kripto)

        # Формируем итоговый список
        for employee, related_objects in employee_dict.items():
            result.append((employee, related_objects["ecp"], related_objects["kriptos"]))

        return result


def delete_employee(
    employee_id: int,
):
    with session_maker() as session:
        delete_empl_stmt = delete(EmployeesORM).where(EmployeesORM.id == employee_id)
        print(delete_empl_stmt.compile(compile_kwargs={"literal_binds":True}))
        session.execute(delete_empl_stmt)
        session.commit()


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
