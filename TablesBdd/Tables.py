"""
Collects tweets by keywords
"""

#! /usr/bin/env python3
# coding: utf-8

import time
from sqlalchemy import Column, Integer, String, Boolean#, ForeignKey, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class KeyWords(Base):
    """
    Table to store keywords to be researched on twitter API
    """
    __tablename__ = 'keywords'
    key = Column(String, primary_key=True)
    nb_query = Column(Integer)
    active = Column(Boolean)

    def __init__(self, key):
        self.key = key
        self.nb_query = 0
        self.active = True

    def __repr__(self):
        return "<keyword : {}>".format(self.key)


class Users(Base):
    """
    User-specific data from tweets
    """
    __tablename__ = u'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_screen_name = Column(String)
    user_location = Column(String)
    user_descr = Column(String)
    user_lang = Column(String)
    user_followers_count = Column(Integer)
    user_verified = Column(Boolean)
    user_timezone = Column(String)
    user_friends_count = Column(Integer)

    def __init__(self, user_data):
        self.user_id = user_data['user_id']
        self.user_name = user_data['user_name']
        self.user_screen_name = user_data['user_screen_name']
        self.user_location = user_data['user_location']
        self.user_descr = user_data['user_descr']
        self.user_lang = user_data['user_lang']
        self.user_followers_count = user_data['user_followers_count']
        self.user_verified = user_data['user_verified']
        self.user_timezone = user_data['user_timezone']
        self.user_friends_count = user_data['user_friends_count']

    def __repr__(self):
        return "<User : {} - {}>".format(self.user_id, self.user_name)


class Tweets(Base):
    __tablename__ = u'Tweets'
    tweet_id = Column(Integer, primary_key=True)
    query = Column(String)
    inserted_date = Column(String)
    date = Column(String)
    month = Column(String)
    year = Column(String)
    truncated = Column(Boolean)
    urls = Column(String)
    hashtags = Column(String)
    user_mentions_name = Column(String)
    user_mentions_id = Column(String)
    text = Column(String)
    user_id = Column(Integer)
    user_name = Column(String)
    language = Column(String)
    place = Column(String)
    sensitive = Column(Boolean)
    reply_to_tw = Column(Integer)
    reply_to_user = Column(Integer)
    reply_to_user_name = Column(String)
    is_rt = Column(Boolean)
    source_tw = Column(String)
    media_type = Column(String)
    media_url = Column(String)
    media_nb = Column(Integer)
    json_output = Column(String)

    def __init__(self, tweet_data):
        self.tweet_id = tweet_data['tweet_id']
        self.query = tweet_data['query']
        self.inserted_date = time.strftime('%Y_%m_%d', time.localtime())
        self.date = tweet_data['date']
        self.month = tweet_data['month']
        self.year = tweet_data['year']
        self.truncated = tweet_data['truncated']
        self.urls = tweet_data['urls']
        self.hashtags = tweet_data['hashtags']
        self.user_mentions_name = tweet_data['user_mentions_name']
        self.user_mentions_id = tweet_data['user_mentions_id']
        self.text = tweet_data['text']
        self.user_id = tweet_data['user_id']
        self.user_name = tweet_data['user_name']
        self.language = tweet_data['language']
        self.place = tweet_data['place']
        self.sensitive = tweet_data['sensitive']
        self.reply_to_tw = tweet_data['reply_to_tw']
        self.reply_to_user = tweet_data['reply_to_user']
        self.reply_to_user_name = tweet_data['reply_to_user_name']
        self.is_rt = tweet_data['is_rt']
        self.source_tw = tweet_data['source_tw']
        self.media_type = tweet_data['media_type']
        self.media_url = tweet_data['media_url']
        self.media_nb = tweet_data['media_nb']
        self.json_output = tweet_data['json_output']


