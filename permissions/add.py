from pathlib import Path

from PyQt5.QtSql import QSqlDatabase

from .api import (
    select,
    insert,
    )
from .utils import (
    db_open,
    CONNECTION_NAME,
    )


def add_rows():
    db = db_open()

    db.transaction()
    try:
        tsv_file = Path('/home/gio/projects/metc/changes_in_state_of_permissions.tsv')
        add_row_from_file(db, tsv_file)
    except Exception as err:
        db.rollback()
        raise(err)
    else:
        db.commit()

    db.close()
    del db  # delete database before removing connection
    QSqlDatabase.removeDatabase(CONNECTION_NAME)


def add_row_from_file(db, tsv_file):
    with tsv_file.open() as f:
        hdr = [x.strip() for x in f.readline().split()]

        for row in f:
            val = [x.strip() for x in row.split('\t')]

            keys = {}
            for k, v in zip(hdr, val):
                if len(v) == 0:
                    continue

                if k == 'protocol':
                    keys['protocol_id'] = select(db, 'protocols', {'protocol': v})

                elif k == 'experimenter':
                    keys['experimenter_id'] = select(db, 'experimenters', {'experimenter': v})

                else:
                    keys[k] = v

            insert(db, 'changes', keys)

    return
