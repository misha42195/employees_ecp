class EmployeeNotFoundException(Exception):
    def __init__(self, employee_id: int):
        super().__init__(
            status_code=404,
            detail=f"Сотрудник с ID {employee_id} не найден"
        )
