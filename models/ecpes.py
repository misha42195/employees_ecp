from sqlalchemy import String, Column, DateTime, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date

from database import Base


class EcpORM(Base):
    __tablename__ = 'ecp'

    id: Mapped[int] = mapped_column(primary_key=True)
    employees_id: Mapped[int] = mapped_column(ForeignKey("employees.id",ondelete="CASCADE"))
    type_ecp: Mapped[str] = mapped_column(String)  # Тип контейнера (токен/реестр)
    status_ecp: Mapped[str] = mapped_column(String)  # Статус (работает/отозван)
    install_location: Mapped[str] = mapped_column(String)  # Место установки
    storage_location: Mapped[str] = mapped_column(String)  # Где хранится
    sbis: Mapped[str] = mapped_column(String)  # Применим к СБИС (да/нет)
    chz: Mapped[str] = mapped_column(String)  # применим к ЧЗ (да/нет)
    diadok: Mapped[str] = mapped_column(String)  # Применим к Диадок (да/нет)
    fns: Mapped[str] = mapped_column(String)  # Применим к ФНС (да/нет)
    report: Mapped[str] = mapped_column(String)  # Применим к отчетности (да/нет)
    fed_resours: Mapped[str] = mapped_column(String)  # Применим к фед. ресурсу (да/нет)
    start_date: Mapped[date] = mapped_column(Date)  # начала лицензии
    finish_date: Mapped[date] = mapped_column(Date)  # окончания лицензии

# Обратная связь с EmployeesORM
    employee = relationship("EmployeesORM", back_populates="ecp")
