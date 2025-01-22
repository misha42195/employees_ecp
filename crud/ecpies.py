from datetime import datetime, timedelta


from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload


from models.ecpes import EcpORM
from database import session_maker, engine
from schemas.ecpies import EcpAdd, EcpReqestAdd, EcpPatch, EcpPut



def get_all_ecp(
    page = 1,
    per_page = 10
):
    with session_maker() as session:
        query = select(EcpORM).limit(per_page).offset(per_page * (page - 1))
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = session.execute(query)
        emloyees = result.scalars().all()
        print(emloyees)
        return emloyees


def get_one_ecp(
    install_location:str,
    storage_location
):
    with session_maker() as session:
        query = select(EcpORM)
        if install_location is not None:
            query = query.filter(EcpORM.install_location.ilike(f"%{install_location}%"))
        if storage_location is not None:
            query = query.filter(EcpORM.storage_location.ilike(f"%{storage_location}%"))

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = session.execute(query)
        ecp = result.scalars().all()
        return {"status": "ok", "ecp": ecp}



def get_one_ecp(ecp_id: int):
     with session_maker() as session:
        query = select(EcpORM).filter_by(id=ecp_id)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = session.execute(query)
        ecp = result.scalars().one()
        return {"status": "ok", "ecp": ecp}



def create_ecp(
    employees_id: int,
    ecp_data: EcpReqestAdd):

    with session_maker() as session:
        _ecp_data = EcpAdd(employees_id=employees_id, **ecp_data.model_dump())
        ecp_data_stmt = insert(EcpORM).values(_ecp_data.model_dump()).returning(EcpORM)
        print(ecp_data_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result =  session.execute(ecp_data_stmt)
        ecp = result.scalars().one()
        session.commit()
        return ecp



def full_update_ecp(
    employees_id: int,
    ecp_id: int,
    ecp_data: EcpPut):
    _ecp_data = EcpPut(**ecp_data.model_dump())
    with session_maker() as session:
        ecp_update_stmt = (
            update(EcpORM).
            filter_by(id=ecp_id, employees_id=employees_id).
            values(**_ecp_data.model_dump())
        )
    print(ecp_update_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
    session.execute(ecp_update_stmt)
    session.commit()
    return {"status": "ok"}


def update_ecp(
    employees_id: int,
    ecp_id: int,
    ecp_data: EcpPatch):
    _ecp_data = EcpPatch(**ecp_data.model_dump(exclude_unset=True))
    print(_ecp_data)
    with session_maker() as session:
        update_ecp_stmt = (update(EcpORM).
                           filter_by(id=ecp_id, employees_id=employees_id).
                           values(**_ecp_data.model_dump(exclude_unset=True))
                           )
        session.execute(update_ecp_stmt)
        session.commit()
        return {"status": "ok"}

def delete_ecp(ecp_id: int):
    with session_maker() as session:
        ecp_delete_stmt = (delete(EcpORM).
                           filter_by(id=ecp_id)
                           .returning(EcpORM))
        result =  session.execute(ecp_delete_stmt)

        ecp = result.scalars().one()
        session.commit()

        return ecp



def get_expiring_ecp():
    today = datetime.today()
    warning_day = today + timedelta(days=20)

    # Получаем все записи из таблицы EcpORM с заканчивающимися лицензиями и заранее подгружаем связанные сущности
    with session_maker() as session:
        query = (
            select(EcpORM)
            .options(joinedload(EcpORM.employee))  # Подгружаем данные о сотрудниках
            .filter(EcpORM.finish_date <= warning_day)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = session.execute(query)
        expiring_ecp = result.scalars().all()
        print(expiring_ecp)

        return expiring_ecp
