from PyQt5.QtSql import QSqlQuery


def select(db, table, values):
    query = QSqlQuery(db)
    col, val = list(values.items())[0]
    query.prepare(f"SELECT id FROM `{table}` WHERE `{col}` = '{val}'")
    if not query.exec():
        raise SyntaxError(query.lastError().text())

    if query.next():
        return query.value('id')


def insert(db, table, values):
    query = QSqlQuery(db)
    col_str = ', '.join(f'`{col}`' for col in values)
    val_str = ', '.join(f':{col}' for col in values)
    query.prepare(f"INSERT INTO {table} ({col_str}) VALUES ({val_str})")
    for col, val in values.items():
        query.bindValue(f':{col}', val)
    if not query.exec():
        raise SyntaxError(query.lastError().text())

    return query.lastInsertId()
