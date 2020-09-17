#!/usr/bin/env python3

from sys import argv
from PyQt5.QtCore import (
    QVariant,
    QDate,
    )
from PyQt5.QtSql import (
    QSqlQuery,
    QSqlDatabase
    )
import sip

db_name = 'metc'
username = 'giovanni'
password = 'password'
CONNECTION_NAME = 'metc_database'

sip.enableautoconversion(QVariant, False)


def main(subject):

    db = QSqlDatabase.addDatabase('QMYSQL', CONNECTION_NAME)
    assert db.isValid()

    db.setHostName('127.0.0.1')
    db.setUserName(username)
    db.setPassword(password)

    db.setDatabaseName(str(db_name))
    db.open()
    if not db.isOpen():
        raise ValueError('could not connect to database')

    output = {
        'document': [],
        'date': [],
        'type': [],
        'protocol': [],
        'version': [],
        'HD': [],
        'use of medical data': [],
        'voice': [],
        'longer than 15y': [],
        'share with institutes': [],
        'share online': [],
        'further contact': [],
        'updates': [],
        'notes': [],
        }

    query = QSqlQuery(db)
    query.prepare("SELECT * FROM permissions WHERE code = :code ")
    query.bindValue(':code', subject)
    if not query.exec():
        raise SyntaxError(query.lastError().text())

    i = 1
    while query.next():

        for k in output:
            if k == 'document':
                v = f'({i})'
                i += 1

            else:

                out = query.value(k)
                if out.isNull():
                    v = '(unknown)'
                elif isinstance(out.value(), QDate):
                    v = out.value().toString('d MMMM yyyy')
                else:
                    v = out.value()

            output[k].append(v)

    for k, out in output.items():
        out.insert(0, '|')
        if k in ('document', 'date', 'protocol', 'version', 'type'):
            out.insert(0, '')
            continue

        l_out = [x for x in out if x not in ('(unknown)', '', '|')]
        if len(l_out) >= 1:
            out.insert(0, l_out[-1])
        else:
            out.insert(0, '(unknown)')

    print(f'\nPERMISSIONS FOR {subject}\n')
    for k, values in output.items():
        if k == 'notes':
            continue
        values_str = ''.join(f'{v:>20}' for v in values)
        print(f"{k.replace('_', ' '):<30} {values_str}")

    query = QSqlQuery(db)
    query.prepare("SELECT path FROM files JOIN interactions ON files.interaction_id = interactions.id JOIN patients ON patients.id = interactions.patient_id WHERE patients.code = :code ")
    query.bindValue(':code', subject)
    if not query.exec():
        raise SyntaxError(query.lastError().text())

    files = []
    while query.next():
        files.append(query.value('path').value())

    if len(files) > 0:
        print('\nFILES')
    for v in files:
        print(f'{v}')

    print('')


if __name__ == '__main__':
    main(argv[1])
