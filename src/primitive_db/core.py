def create_table(metadata, table_name, columns):
    table_name = table_name.strip()
    if not table_name:
        print("Ошибка: Название таблицы не может быть пустым.")
        return metadata
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = {"ID": "int"}
    valid_types = ("int", "str", "bool")
    used_columns = []
    for data in columns:
        if data.count(":") != 1:
            print("Ошибка: Некорректный формат данных.")
            return metadata
        column_name, column_type = data.split(":")
        column_name = column_name.strip()
        if not column_name:
            print("Ошибка: Название столбца не может быть пустым.")
            return metadata
        if column_name in used_columns:
            print("Ошибка: Название столбца не может повторяться.")
            return metadata
        if column_type not in valid_types:
            print(f"Некорректное значение: {column_type}. Попробуйте снова.")
            return metadata
        if column_name == "ID" and column_type != "int":
            print("Ошибка: Столбец ID должен иметь тип int.")
            return metadata

        used_columns.append(column_name)

        table_columns[column_name] = column_type
    metadata[table_name] = table_columns
    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def list_tables(metadata):
    if not metadata:
        print("В базе данных пока нет таблиц.")
        return
    for table_name in metadata:
        print(f"- {table_name}")
