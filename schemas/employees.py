from pydantic import BaseModel, Field

# схема для добавления сотрудника
class EmployeeAdd(BaseModel):
    full_name: str
    position: str
    com_name: str

# схема для DataMapper
class Employee(EmployeeAdd):
    id: int

# схема для полного изменения данных сотрудника
class EmployeePut(BaseModel):
    full_name: str
    position: str
    com_name: str


# схема для частичного изменения данных сотрудника
class EmployeePatch(BaseModel):
    full_name: str | None = Field(None)
    position: str | None = Field(None)
    com_name: str | None = Field(None)
