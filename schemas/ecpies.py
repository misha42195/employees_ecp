from datetime import date

from pydantic import BaseModel, Field

class EcpReqestAdd(BaseModel):
    type_ecp: str
    status_ecp: str
    install_location: str
    storage_location: str
    sbis: str
    chz: str
    diadok: str
    fns: str
    report: str
    fed_resours: str
    start_date: date
    finish_date: date



class EcpAdd(BaseModel):

    employees_id: int
    type_ecp: str
    status_ecp: str  # работает/отозван
    install_location: str | None = Field(None)
    storage_location: str | None = Field(None)
    sbis: str
    chz: str
    diadok: str
    fns: str
    report: str
    fed_resours: str
    start_date: date
    finish_date: date


class Ecp(BaseModel):
    id: int
    employees_id: int
    type_ecp: str
    status_ecp: str
    install_location: str
    storage_location: str
    sbis: str
    chz: str
    diadok: str
    fns: str
    report: str
    fed_resours: str
    start_date: date
    finish_date: date

class EcpPut(BaseModel):
    type_ecp: str
    status_ecp: str
    install_location: str
    storage_location: str
    sbis: str
    chz: str
    diadok: str
    fns: str
    report: str
    fed_resours: str
    start_date: date
    finish_date: date

class EcpPatch(BaseModel):
    type_ecp: str|None = None
    status_ecp: str|None = None
    install_location: str|None = None
    storage_location: str|None = None
    sbis: str|None = None
    chz: str|None = None
    diadok: str|None = None
    fns: str|None = None
    report: str|None = None
    fed_resours: str|None = None
    start_date: date|None = None
    finish_date: date|None = None
