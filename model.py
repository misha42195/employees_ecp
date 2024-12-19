

from sqlmodel import SQLModel, create_engine, Field, Session, select
from typing import Optional, List
from datetime import date



# Class for ECP
class ECP(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    type_ecp: str = Field(nullable=False)  # Тип контейнера (токен/реестр)
    status_ecp: str = Field(nullable=False)  # Статус (работает/отозван)
    install_location: str = Field(nullable=False)  # Место установки
    storage_location: str = Field(nullable=False)  # Где хранится
    sbis: str = Field(nullable=False)  # Применим к СБИС (да/нет)
    CHZ: str = Field(nullable=False)  # Применим к ЧЗ (да/нет)
    diadok: str = Field(nullable=False)  # Применим к Диадок (да/нет)
    FNS: str = Field(nullable=False)  # Применим к ФНС (да/нет)
    report: str = Field(nullable=False)  # Применим к отчетности (да/нет)
    fed_resours: str = Field(nullable=False)  # Применим к фед. ресурсу (да/нет)
    start_date: date = Field(nullable=False)  # Дата начала лицензии
    finish_date: date = Field(nullable=False)  # Дата окончания лицензии

# Class for KriptoPro
class KriptoPro(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    install_location: str = Field(nullable=False)  # Место установки
    licens_type: str = Field(nullable=False)  # Тип лицензии
    start_date: date = Field(nullable=False)  # Дата начала лицензии
    finish_date: date = Field(nullable=False)  # Дата окончания лицензии

# Class for Employee
class Employee(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    full_name: str = Field(nullable=False)  # ФИО
    position: str = Field(nullable=False)  # Должность
    com_name: str = Field(nullable=False)  # Имя компьютера

# CRUD Operations
def create_tables():
    SQLModel.metadata.create_all(engine)

def add_instance(instance):
    with Session(engine) as session:
        session.add(instance)
        session.commit()
        return True

def update_instance(model, id, **kwargs):
    with Session(engine) as session:
        statement = select(model).where(model.id == id)
        result = session.exec(statement).first()
        if not result:
            return False
        for key, value in kwargs.items():
            setattr(result, key, value)
        session.add(result)
        session.commit()
        return True

def get_all_instances(model):
    with Session(engine) as session:
        statement = select(model)
        results = session.exec(statement)
        return results.all()

def get_instance_by_id(model, id):
    with Session(engine) as session:
        statement = select(model).where(model.id == id)
        result = session.exec(statement).first()
        return result

def delete_instance(model, id):
    with Session(engine) as session:
        statement = select(model).where(model.id == id)
        result = session.exec(statement).first()
        if not result:
            return False
        session.delete(result)
        session.commit()
        return True

def create_tables():
    SQLModel.metadata.create_all(engine)
