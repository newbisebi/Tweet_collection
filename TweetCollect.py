"""
Collects tweets by keywords
"""

#! /usr/bin/env python3
# coding: utf-8
import os
import re
import time
from datetime import datetime #date et heure
import sqlalchemy
from sqlalchemy import func
from twython import TwythonRateLimitError
from Modules.logger import logger
from Modules import TwitterApi
from TablesBdd.Tables import KeyWords, Tweets, Users, Base

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
                logger.info("New keyword added to the table 'keywords' : '%s'", key)
            elif key_already_exists.one().active is False:
                key_to_reactivate = key_already_exists.one()
                key_to_reactivate.active = True
                logger.info("Key '%s' status passed to 'active'", key)
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
                logger.info("Key %s status passed to 'inactive'", key)

    def get_limits(self, key):
        """
        Get the newest and oldest tweet already collected for a given keyword
        """
        max_id = self.session.query(func.max(Tweets.tweet_id)).filter_by(query=key).one()[0]
        min_id = self.session.query(func.min(Tweets.tweet_id)).filter_by(query=key).one()[0]
        return min_id, max_id

    def increment_nb_query(self, key):
        """
        Add 1  to the number of query realized for a given keyword
        """
        key_upd = self.session.query(KeyWords).filter_by(key=key).one()
        key_upd.nb_query += 1
        self.session.commit()

    def launch_query(self, key, oldest_tweets=False):
        """
        Look up tweets corresponding to a given keyword
        Can search for oldest tweet than those previously collected
        or on the contrary, more recent tweets.
        the oldest mode enables user to get tweets from the past week.
        """
        logger.info('Searching tweets for keywords %s', key)
        min_id, max_id = self.get_limits(key)

        keep_looking = True
        i = 0
        while keep_looking:
            i += 1
            logger.info("Searching for keyword %s ; loop number %s", key, i)
            try:
                if oldest_tweets is True:
                    if min_id:
                        min_id -= 1
                    res = api.search(q=key,
                                     count=100,
                                     result_type="recent",
                                     max_id=min_id,
                                     include_entities=True,
                                     tweet_mode='extended')
                else:
                    if max_id:
                        max_id += 1
                    res = api.search(q=key,
                                     count=100,
                                     result_type="recent",
                                     since_id=max_id,
                                     include_entities=True,
                                     tweet_mode='extended')
                if res['statuses']: #case where there are some results to write in database
                    logger.info("Number of tweets : %s", len(res['statuses']))
                    min_id = min([tweet['id'] for tweet in res['statuses']])-1
                    logger.debug("min_id : %s", min_id)

                    #Formatting and writing data
                    self.write_data(res, key)


                    keep_looking = True #still results so moving to next loop
                    oldest_tweets = True #then we search tweet oldest than those just collected
                else:
                    logger.info("No more results for keyword '%s' ; moving to next keyword", key)
                    keep_looking = False

            except TwythonRateLimitError:
                logger.warning("Twitter limit reached. Waiting 15 minutes before moving to next keyword")
                time.sleep(900)
                break
            self.increment_nb_query(key)

    def write_data(self, res, key):
        """
        Get data from Twitter and reorganize into two dictionnary,
        one to be passed as argument for class Tweets, and the other for class Users
        Then write data in DB using these dics
        """
        tweet_data = {}
        user_data = {}

        tweet_data['query'] = key
        #min_id = None
        for tw in res['statuses']:
            #tweets data
            tweet_data['tweet_id'] = tw["id"]

            date = tw["created_at"]
            date1 = datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')
            tweet_data['date'] = date1.strftime('%Y-%m-%d')
            tweet_data['month'] = date1.strftime('%m')
            tweet_data['year'] = date1.strftime('%Y')

            tweet_data['truncated'] = tw["truncated"]
            tweet_data['urls'] = ','.join([url["expanded_url"] for url in tw["entities"]["urls"]])
            tweet_data['hashtags'] = ','.join([ht["text"] for ht in tw["entities"]["hashtags"]])
            tweet_data['user_mentions_name'] = ','.join(
                [user["screen_name"] for user in tw["entities"]["user_mentions"]])
            tweet_data['user_mentions_id'] = ','.join(
                [str(user["id"]) for user in tw["entities"]["user_mentions"]])
            tweet_data['text'] = tw["full_text"]
            tweet_data['language'] = tw["lang"]
            if tw['place']:
                tweet_data['place'] = tw['place']['name'] + ", "+tw['place']['country']
            else:
                tweet_data['place'] = None
            if "possibly_sensitive" in tw:
                tweet_data['sensitive'] = tw["possibly_sensitive"]
            else:
                tweet_data['sensitive'] = False
            tweet_data['reply_to_tw'] = tw["in_reply_to_status_id"]
            tweet_data['reply_to_user'] = tw["in_reply_to_user_id"]
            tweet_data['reply_to_user_name'] = tw["in_reply_to_screen_name"]
            tweet_data['is_rt'] = bool('retweeted_status' in tw)

            tweet_data['source_tw'] = tw["source"]
            if "extended_entities" in tw:
                tweet_data['media_type'] = ','.join(
                    [media["type"] for media in tw["extended_entities"]["media"]])
                tweet_data['media_url'] = ','.join(
                    [media["media_url"] for media in tw["extended_entities"]["media"]])
                tweet_data['media_nb'] = len(tw["extended_entities"]["media"])
            else:
                tweet_data['media_type'] = None
                tweet_data['media_url'] = None
                tweet_data['media_nb'] = None

            tweet_data['json_output'] = str(tw)

             #Shared data
            tweet_data['user_id'] = tw["user"]["id"]
            tweet_data['user_name'] = tw["user"]["name"]
            user_data['user_id'] = tw["user"]["id"]
            user_data['user_name'] = tw["user"]["name"]

            #User specific data
            user_data['user_screen_name'] = tw["user"]["screen_name"]
            user_data['user_location'] = tw["user"]["location"]
            user_data['user_descr'] = tw["user"]["description"]
            user_data['user_lang'] = tw["user"]["lang"]
            user_data['user_followers_count'] = tw["user"]["followers_count"]
            user_data['user_verified'] = tw["user"]["verified"]
            user_data['user_timezone'] = tw["user"]["time_zone"]
            user_data['user_friends_count'] = tw['user']['friends_count']

            #Writing User data :
            user = self.session.query(Users).filter_by(user_id=user_data['user_id'])
            if not user.all():
                new = Users(user_data)
                self.session.add(new)

            #Wrinting Tweet_data :
            tweet_id = tweet_data['tweet_id']
            tweet = self.session.query(Tweets.tweet_id).filter_by(tweet_id=tweet_id).all()
            if not tweet:
                new = Tweets(tweet_data)
                self.session.add(new)
                logger.info("Adding tweet %s", tweet_id)
            self.session.commit()

def launch_program():
    """
    Successive operations to run the program
    """
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
        db.launch_query(key, oldest_tweets=False)

if __name__ == '__main__':
    launch_program()
