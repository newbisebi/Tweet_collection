"""
Create  SqlAlchemy session
"""

#! /usr/bin/env python3
# coding: utf-8

import os
import argparse
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

def arguments():
    """
    Define arguments passed in console
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--datafile_name', help="""Enter datafile name eg data""")
    return parser.parse_args()

class ConnectSQLAlchemy:
    """
    Return objects used to interact with database
    """
    def __init__(self):
        self.Base = declarative_base()
        self.database_name = "data"

    def path_to_database(self, database_name):
        directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bdd_file = os.path.join(directory, "data",database_name)
        bdd_file = "sqlite:///"+bdd_file+".sqlite"
        return bdd_file

    @property
    def session(self):
        if arguments().datafile_name:
            bdd_file = self.path_to_database(arguments().datafile_name)
        else:
            bdd_file = self.path_to_database(self.database_name)
        engine = sqlalchemy.create_engine(bdd_file, echo=False)
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        sess = Session()
        self.Base.metadata.create_all(engine)
        return sess

def main():
    conn = ConnectSQLAlchemy()
    session = conn.session
    Base = conn.Base
    return session, Base


if __name__ == '__main__':
    print(main())
