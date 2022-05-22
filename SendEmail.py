import base64
from GoogleAuthenticator import authenticator
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = authenticator(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

message = MIMEText('Python Mail test using API Google')
message['from'] = "smigoubr@gmail.com"
message['to'] = 'hejito5088@dakcans.com'
message['subject'] = 'API Google 4'
raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()

try:
    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print ('Message Id: {}'.format(message['id']))
except HttpError as error:
     print ('An error occurred: {}'.format(error))
