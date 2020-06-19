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
    assert db.isOpen()

    output = {
        'document': [],
        'informed_consent': [],
        'informed_consent_version': [],
        'signature_date': [],
        'agrees_to_highdensity': [],
        'clinical_data_for_research': [],
        'use_voice': [],
        'store_longer_than_15y': [],
        'data_sharing_institutes': [],
        'data_sharing_online': [],
        'can_be_contacted_again': [],
        'wants_update': [],
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

    print(f'\nPERMISSIONS FOR {subject}\n')
    for k, values in output.items():
        if k == 'notes':
            continue
        values_str = ''.join(f'{v:>20}' for v in values)
        print(f"{k.replace('_', ' '):<30} {values_str}")

    if any([n != '(unknown)' for n in output['notes']]):
        print('\nNOTES')
    for i, n in zip(output['document'], output['notes']):
        if n == '(unknown)':
            continue
        else:
            print(f'{i:<10}: {n}')

    query = QSqlQuery(db)
    query.prepare("SELECT path FROM files JOIN protocols ON files.protocol_id = protocols.id JOIN subjects ON subjects.id = protocols.subject_id WHERE subjects.code = :code ")
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
