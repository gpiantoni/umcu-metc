#!/usr/bin/env python3

from xelo2.database.create import _drop_create_mysql, dedent, close_database
from PyQt5.QtSql import (
    QSqlQuery,
    QSqlDatabase,
    )

db_name = 'metc'
username = 'giovanni'
password = 'password'
CONNECTION_NAME = 'metc_database'


COLUMNS = [
    'subject_id',
    'informed_consent',
    'informed_consent_version',
    'signature_date',
    'LETTER',
    None,
    'agrees_to_highdensity',
    'clinical_data_for_research',
    'use_voice',
    'store_longer_than_15y',
    'data_sharing_institutes',
    'data_sharing_online',
    'can_be_contacted_again',
    'wants_update',
    'notes',
    ]


STATEMENTS = [
    """\
    CREATE TABLE subjects (
      id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
      code VARCHAR(256))""",
    """\
    CREATE TABLE protocols (
      id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
      subject_id INT NOT NULL,
      informed_consent ENUM ('clinical_request', '14-420_adults', '14-090_children', '07-260_bcipatients', '14-622_intraop', 'follow-up'),
      informed_consent_version TEXT,
      signature_date DATE,
      agrees_to_highdensity ENUM ('yes', 'no'),
      clinical_data_for_research ENUM ('yes', 'no'),
      use_voice ENUM ('yes', 'no'),
      store_longer_than_15y ENUM ('yes', 'no'),
      data_sharing_institutes ENUM ('yes', 'no'),
      data_sharing_online ENUM ('yes', 'no'),
      can_be_contacted_again ENUM ('yes', 'no'),
      wants_update ENUM ('yes', 'no'),
      notes TEXT,
      FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE)""",
    """\
    CREATE TABLE files (
      protocol_id INT NOT NULL,
      path TEXT,
      FOREIGN KEY (protocol_id) REFERENCES protocols (id) ON DELETE CASCADE)""",
    """\
    CREATE VIEW permissions AS
      SELECT code,
      informed_consent,
      informed_consent_version,
      signature_date,
      agrees_to_highdensity,
      clinical_data_for_research,
      use_voice,
      store_longer_than_15y,
      data_sharing_institutes,
      data_sharing_online,
      can_be_contacted_again,
      wants_update,
      notes
      FROM subjects
      JOIN protocols ON subject_id = subjects.id
      ORDER BY code""",  # TODO: sort by date, so that we can trust the results when reading multiple protocols
    ]


def main():
    db = QSqlDatabase.addDatabase('QMYSQL', CONNECTION_NAME)
    assert db.isValid()

    _drop_create_mysql(db_name, username, password)
    db.setHostName('127.0.0.1')
    db.setUserName(username)
    db.setPassword(password)

    db.setDatabaseName(str(db_name))
    db.open()

    for t in STATEMENTS:
        query = QSqlQuery(db)
        if not query.exec(dedent(t)):
            print(query.lastError().text())

    with open('permissions.tsv') as f:
        for line in f:
            info = [x.strip() for x in line.split('\t')]
            add_protocols_per_subject(db, info)

    close_database(db)


def add_subjects(db, code):
    query = QSqlQuery(db)
    query.prepare("INSERT INTO subjects (`code`) VALUES (:code)")
    query.bindValue(':code', code)
    if not query.exec():
        raise SyntaxError(query.lastError().text())

    return query.lastInsertId()


def add_protocols_per_subject(db, info):
    values = []
    columns = []
    for col, val in zip(COLUMNS, info):
        if col == 'subject_id':
            columns.append(col)
            values.append(add_subjects(db, val))
        elif col == 'LETTER':
            if val == 'NULL':
                followup_columns = False
            else:
                followup_columns = ['subject_id', 'informed_consent', 'informed_consent_version']
                followup_values = [values[0], 'follow-up', val]
        elif col is None:
            continue

        elif val != 'NULL':
            columns.append(col)
            values.append(val)

    _add_protocol(db, columns, values)
    if followup_columns:
        _add_protocol(db, followup_columns, followup_values)


def _add_protocol(db, columns, values):
    query = QSqlQuery(db)
    col_str = ', '.join(f'`{col}`' for col in columns)
    val_str = ', '.join(f':{col}' for col in columns)
    query.prepare(f"INSERT INTO protocols ({col_str}) VALUES ({val_str})")
    for col, val in zip(columns, values):
        query.bindValue(f':{col}', val)
    if not query.exec():
        raise SyntaxError(query.lastError().text())


if __name__ == '__main__':
    main()
