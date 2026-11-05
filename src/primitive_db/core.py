from .utils import load_table_data


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


def insert(metadata, table_name, values):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    expected_values = len(metadata[table_name]) - 1
    if expected_values != len(values):
        print(f"Ошибка: Ожидалось {expected_values} значения, получено {len(values)}")
        return None

    columns = list(metadata[table_name].items())[1:]
    type_map = {
        "int": int,
        "str": str,
        "bool": bool,
    }
    for (name, column_type), value in zip(columns, values):
        expected_type = type_map[column_type]
        if type(value) is not expected_type:
            print(f"Некорректное значение: {value}. Попробуйте снова.")
            return None
    table_data = load_table_data(table_name)
    new_id = max((row["ID"] for row in table_data), default=0) + 1
    new_record = {"ID": new_id}
    for (name, _), value in zip(columns, values):
        new_record[name] = value
    table_data.append(new_record)
    return table_data


def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data

    column, value = next(iter(where_clause.items()))
    result = []

    for row in table_data:
        if row.get(column) == value:
            result.append(row)

    return result


def update(table_data, set_clause, where_clause):
    set_column, new_value = next(iter(set_clause.items()))
    where_column, where_value = next(iter(where_clause.items()))

    for row in table_data:
        if row.get(where_column) == where_value:
            row[set_column] = new_value

    return table_data


def delete(table_data, where_clause):
    column, value = next(iter(where_clause.items()))

    result = []

    for row in table_data:
        if row.get(column) != value:
            result.append(row)

    return result
