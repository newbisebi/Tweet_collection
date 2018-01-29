## Instructions
### Authentification
Create a file "AuthTwitterCodes.txt" at project root with 4 lines corresponding to Twitter API ids (to be created in your developper account on Twitter), in that order :
- app_key
- app_secret
- oauth_token
- oauth_token_secret
No space, no comma.

### Search keywords
In the file keywords.txt, indicate words or hashtags you want to search for in Twitter.
All keywords on the same line, separated by comma

### Search parameters
the following options can be passed :
-o (--older) :  if argument passed, search for tweets older than those already stored in Database. Otherwise, the program get tweets more recent.


##To do
auth ids could be passed as arguments
default datafile name : "data.sqlite" ; name could be passed as argument
