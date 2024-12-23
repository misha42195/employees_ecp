from datetime import date

from pydantic import BaseModel


class KriptoproRequestAdd(BaseModel):
    install_location: str
    licens_type: str
    start_date: date
    finish_date: date


class KriptoproAdd(BaseModel):
    employees_id: int
    install_location: str
    licens_type: str
    start_date: date
    finish_date: date


class KriptoproPut(BaseModel):
    install_location: str
    licens_type: str
    start_date: date
    finish_date: date


class KriptoproPath(BaseModel):
    install_location: str
    licens_type: str
    start_date: date
    finish_date: date
