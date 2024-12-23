from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class EmployeesORM(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(100), unique=True)
    position: Mapped[str] = mapped_column(String(100))
    com_name: Mapped[str] = mapped_column(String(100))


    # Связь с таблицей EcpORM (один ко многим)
    ecp = relationship("EcpORM", back_populates="employee", cascade="all, delete-orphan")

    # Связь с таблицей KriptosORM (один ко многим)
    kriptos = relationship("KriptosORM", back_populates="employee", cascade="all, delete-orphan")
