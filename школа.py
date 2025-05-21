
available_classes = [f'{i}{letter}' for i in range(1, 12) for letter in ['A', 'B', 'C']]
closed_classes = []
students = {}


def add_student(name, clas):
    students[name] = clas
    if clas in available_classes:
        available_classes.remove(clas)
        closed_classes.append(clas)


def remove_student(name):
    if name in students:
        clas = students[name]
        students.pop(name)

        if clas not in students.values():
            closed_classes.remove(clas)
            available_classes.append(clas)


def list_classes():
    return sorted(closed_classes)


def list_students():
    return sorted(students)


while True:
    admin = input('Выберите действие (добавить / удалить / классы / ученики): ').lower()

    if admin.lower() == 'добавить':
        student_name = input('Введите имя ученика: ')
        print('Доступные классы:', sorted(available_classes))
        student_class = input('Выберите класс (например 5A): ')
        if student_class in available_classes:
            add_student(student_name, student_class)
            print('Ученик добавлен успешно!')
        else:
            print('Такого класса нет или он уже занят!')

    elif admin.lower() == 'удалить':
        student_name = input('Введите имя ученика: ')
        if student_name in students:
            remove_student(student_name)
            print('Ученик успешно удален!')
        else:
            print('Ученик не найден!')

    elif admin.lower() == 'классы':
        print('Список занятых классов:', list_classes())

    elif admin.lower() == 'ученики':
        print('Список учеников:', list_students())

    else:
        print('Неизвестная операция!')
