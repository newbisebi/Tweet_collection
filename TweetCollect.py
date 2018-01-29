"""
Collects tweets by keywords
"""

#! /usr/bin/env python3
# coding: utf-8
import os
import re
import logging as lg
import sqlalchemy
from sqlalchemy import func
from TablesBdd.Tables import KeyWords, Tweets, Users, Base
from connect import TwitterApi

lg.basicConfig(level=lg.INFO)
api = TwitterApi.main()

class Database:
    """
    Database to store data from Twitter
    """


    def __init__(self, filename='twitter_data'): #default database name = data
        self.name = filename
        directory = os.path.dirname(os.path.abspath(__file__))
        bdd_file = os.path.join(directory, "data", self.name)
        bdd_file = "sqlite:///"+bdd_file+".sqlite"
        engine = sqlalchemy.create_engine(bdd_file, echo=False)
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)
        self.all_keywords = []
        self.active_keywords = []
        self.inactive_keywords = []

    def add_keywords(self, keywords_list):
        """
        Set the list of keywords to look up on Twitter
        """
        for key in keywords_list:
            key = re.sub('^#', "%23", key) #remplace # par '%23'
            key_already_exists = self.session.query(KeyWords).filter_by(key=key)
            if not key_already_exists.all():
                new = KeyWords(key)
                self.session.add(new)
                lg.info("New keyword added to the table 'keywords' : '%s'", key)
            elif key_already_exists.one().active is False:
                key_to_reactivate = key_already_exists.one()
                key_to_reactivate.active = True
                lg.info("Key '%s' status passed to 'active'", key)
        self.session.commit()

    def get_kw(self):
        """
        Create/update lists of keywords (all / active / inactive)
        """
        self.all_keywords = [el.key for el in self.session
                             .query(KeyWords.key)]
        self.active_keywords = [el.key for el in self.session
                                .query(KeyWords.key)
                                .filter_by(active=True)
                                .order_by(KeyWords.nb_query)]
        self.inactive_keywords = [el.key for el in self.session
                                  .query(KeyWords.key)
                                  .filter_by(active=False)]
        #import pdb ; pdb.set_trace()

    def desactivate_keywords(self, keywords):
        """
        Pass status of keywords to inactive when removed from the text file
        """
        keywords = [re.sub('^#', "%23", key) for key in keywords]
        for key in self.active_keywords:
            if key not in keywords:
                key_to_desactivate = self.session.query(KeyWords).filter_by(key=key).one()
                key_to_desactivate.active = False
                self.session.commit()
                lg.info("Key %s status passed to 'inactive'", key)

    def get_limits(self, key):
        """
        Get the newest and oldest tweet already collected for a given keyword
        """
        max_id = self.session.query(func.max(Tweets.tweet_id)).filter_by(query=key).one()
        min_id = self.session.query(func.min(Tweets.tweet_id)).filter_by(query=key).one()
        return min_id, max_id

    def query_api(self, key, oldest_tweets=True):
        lg.info('Searching tweets for keywords %s', key)
        min_id, max_id = self.get_limits(key)

        continu = True
        i=0
        while continu:
            i+=1
            lg.info("Recherche pour le mot clé %s : recherche numéro %s", key, i)
            try:
                if oldest_tweets == True:
                    res = api.search(q=key,
                                     count=100,
                                     result_type="recent",
                                     max_id=min_id-1,
                                     include_entities=True,
                                     tweet_mode='extended')
                else:
                    res = api.search(q=key,
                                     count=100,
                                     result_type="recent",
                                     since_id=max_id+1,
                                     include_entities=True,
                                     tweet_mode='extended')
                if res['statuses']:
                    lg.info("Nombre de tweets : %s", len(res['statuses']))
                    min_id = enregistrement(res, key)
                    continu = True
                    oldest_tweets = True
                    lg.debug("min_id : %s", min_id)
                else:
                    lg.info("Plus de résultat pour le mot clé '%s' ; passage au mot clé suivant", key)
                    continu = False

            except TwythonRateLimitError:
                lg.warning("Twitter limit reached. Waiting 15 minutes before moving to next keyword")
                time.sleep(900)
                break

            #######  UPDATE NUMBER OF QUERIES FOR A KEYWORD ######
            key_upd = s.query(KEYWORDS).filter_by(key = k).one()
            key_upd.nb_query += 1
            s.commit()

def main():
    #Creating / connecting to Bdd
    db = Database(filename='twitter_data')

    #Updating keywords list
    with open('keywords.txt') as keywords_file:
        keywords = ''.join(keywords_file.readlines()).replace(' ', '').split(',')
    db.add_keywords(keywords)
    db.get_kw()
    db.desactivate_keywords(keywords)
    db.get_kw() #Repeat this line to eliminate recently desactivated keys from query list

    #Tweets Collection
    for key in db.active_keywords:
        db.query_api(key)




if __name__ == '__main__':
    main()