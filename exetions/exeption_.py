class EmployeeNotFoundException(Exception):
    def __init__(self, full_name:str):
        super().__init__("Введите правильное имя сотрудника")
