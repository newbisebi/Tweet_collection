"""
Connexion to the Twitter API
return an api object
"""

#! /usr/bin/env python3
# coding: utf-8

import argparse
import os
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
    parser.add_argument('-f', '--codes_filename', help="""Enter the name of the txt file with API keys (4 lines)""")
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

    def code_file_param(self,args):
        """
        Read api keys passed as parameters
        """
        
        self.api_codes = args.twittercodes.split(',')

    def open_codes_file(self, args):
        """
        Read the file containing the api_codes
        """
        if not args.codes_filename:
            twitter_codes_filename = 'AuthTwitterCodes.txt'
        else:
            twitter_codes_filename = args.codes_filename

        directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        twitter_codes_file = os.path.join(directory, twitter_codes_filename)
        #import pdb; pdb.set_trace()
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
    args = arguments()
    auth = AuthTwitter()
    if arguments().twittercodes is not None:
        auth.code_file_param(args)
    else:
        try:
            auth.open_codes_file(args)
        except FileNotFoundError:
            lg.critical("Authentifications codes expected. Please enter codes as parameters or create a file with a line for each key ('app_key, app_secret, oauth_token, oauth_token_secret'")
    if auth.api_codes:
        api = auth.connect()
        lg.info("Connexion à l'API effectuée")
    else:
        api = None
    return api

if __name__ == '__main__':
    API = main()
    print(API)
