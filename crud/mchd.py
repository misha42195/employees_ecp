from unittest import result
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import joinedload
from crud.ecpies import engine
from models.mchd import MchdORM
from schemas.mchd import MchdAdd
from database import session_maker


def create_mchd(mchd_data: MchdAdd):
    with session_maker() as session:
        mchd_data_stmt = (
            insert(MchdORM)
            .values(**mchd_data.model_dump())
            .returning(MchdORM.fns_dov_num)
        )
        # print(mchd_data_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = session.execute(mchd_data_stmt)
        mchd = result.scalars().one()
        session.commit()
        return mchd

def delete_mchd(mchd_id: int):
    with session_maker() as session:
        mchd_delete_stmt = delete(MchdORM).filter_by(id=mchd_id).returning(MchdORM)
        result = session.execute(mchd_delete_stmt)

        kpr = result.scalars().one()
        session.commit()

        return kpr


def get_xml_from_db(record_id):
    with session_maker() as session:
        mchd_file_stmt = select(MchdORM).filter_by(id=record_id)
        result = session.execute(mchd_file_stmt)
        mchd = result.scalars().one()

        return mchd
