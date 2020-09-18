from PyQt5.QtSql import (
    QSqlDatabase,
    )

DB_TYPE = 'QMYSQL'
DB_NAME = 'metc'
USERNAME = 'giovanni'
PASSWORD = 'password'
CONNECTION_NAME = 'metc_database'


def db_open(db_name=DB_NAME):

    db = QSqlDatabase.addDatabase(DB_TYPE, CONNECTION_NAME)
    assert db.isValid()

    db.setHostName('127.0.0.1')
    db.setUserName(USERNAME)
    db.setPassword(PASSWORD)

    db.setDatabaseName(str(db_name))
    db.open()

    return db

def db_close():
    """We need to "del db" in the lower scope"""
    pass
