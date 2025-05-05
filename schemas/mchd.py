from datetime import date

from pydantic import BaseModel


class MchdAdd(BaseModel):
    employees_id: int
    organiazation_dov_num: str
    fns_dov_num: str
    start_date: date
    finish_date: date
    file_mchd: bytes
    file_csp: bytes | None = None
    name_of_powers: str
