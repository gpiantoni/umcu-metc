#!/usr/bin/env python3

from xelo2.database.create import close_database
from PyQt5.QtSql import (
    QSqlQuery,
    QSqlDatabase,
    )

db_type = 'QMYSQL'
db_name = 'metc'
username = 'giovanni'
password = 'password'
CONNECTION_NAME = 'metc_database'


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


def main():
    db = QSqlDatabase.addDatabase(db_type, CONNECTION_NAME)
    assert db.isValid()

    db.setHostName('127.0.0.1')
    db.setUserName(username)
    if password is not None:
        db.setPassword(password)

    db.setDatabaseName(str(db_name))
    db.open()

    add_rows(db)

    close_database(db)


def add_rows(db):
    """
    case 1
    clinical subject, retrospective call to use clinical data, nonWMO retrospective letter for sharing data
    laan, wolf, vref, brin
    """
    pt_idx = insert(db, 'patients', {'code': 'laan'})
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'letter',
        'protocol_id': select(db, 'protocols', {'protocol': 'ORCHIID'}),
        'date': '2020-08-02',
        'protocol_version': 'C1.0 22-Jun-2020',
        'medical_data_for_research': 'yes',
        'use_voice': 'yes',
        'store_longer_than_15y': 'yes',
        'data_sharing_institutes': 'yes',
        'data_sharing_online': 'yes',
        })

    """
    case 2
    protocol subject, retrospective call/letter to use clinical data and share data
    muiden/zeist/delft
    """
    pt_idx = insert(db, 'patients', {'code': 'muiden'})
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'in person',
        'protocol_id': select(db, 'protocols', {'protocol': '14-090_children'}),
        'experimenter_id': select(db, 'experimenters', {'experimenter': 'Mariska'}),
        'date': '2016-08-14',
        'protocol_version': '2-090514',
        'can_be_contacted_again': 'yes',
        'wants_update': 'yes',
        })
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'letter',
        'date': '2020-07-30',
        'protocol_id': select(db, 'protocols', {'protocol': 'ORCHIID'}),
        'protocol_version': 'A_B1.1 24-Jul-2020',
        'medical_data_for_research': 'yes',
        'store_longer_than_15y': 'yes',
        'data_sharing_institutes': 'yes',
        'data_sharing_online': 'yes',
        })

    """
    case 3
    protocol subject, retrospective call to share data, and later retrospective letter to use medical data and public sharing
    habe/simo/mels
    """
    pt_idx = insert(db, 'patients', {'code': 'habe'})
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'in person',
        'protocol_id': select(db, 'protocols', {'protocol': '07-260_bcipatients'}),
        'experimenter_id': select(db, 'experimenters', {'experimenter': 'Mariska'}),
        'date': '2010-01-22',
        'protocol_version': 'V2, 19-10-2007',
        'medical_data_for_research': 'yes',
        'data_sharing_institutes': 'yes',
        'can_be_contacted_again': 'yes',
        'agrees_to_highdensity': 'yes',
        })
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'letter',
        'date': '2020-07-30',
        'protocol_version': 'V1 12-3-2020',
        'data_sharing_online': 'yes',
        })
    """
    case 4
    clinical subject, nWMO letter to use data and sharing data
    ahma/grie/verh
    """
    pt_idx = insert(db, 'patients', {'code': 'grie'})
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'letter',
        'protocol_id': select(db, 'protocols', {'protocol': 'ORCHIID'}),
        'date': '2020-08-02',
        'protocol_version': 'D_E1.0 22-Jun-2020',
        'medical_data_for_research': 'yes',
        'data_sharing_institutes': 'yes',
        'use_voice': 'yes',
        'data_sharing_online': 'yes',
        })

    """
    case 5
    recorrent patients who signed several protocols
    gennep (guij)
    """
    pt_idx = insert(db, 'patients', {'code': 'gennep'})
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'in person',
        'protocol_id': select(db, 'protocols', {'protocol': '07-260_bcipatients'}),
        'experimenter_id': select(db, 'experimenters', {'experimenter': 'Mariska'}),
        'date': '2012-05-08',
        'protocol_version': 'V2 19-10-2007',
        'medical_data_for_research': 'yes',
        'can_be_contacted_again': 'yes',
        })
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'in person',
        'protocol_id': select(db, 'protocols', {'protocol': '14-420_adults'}),
        'experimenter_id': select(db, 'experimenters', {'experimenter': 'Mariska'}),
        'date': '2016-03-14',
        'protocol_version': '2-28082014',
        'can_be_contacted_again': 'yes',
        'agrees_to_highdensity': 'yes',
        })
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'phone',
        'date': '2019-03-19',  # maybe
        })
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'phone',
        'date': '2019-07-15',  # maybe
        'data_sharing_institutes': 'yes',
        })
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'letter',
        'date': '2020-03-19',
        'protocol_version': 'V1 12-3-2020',
        'data_sharing_institutes': 'yes',
        'use_voice': 'yes',
        'data_sharing_online': 'yes',
        })

    """
    case 6
    protocol subject, who gave permission, but has passed away meanwhile: we can access all data
    groe
    """
    pt_idx = insert(db, 'patients', {'code': 'groe'})
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'in person',
        'protocol_id': select(db, 'protocols', {'protocol': '07-260_bcipatients'}),
        'experimenter_id': select(db, 'experimenters', {'experimenter': 'Mariska'}),
        'date': '2010-01-08',
        'protocol_version': 'V2 19-10-2007',
        'medical_data_for_research': 'yes',
        'can_be_contacted_again': 'yes',
        })
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'death',
        'date': '2050-01-01',
        'use_voice': 'yes',
        'data_sharing_institutes': 'yes',
        'data_sharing_online': 'yes',
        'store_longer_than_15y': 'yes',
        })

    """
    case 7
    patient gave consent first then took it back
    franeker
    """
    pt_idx = insert(db, 'patients', {'code': 'franeker'})
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'in person',
        'protocol_id': select(db, 'protocols', {'protocol': '14-420_adults'}),
        'experimenter_id': select(db, 'experimenters', {'experimenter': 'Elmar'}),
        'date': '2018-02-15',
        'protocol_version': '6-191017',
        'medical_data_for_research': 'yes',
        'data_sharing_institutes': 'yes',
        'agrees_to_highdensity': 'yes',
        'can_be_contacted_again': 'no',
        })
    insert(db, 'interactions', {
        'patient_id': pt_idx,
        'type': 'phone',
        'date': '2020-01-01',
        'data_sharing_online': 'no',
        })


if __name__ == '__main__':
    main()
