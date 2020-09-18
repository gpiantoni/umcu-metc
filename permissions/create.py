from textwrap import dedent

from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlQuery,
    )

from .utils import (
    db_open,
    DB_NAME,
    CONNECTION_NAME,
    )

from .api import insert


STATEMENTS_DB = [
    """DROP DATABASE IF EXISTS metc;""",
    """CREATE DATABASE metc;""",
    ]

STATEMENTS_TABLES = [
    """\
    CREATE TABLE experimenters (
      id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
      experimenter VARCHAR(256))""",
    """\
    CREATE TABLE protocols (
      id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
      protocol VARCHAR(256))""",
    """\
    CREATE TABLE changes (
      id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
      code VARCHAR(256) NOT NULL,
      date DATE,
      type ENUM ('informed consent', 'letter', 'email', 'phone', 'unresponsive', 'death') NOT NULL,
      period ENUM ('original', 'retrospective') NOT NULL,
      protocol_id INT,
      version TEXT,
      experimenter_id INT,
      agrees_to_highdensity ENUM ('yes', 'no'),
      medical_data_for_research ENUM ('yes', 'no'),
      use_voice ENUM ('yes', 'no'),
      store_longer_than_15y ENUM ('yes', 'no'),
      data_sharing_institutes ENUM ('yes', 'no'),
      data_sharing_online ENUM ('yes', 'no'),
      can_be_contacted_again ENUM ('yes', 'no'),
      wants_update ENUM ('yes', 'no'),
      notes TEXT,
      FOREIGN KEY (experimenter_id) REFERENCES experimenters (id) ON DELETE CASCADE,
      FOREIGN KEY (protocol_id) REFERENCES protocols (id) ON DELETE CASCADE)""",
    """\
    CREATE TABLE aliases (
      person INT NOT NULL,
      code VARCHAR(256) NOT NULL)""",
    """\
    CREATE TABLE files (
      change_id INT NOT NULL,
      path TEXT,
      FOREIGN KEY (change_id) REFERENCES changes (id) ON DELETE CASCADE)""",
    """\
    CREATE VIEW permissions AS
      SELECT
      code patient,
      date,
      type,
      period,
      experimenters.experimenter experimenter,
      protocols.protocol,
      version,
      agrees_to_highdensity HD,
      medical_data_for_research `use of medical data`,
      use_voice voice,
      store_longer_than_15y `longer than 15y`,
      data_sharing_institutes `share with institutes`,
      data_sharing_online `share online`,
      can_be_contacted_again `further contact`,
      wants_update updates,
      notes
      FROM changes
      LEFT JOIN protocols ON protocols.id = changes.protocol_id
      LEFT JOIN experimenters ON experimenters.id = changes.experimenter_id
      ORDER BY `code`, `date`
    """
    ]

def create_database(username=None):
    run_statements('information_schema', username, STATEMENTS_DB)
    run_statements(DB_NAME, username, STATEMENTS_TABLES)
    insert_default_values(DB_NAME, username)


def run_statements(db_name, username, statements):

    db = db_open(db_name, username)

    for t in statements:
        query = QSqlQuery(db)
        if not query.exec(dedent(t)):
            print(query.lastError().text())

    db.close()
    del db  # delete database before removing connection
    QSqlDatabase.removeDatabase(CONNECTION_NAME)


def insert_default_values(db_name, username=None):
    """We can use statements, but I prefer to use python API.
    """
    db = db_open(username=username)

    insert(db, 'protocols', {'protocol': '07-260_bcipatients'})
    insert(db, 'protocols', {'protocol': '14-090_children'})
    insert(db, 'protocols', {'protocol': '14-420_adults'})
    insert(db, 'protocols', {'protocol': 'ORCHIID'})

    insert(db, 'experimenters', {'experimenter': 'Mariska'})
    insert(db, 'experimenters', {'experimenter': 'Erik'})
    insert(db, 'experimenters', {'experimenter': 'Giovanni'})
    insert(db, 'experimenters', {'experimenter': 'Mariana'})
    insert(db, 'experimenters', {'experimenter': 'Elmar'})

    insert(db, 'aliases', {'person': 1, 'code': 'guij'})
    insert(db, 'aliases', {'person': 1, 'code': 'gennep'})
    insert(db, 'aliases', {'person': 2, 'code': 'meppel'})
    insert(db, 'aliases', {'person': 2, 'code': 'marrum'})

    db.close()
    del db  # delete database before removing connection
    QSqlDatabase.removeDatabase(CONNECTION_NAME)
