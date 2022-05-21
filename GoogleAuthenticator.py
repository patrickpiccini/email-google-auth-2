import os.path, json, requests#
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta#


def authenticator(client_secret_file, api_service_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_service_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    creds = None
    date_time_now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")#

    if os.path.exists('email-google-auth-2/token.json'):
        with open('email-google-auth-2/token.json', 'r') as verify:#
            info_json = json.load(verify)#

            if date_time_now < info_json['expiry']:#
                refresh_token(info_json)#

        creds = Credentials.from_authorized_user_file(
            'email-google-auth-2/token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('email-google-auth-2/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        print(API_SERVICE_NAME, 'service created successfully')
        return service

    except HttpError as error:
        # TO DO(developer) - Handle errors from gmail API.
        print('An error occurred: {}'.format(error))

def refresh_token(info_json):
    try:
        refresh_token_obj = {
            "client_id": str(info_json["client_id"]).replace("u'", "'"),
            "client_secret": str(info_json["client_secret"]).replace("u'", "'"),
            "refresh_token": str(info_json["refresh_token"]).replace("u'", "'"), 
            "grant_type": "refresh_token"
        }

        refresh_credentials = request_refresh_token(refresh_token_obj)

        refresh_toke_obj = json.loads(refresh_credentials.text)
        expiry_time_refresh_token = datetime.now() + timedelta(hours=4)
        access_token = refresh_toke_obj['access_token']

        # Token replacement and 4+hour increment in token.json file
        info_json['expiry'] = expiry_time_refresh_token.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        info_json['token'] = str(access_token)

        with open('email-google-auth-2/token.json', 'w') as token:
            token.write(json.dumps(info_json))

    except Exception as error:
        print('Erro criacao de refresh_token.\n%s' % str(error))

def request_refresh_token(refresh_token_obj):
    try:
        return requests.post('https://oauth2.googleapis.com/token', data=refresh_token_obj)

    except requests.exceptions.Timeout as e:
        print('Request Timeout exception:\n%s' % str(e))
        return
    except requests.exceptions.TooManyRedirects as e:
        print('Request too many redirects exception:\n%s' % str(e))
        return
    except requests.exceptions.RequestException as e:
        print('Request exception:\n%s' % str(e))
        return