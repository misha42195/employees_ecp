from sqlalchemy import Integer, LargeBinary, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class MchdORM(Base):
    __tablename__ = "mchd"

    id: Mapped[int] = mapped_column(primary_key=True)
    employees_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE")
    )
    organiazation_dov_num: Mapped[int] = mapped_column(
        Integer
    )  # номер доверенноси организации <>
    fns_dov_num: Mapped[str] = mapped_column(String)  # номера доверенности в ФНС
    start_date: Mapped[Date] = mapped_column(Date)  # дата начала
    finish_date: Mapped[Date] = mapped_column(Date)  # дата завершения
    file_mchd: Mapped[bytes] = mapped_column(LargeBinary)  # файл мчд
    file_csp: Mapped[bytes] = mapped_column(
        LargeBinary, nullable=True
    )  # файл для подписки
    name_of_powers: Mapped[str] = mapped_column(String)  # наименование полном.

    # обратная связь с EmployeesORM
    employee = relationship("EmployeesORM", back_populates="mchd")
