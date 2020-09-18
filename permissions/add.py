from PyQt5.QtSql import QSqlDatabase

from .api import (
    select,
    insert,
    )
from .utils import (
    db_open,
    CONNECTION_NAME,
    )


def add_rows(tsv_file, username=None):
    db = db_open(username=username)

    db.transaction()
    try:
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
            files = None
            for k, v in zip(hdr, val):
                if len(v) == 0:
                    continue

                if k == 'protocol':
                    keys['protocol_id'] = select(db, 'protocols', {'protocol': v})

                elif k == 'experimenter':
                    keys['experimenter_id'] = select(db, 'experimenters', {'experimenter': v})

                elif k == 'files':
                    files = v

                else:
                    keys[k] = v

            change_id = insert(db, 'changes', keys)
            if files is not None:
                for f in files.split(';'):
                    if len(f.strip()) == 0:  # handle case "path1;path2;"
                        continue
                    insert(db, 'files', {'change_id': change_id, 'path': f.strip()})
