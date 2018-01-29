"""
Connexion to the Twitter API
return an api object
"""

#! /usr/bin/env python3
# coding: utf-8

import os
import logging as lg
from twython import Twython #interface avec Twitter
from twython import TwythonAuthError

lg.basicConfig(level=lg.INFO)
#import pdb; pdb.set_trace()

def create_file():
    """
    Create a file with identifications keys to connect to Twitter API
    File must be completed by user before lauching tweet collection
    """
    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    twitter_codes_file = os.path.join(directory, 'AuthTwitterCodes.txt')
    with open(twitter_codes_file, "w") as code_file:
        code_file.write("""Replace this line with app_key\nReplace this line with app_secret\nReplace this line with oauth_token\nReplace this line with oauth_token_secret""")


def open_codes_file():
    """
    Read the file containing the api_codes
    """
    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    twitter_codes_file = os.path.join(directory, 'AuthTwitterCodes.txt')
    #import pdb; pdb.set_trace()
    with open(twitter_codes_file) as code_file:
        api_codes = [line.strip() for line in code_file.readlines()]
    return api_codes

def log_in_to_api(api_codes):
    """
    Log in to the API
    """
    return Twython(app_key=api_codes[0],
                   app_secret=api_codes[1],
                   oauth_token=api_codes[2],
                   oauth_token_secret=api_codes[3])

def connect():
    """
    Main operations
    """
    try:
        api_codes = open_codes_file()
        api = log_in_to_api(api_codes)
        lg.info("Connexion à l'API effectuée")
    except TwythonAuthError:
        lg.critical("Authentification failed, please verify credentials")
        raise SystemExit
    except FileNotFoundError:
        lg.critical("########### Authentifications codes expected. Please complete the file 'AuthTwitterCodes.txt' at project root with login keys: ('app_key, app_secret, oauth_token, oauth_token_secret' ###########")
        create_file()
        raise SystemExit

    return api

if __name__ == '__main__':
    pass
