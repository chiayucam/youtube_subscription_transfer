# youtube_subscription_transfer
youtube_subscription_transfer is a python program for subscription exporting and importing from a chosen youtube account. This program uses Youtube's Data API to extract subscription data from an authorized chosen account and saves into a local json file. Vice versa, it can import subscription data from a local json file into an authorized account.
## Requirements
### Python packages
* google-api-python-client==1.12.8
* google-auth-httplib2==0.0.4
* google-auth-oauthlib==0.4.2
  
Instructions for installing these packages can be found here: https://developers.google.com/youtube/v3/quickstart/python

### OAuth 2.0 setup for visiting Google API
This application uses sensitive scopes of Google API and thus requires Google's verification for other users to operate. Currently, there is no plan for verifying this program in the near future, users will have to set up there own OAuth 2.0 client ID for this application. Here are the instruction for setting this up.
1. Go to https://console.cloud.google.com/apis/dashboard
2. Add new project and name it as: youtube_subscription_transfer
3. Click + ENABLE APIS AND SERVICES and Enable Youtube Data API v3 for the project
4. Go to OAuth consent screen and choose External User Type
5. Fill in App information
6. Add these 2 scopes [.../auth/youtube/readonly] (View your YouTube account) and [.../auth/youtube] (Manage your YouTube account)
7. Add your gmail in + ADD USERS
8. Go to Credentials and choose OAuth client ID in + CREATE CREDENTIALS
9. Choose Desktop App for Application type
10. Download OAuth client into json file and name it client_id.json, save it under the client_secrets_file directory
  
More instructions for setting up a OAuth 2.0 client ID can be found here: https://developers.google.com/youtube/registering_an_application

## Commands
### Export
Use command:
```
python youtube_subscription_transfer.py export <filename>.json
```
to export subscription list from a youtube account into a json file saved in the json directory

### Import
Use command:
```
python youtube_subscription_transfer.py import <filename>.json
```
to import subscription list from a json file in the json directory into a youtube account
