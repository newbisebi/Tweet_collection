# Tweet Collection
This scripts aims at creating a database of tweets matching given hashtags or words. 

I'm new to programming, so this could be improved a lot for sure!

## Instructions
### Authentification
To use the scripts, you need to have Twitter API keys: a tutorial is available here: http://www.curiositybits.com/new-page-3/

Create a file "AuthTwitterCodes.txt" at project root with 4 lines corresponding to Twitter API ids (to be created in your developper account on Twitter), in that order :
- app_key
- app_secret
- oauth_token
- oauth_token_secret

No space, no comma.

### Search keywords
In the file keywords.txt, indicate words or hashtags you want to search in Twitter.

All keywords on the same line, separated by comma

Keywords removed from the file wont be search next time

### Search parameters
the following options can be passed :

-o (--older) :  if argument passed, search for tweets older than those already stored in Database. Otherwise, the program gets the latest tweets.


### Output
log and database (sqlite) are in folder "data"
