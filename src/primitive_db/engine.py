import shlex

import prompt

from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata


def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print(
        "<command> create_table <имя_таблицы> "
        "<столбец1:тип> <столбец2:тип> .. - создать таблицу"
    )
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    print_help()

    while True:
        metadata = load_metadata("db_meta.json")

        user_input = prompt.string("Введите команду: ")
        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Ошибка: Проверьте правильность кавычек.")
            continue
        if not args:
            continue
        command = args[0]
        if command == "help":
            if len(args) != 1:
                print("Некорректное количество аргументов.")
                continue
            print_help()

        elif command == "exit":
            if len(args) != 1:
                print("Некорректное количество аргументов.")
                continue
            break

        elif command == "list_tables":
            if len(args) != 1:
                print("Некорректное количество аргументов.")
                continue
            list_tables(metadata)

        elif command == "create_table":
            if len(args) < 3:
                print("Некорректное количество аргументов.")
                continue

            old_count = len(metadata)
            create_table(metadata, args[1], args[2:])
            if len(metadata) > old_count:
                save_metadata("db_meta.json", metadata)
                columns = metadata[args[1]]
                column_description = []
                for name, column_type in columns.items():
                    column_description.append(f"{name}:{column_type}")
                result = ", ".join(column_description)
                print(f'Таблица "{args[1]}" успешно создана со столбцами: {result}')

        elif command == "drop_table":
            if len(args) != 2:
                print("Некорректное количество аргументов.")
                continue
            tables_before_delete = len(metadata)
            drop_table(metadata, args[1])
            if len(metadata) < tables_before_delete:
                save_metadata("db_meta.json", metadata)
        else:
            print(f"Функции {command} нет. Попробуйте снова.")
