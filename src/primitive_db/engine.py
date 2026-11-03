import shlex

import prompt

from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata


def welcome():
    print("Первая попытка запустить проект!")
    print_help()

    while True:
        user_input = prompt.string("Введите команду: ")
        args = shlex.split(user_input)
        if not args:
            continue
        command = args[0]
        if command == "help":
            print_help()

        elif command == "exit":
            break

        elif command == "list_tables":
            metadata = load_metadata("db_meta.json")
            list_tables(metadata)

        elif command == "create_table":
            if len(args) < 3:
                print("Некорректное количество аргументов.")
                continue
            metadata = load_metadata("db_meta.json")
            old_count = len(metadata)
            create_table(metadata, args[1], args[2:])
            if len(metadata) > old_count:
                save_metadata("db_meta.json", metadata)
                print(f'Таблица "{args[1]}" успешно создана.')

        elif command == "drop_table":
            if len(args) != 2:
                print("Некорректное количество аргументов.")
                continue
            metadata = load_metadata("db_meta.json")
            tables_before_delete = len(metadata)
            drop_table(metadata, args[1])
            if len(metadata) < tables_before_delete:
                save_metadata("db_meta.json", metadata)


def print_help():
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> create_table - создать таблицу")
    print("<command> drop_table - удалить таблицу")
