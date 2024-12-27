from datetime import datetime

from crud.employees import get_employees_with_expiring_licenses



def create_notification():
    employees_with_objects = get_employees_with_expiring_licenses()
    print(f"данные {employees_with_objects}")
    if not employees_with_objects:
        return None
    # Формируем сообщения
    messages = []
    for employee, ecps, kriptos in employees_with_objects:
        employee_message = [f"🔴⚠️Сотрудник: {employee.full_name}"]

        for ecp in ecps:
            days_left = (ecp.finish_date - datetime.now().date()).days
            employee_message.append(
                f"  ECP заканчивается: {ecp.finish_date.strftime('%Y-%m-%d')}, осталось {days_left} дней"
            )

        for kripto in kriptos:
            days_left = (kripto.finish_date - datetime.now().date()).days
            employee_message.append(
                f"  Kriptos заканчивается: {kripto.finish_date.strftime('%Y-%m-%d')}, осталось {days_left} дней"
            )

        messages.append("\n".join(employee_message))

    # Объединяем все сообщения в одно
    return "\n\n".join(messages)
