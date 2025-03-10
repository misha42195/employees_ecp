
from sqlalchemy import String, ForeignKey, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date
from database import Base

class KriptosORM(Base):
    __tablename__ = 'kriptos'
    id: Mapped[int] = mapped_column(primary_key=True)
    employees_id: Mapped[int] = mapped_column(ForeignKey("employees.id",ondelete="CASCADE"))
    install_location: Mapped[str] = mapped_column(String)
    licens_type: Mapped[str] = mapped_column(String) # должно быть comp_name - имя компьютера
    version: Mapped[str] = mapped_column(Integer)
    start_date: Mapped[date] = mapped_column(Date)
    finish_date: Mapped[date] = mapped_column(Date)

    # Обратная связь с EmployeesORM
    employee = relationship("EmployeesORM", back_populates="kriptos")
