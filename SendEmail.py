import base64
from email import errors
from GoogleAuthenticator import authenticator
from email.mime.text import MIMEText

CLIENT_SECRET_FILE = 'email-google-auth-2/credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = authenticator(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

message = MIMEText('Python Mail test using API Google')
message['from'] = "piccini.linx@gmail.com"
message['to'] = 'patrick.piccini@linx.com.br'
message['subject'] = 'API Google '
raw_string = base64.urlsafe_b64encode(message.as_string())

try:
    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print ('Message Id: {}').format(message['id'])
except errors.HttpError as error:
     print ('An error occurred: {}').format(error)
