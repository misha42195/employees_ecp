from typing import Annotated
from fastapi import Query, Depends
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Номер страницы")]
    per_page: Annotated[int | None, Query(5, ge=1, le=10, description="Кол-во сотрудников")]


PaginationDep = Annotated[PaginationParams, Depends()]
