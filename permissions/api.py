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


def list_columns(db, table):
    query = QSqlQuery(db)
    query.prepare(f"DESCRIBE {table}")
    if not query.exec():
        raise SyntaxError(query.lastError().text())

    cols = []
    while query.next():
        cols.append(query.value(0).value())

    return cols


def find_aliases(db, code):
    query = QSqlQuery(db)
    query.prepare('SELECT code FROM aliases WHERE person = (SELECT person FROM aliases WHERE code = :code) ORDER BY code')
    query.bindValue(':code', code)

    if not query.exec():
        raise SyntaxError(query.lastError().text())

    codes = []
    while query.next():
        codes.append(query.value('code').value())

    return codes
