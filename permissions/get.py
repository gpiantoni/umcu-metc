from collections import defaultdict

from PyQt5.QtCore import (
    QVariant,
    QDate,
    )
from PyQt5.QtSql import (
    QSqlQuery,
    QSqlDatabase
    )
import sip

from .api import list_columns, find_aliases
from .utils import db_open, CONNECTION_NAME


sip.enableautoconversion(QVariant, False)
PLACEHOLDER = '-'


def get(code, username=None):
    db = db_open(username=username)

    aliases = find_aliases(db, code)
    if len(aliases) > 1:
        print('\nThis patient has multiple codes: ' + ', '.join(aliases))

    output = get_all_changes(db, code)
    if output is None:
        print(f'\nNo permissions found for {code}\n')

    else:
        outcome = parse_outcome(output)
        files = get_files(db, code)

        print(f'\nPERMISSIONS FOR {code}')
        print_permissions(output, outcome)
        print_notes(output)
        print_files(files)

    db.close()
    del db  # delete database before removing connection
    QSqlDatabase.removeDatabase(CONNECTION_NAME)


def get_all_changes(db, code):
    """

    Returns
    -------
    dict
        where keys are the columns and the values are a list with the
        values for each interaction. It returns None, when the code is not found
    """
    cols = list_columns(db, 'permissions')
    cols.remove('patient')

    query = QSqlQuery(db)
    query.prepare("SELECT * FROM permissions WHERE patient = :code ")
    query.bindValue(':code', code)
    if not query.exec():
        raise SyntaxError(query.lastError().text())

    output = defaultdict(list)
    while query.next():

        for k in cols:
            out = query.value(k)
            if out.isNull():
                v = PLACEHOLDER
            elif isinstance(out.value(), QDate):
                v = out.value().toString('d MMMM yyyy')
            else:
                v = out.value()

            output[k].append(v)

    if len(output) == 0:
        return None
    else:
        return output

def parse_outcome(output):

    outcome = {}
    for k, v in output.items():
        if k in ('date', 'type', 'period', 'experimenter', 'protocol', 'version', 'notes'):
            out = ''  # these columns do not contain permissions
        else:

            l_out = [x for x in v if x not in (PLACEHOLDER, )]
            if len(l_out) >= 1:
                out = l_out[-1]
            else:
                out = PLACEHOLDER

        outcome[k] = out
    return outcome


def get_files(db, code):
    query = QSqlQuery(db)
    query.prepare("SELECT path FROM files JOIN changes ON files.change_id = changes.id WHERE code = :code ")
    query.bindValue(':code', code)
    if not query.exec():
        raise SyntaxError(query.lastError().text())

    files = []
    while query.next():
        files.append(query.value('path').value())

    return files


def print_permissions(output, outcome):

    n_changes = len(output[next(iter(output))])
    sources = [f"({i + 1})" for i in range(n_changes)]
    sources = ''.join(f"{i:>20}" for i in sources)
    print(f"{'':<30}{'':>20}|{sources}")

    for k, val in output.items():
        if k == 'notes':
            continue

        values_str = ''.join(f'{v:>20}' for v in val)
        print(f"{k:<30}{outcome[k]:<20}|{values_str}")


def print_notes(output):
    print('\nNOTES')
    for i, n in enumerate(output['notes']):
        if n == PLACEHOLDER:
            continue
        print(f'  ({i + 1}) : {n}')


def print_files(files):
    if len(files) > 0:
        print('\nFILES')
    for v in files:
        print(f'  - {v}')
    print('')
