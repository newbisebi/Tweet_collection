"""
Connexion to the Twitter API
return an api object
"""

#! /usr/bin/env python3
# coding: utf-8

import argparse
import logging as lg
from twython import Twython #interface avec Twitter

lg.basicConfig(level=lg.INFO)
#import pdb; pdb.set_trace()


def arguments():
    """
    Define arguments passed in console
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--twittercodes', help="""Enter the 4 keys for authenticating into Twitter API, separated by comma, no space""")
    return parser.parse_args()

class AuthTwitter:
    """
    Authentification to the Twitter API
    """
    def __init__(self, api_codes=None):
        """
        API Codes in the following order : app_key, app_secret, oauth_token, oauth_token_secret
        """
        self.api_codes = api_codes

    def code_file_param(self):
        """
        Read api keys passed as parameters
        """
        args = arguments()
        self.api_codes = args.twittercodes.split(',')

    def open_codes_file(self, twitter_codes_file):
        """
        Read the file containing the api_codes
        """
        with open(twitter_codes_file) as code_file:
            self.api_codes = [line.strip() for line in code_file.readlines()]

    def connect(self):
        """
        Log in to the API
        """
        return Twython(app_key=self.api_codes[0],
                       app_secret=self.api_codes[1],
                       oauth_token=self.api_codes[2],
                       oauth_token_secret=self.api_codes[3])

def main():
    """
    Main operations
    """
    auth = AuthTwitter()
    if arguments().twittercodes is not None:
        import pdb; pdb.set_trace()
        auth.code_file_param()
    else:
        try:
            auth.open_codes_file(twitter_codes_file='AuthTwitterCodes.txt')
        except FileNotFoundError:
            lg.critical("Authentifications codes expected. Please enter codes as parameters or create a file with a line for each key ('app_key, app_secret, oauth_token, oauth_token_secret'")
    if auth.api_codes:
        api = auth.connect()
        lg.info("Connexion à l'API effectuée")
    return api

if __name__ == '__main__':
    twitter_api = main()
    print(twitter_api)
