from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


from database import Base

class EmployeesORM(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(100), unique=True)
    position: Mapped[str] = mapped_column(String(100))
    com_name: Mapped[str] = mapped_column(String(100))
