from argparse import ArgumentParser, RawTextHelpFormatter
from textwrap import dedent
from pathlib import Path
from getpass import getuser

from .create import create_database
from .add import add_rows
from .get import get


def create_database_permissions():
    parser = ArgumentParser(
        description='Create Database called "metc" and populate it with some basic rows (f.e. protocols and experimenters)')
    parser.add_argument(
        '-U', '--username',
        help=f"specify username (if different from default `{getuser()}`)")
    args = parser.parse_args()
    create_database(username=args.username)


def add_permissions():
    parser = ArgumentParser(
        description=dedent("""\
            Add permissions to the `metc` database from a .tsv file.
            The .tsv file needs a header with the name of the columns. The possible columns are:
              - code (mandatory)
              - type (mandatory, one of 'informed consent','letter','email','phone','unresponsive','death')
              - period (mandatory, one of 'original','retrospective')
              - date (in format 1969-07-20)
              - protocol (one of the values in table `protocols`)
              - version (free text)
              - experimenter (one of the values in table `experimenters`)
              - agrees_to_highdensity ('yes', 'no')
              - medical_data_for_research ('yes', 'no')
              - use_voice ('yes', 'no')
              - store_longer_than_15y ('yes', 'no')
              - data_sharing_institutes ('yes', 'no')
              - data_sharing_online ('yes', 'no')
              - can_be_contacted_again ('yes', 'no')
              - wants_update ('yes', 'no')
              - notes (free text)
              - files (one or multiple paths to files separated by ';')

            If you do not want to specify a value, leave it empty. Do not use quotes.
            If the value you want to enter for `protocol` or `experimenter` are not present in the table, just let Gio know.
            """),
        formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        'tsv_file',
        help="Path to TSV file containing a line with the header and each row is a change in permissions")
    parser.add_argument(
        '-U', '--username',
        help=f"specify username (if different from default `{getuser()}`)")
    args = parser.parse_args()

    add_rows(Path(args.tsv_file).resolve(), username=args.username)


def get_permissions():
    parser = ArgumentParser(
        description='List permissions for one patient code and all the interactions we\'ve had with the patient')
    parser.add_argument(
        'code',
        help="Patient code")
    parser.add_argument(
        '-U', '--username',
        help=f"specify username (if different from default `{getuser()}`)")
    args = parser.parse_args()

    get(args.code, username=args.username)
