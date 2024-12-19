
from sqlalchemy import String, Column, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from datetime import date
from database import Base

class KriptosORM(Base):
    __tablename__ = 'kriptos'
    id: Mapped[int] = mapped_column(primary_key=True)
    employees_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    install_location: Mapped[str] = mapped_column(String)
    licens_type: Mapped[str] = mapped_column(String)
    start_date: Mapped[date] = mapped_column()
    finish_date: Mapped[date] = mapped_column()
