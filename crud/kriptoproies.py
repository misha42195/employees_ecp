from sqlalchemy import select, insert, update, delete

from fastapi import APIRouter, Body
from models.kriptoproies import KriptosORM
from schemas.kriptopro import KriptoproRequestAdd, KriptoproPut, KriptoproPath, KriptoproRequestAdd
from schemas.kriptopro import KriptoproAdd
from database import session_maker, session_maker, engine


async def get_kriptos(
    employees_id: int,
    kriptopro_id: int,

):
    with session_maker() as session:
        query = select(KriptosORM).filter_by(id=kriptopro_id, employees_id=employees_id)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)
        kript = result.scalars().all()
        return {"status": "ok", "kript": kript}


def create_kriptopro(
    employees_id: int,
    kriptopro_data: KriptoproRequestAdd):
    with session_maker() as session:
        _kriptopro_data = KriptoproAdd(employees_id=employees_id, **kriptopro_data.model_dump())
        kriptopro_data_stmt = insert(KriptosORM).values(_kriptopro_data.model_dump()).returning(KriptosORM)
        print(kriptopro_data_stmt.compile(engine,compile_kwargs={"literral_binds":True}))
        result = session.execute(kriptopro_data_stmt)
        kripto = result.scalars().one()
        session.commit()
        return kripto


def full_update_kriptopro(
    employees_id: int,
    kriptopro_id: int,
    kriptopro_data: KriptoproRequestAdd = Body()
):
    with session_maker() as session:
        _kriptopro_data = KriptoproPut(**kriptopro_data.model_dump())
        _kriptopro_data_stmt = (update(KriptosORM).
                                filter_by(id=kriptopro_id, employees_id=employees_id)
                                .values(**kriptopro_data.model_dump()))
        session.execute(_kriptopro_data_stmt)
        session.commit()
        return {"status": "ok"}


def update_kriptopro(
    employees_id: int,
    kriptopro_id: int,
    kriptopro_data: KriptoproRequestAdd = Body()
):
    _kriptopro_data = KriptoproPath(**kriptopro_data.model_dump(exclude_unset=True))

    with session_maker() as session:
        update_ecp_stmt = (
            update(KriptosORM).
            filter_by(id=kriptopro_id, employees_id=employees_id).
            values(**kriptopro_data.model_dump(exclude_unset=True))
        )

        session.execute(update_ecp_stmt)
        session.commit()
        return {"status": "ok"}


def delete_kriptopro(
    employees_id: int,
    kriptopro_id: int
):
    with session_maker() as session:
        ecp_delete_stmt = (delete(KriptosORM).
                           filter_by(id=kriptopro_id, employees_id=employees_id)
                           .returning(KriptosORM))
        result = session.execute(ecp_delete_stmt)

        kripto = result.scalars().one()
        session.commit()

        return {"status": "ok", "ecp": kripto}
