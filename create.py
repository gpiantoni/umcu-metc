#!/usr/bin/env python3

from xelo2.database.create import _drop_create_mysql, dedent, close_database
from PyQt5.QtSql import (
    QSqlQuery,
    QSqlDatabase,
    )

db_type = 'QMYSQL'
db_name = 'metc'
username = 'giovanni'
password = 'password'
CONNECTION_NAME = 'metc_database'


STATEMENTS = [
    """\
    CREATE TABLE patients (
      id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
      code VARCHAR(256))""",
    """\
    CREATE TABLE experimenters (
      id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
      experimenter VARCHAR(256))""",
    """\
    CREATE TABLE protocols (
      id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
      protocol VARCHAR(256))""",
    """\
    CREATE TABLE interactions (
      id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
      patient_id INT NOT NULL,
      experimenter_id INT,
      type ENUM ('in person', 'letter', 'email', 'phone', 'death') NOT NULL,
      protocol_id INT,
      date DATE,
      protocol_version TEXT,
      agrees_to_highdensity ENUM ('yes', 'no'),
      medical_data_for_research ENUM ('yes', 'no'),
      use_voice ENUM ('yes', 'no'),
      store_longer_than_15y ENUM ('yes', 'no'),
      data_sharing_institutes ENUM ('yes', 'no'),
      data_sharing_online ENUM ('yes', 'no'),
      can_be_contacted_again ENUM ('yes', 'no'),
      wants_update ENUM ('yes', 'no'),
      notes TEXT,
      FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE,
      FOREIGN KEY (experimenter_id) REFERENCES experimenters (id) ON DELETE CASCADE,
      FOREIGN KEY (protocol_id) REFERENCES protocols (id) ON DELETE CASCADE)""",
    """\
    CREATE TABLE files (
      interaction_id INT NOT NULL,
      path TEXT,
      FOREIGN KEY (interaction_id) REFERENCES interactions (id) ON DELETE CASCADE)""",
    """\
    INSERT INTO
        protocols (`protocol`)
    VALUES
        ('07-260_bcipatients'),
        ('14-090_children'),
        ('14-420_adults'),
        ('14-622_intraop'),
        ('ORCHIID')
    """,
    """\
    INSERT INTO
        experimenters (`experimenter`)
    VALUES
        ('Mariska'),
        ('Erik'),
        ('Giovanni'),
        ('Mariana'),
        ('Elmar')
    """,
    """\
    CREATE VIEW permissions AS
      SELECT
      patients.code,
      type,
      date,
      protocols.protocol,
      protocol_version version,
      agrees_to_highdensity HD,
      medical_data_for_research `use of medical data`,
      use_voice voice,
      store_longer_than_15y `longer than 15y`,
      data_sharing_institutes `share with institutes`,
      data_sharing_online `share online`,
      can_be_contacted_again `further contact`,
      wants_update updates,
      notes
      FROM interactions
      LEFT JOIN patients ON patients.id = interactions.patient_id
      LEFT JOIN protocols ON protocols.id = interactions.protocol_id
      ORDER BY `code`, `date`
    """
    ]


def main():
    _drop_create_mysql(db_name, username, password)

    db = QSqlDatabase.addDatabase(db_type, CONNECTION_NAME)
    assert db.isValid()

    db.setHostName('127.0.0.1')
    db.setUserName(username)
    if password is not None:
        db.setPassword(password)

    db.setDatabaseName(str(db_name))
    db.open()

    for t in STATEMENTS:
        query = QSqlQuery(db)
        if not query.exec(dedent(t)):
            print(query.lastError().text())

    close_database(db)


if __name__ == '__main__':
    main()
