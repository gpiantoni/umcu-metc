from PyQt5.QtSql import (
    QSqlDatabase,
    )
from getpass import getuser, getpass

DB_TYPE = 'QMYSQL'
DB_NAME = 'metc'
CONNECTION_NAME = 'metc_database'


def db_open(db_name=DB_NAME, username=None, password=None):

    db = QSqlDatabase.addDatabase(DB_TYPE, CONNECTION_NAME)
    assert db.isValid()

    db.setHostName('127.0.0.1')
    if password is None:
        username, password = get_auth(username)

    db.setUserName(username)
    db.setPassword(password)

    db.setDatabaseName(str(db_name))
    db.open()
    if not db.isOpen():
        raise ValueError('could not connect to database')

    return db


def get_auth(username=None):
    if username is None:
        username = getuser()
    password = getpass(f'Type password for `{username}` on SQL server (it might be different from the password on RIBS): ')
    return username, password


def db_close():
    """We need to "del db" in the lower scope"""
    pass
