"""
Collects tweets by keywords
"""

#! /usr/bin/env python3
# coding: utf-8

from sqlalchemy import Column, Integer, String#, ForeignKey, Text, DateTime, Float, Boolean
from connect import SqlaSession, TwitterApi


API = TwitterApi.main()
session, Base = SqlaSession.main()
#import pdb; pdb.set_trace()


class KEYWORDS(Base):
    """
    Sqlite table to store research keys
    """
    __tablename__ = u'keywords'
    key = Column(String, primary_key =True)
    nb_query = Column(Integer)

    def __init__(self):
        self.nb_query = 0

    def add_keys(session=s, keywords = [], hashtags=[]):
        """
        Ajoute des mots clés à rechercher
        """
        for h in hashtags:
            h = h.replace("#","")
            h = "%23"+h
            keywords.append(h)

        for k in keywords:
            test = s.query(KEYWORDS).filter_by(key=k).all()
            if not test:
                new = KEYWORDS(k)
                s.add(new)
        s.commit()

def main():
    pass
    #On défini la liste des mots clés à traiter

    #On lance la collecte

    #ON récupère les infos et on les mets dans le format attendu

    #On créé les objets correspondants


if __name__ == '__main__':
    main()