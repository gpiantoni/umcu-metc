#!/usr/bin/env python3

from sys import argv
from PyQt5.QtCore import QVariant
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

    output = {
        'informed_consent': None,
        'informed_consent_version': None,
        'signature_date': None,
        'agrees_to_highdensity': None,
        'clinical_data_for_research': None,
        'use_voice': None,
        'store_longer_than_15y': None,
        'data_sharing_institutes': None,
        'data_sharing_online': None,
        'can_be_contacted_again': None,
        'wants_update': None,
        'notes': None,
        }

    query = QSqlQuery(db)
    query.prepare("SELECT * FROM permissions WHERE code = :code ")
    query.bindValue(':code', subject)
    if not query.exec():
        raise SyntaxError(query.lastError().text())

    while query.next():
        for k in output:
            out = query.value(k)
            if not out.isNull():
                output[k] = out.value()

    print(f'Permissions for {subject}')
    for k, v in output.items():
        if v is None:
            v = '(unknown)'
        print(f"{k.replace('_', ' '):<30} {v:>20}")


if __name__ == '__main__':
    main(argv[1])
