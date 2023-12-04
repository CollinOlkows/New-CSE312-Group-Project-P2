import httplib2
import os
import oauth2client
from oauth2client import client, tools,file
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
from config import get_creds
from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI, client
import hashlib
import secrets
def get_credentials():
    c = get_creds()
    CLIENT_ID = c['client_id']
    CLIENT_SECRET = c['client_secret']
    REFRESH_TOKEN = c['refresh']
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    credentials = client.OAuth2Credentials(
        access_token=None,  # set access_token to None since we use a refresh token
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        refresh_token=REFRESH_TOKEN,
        token_expiry=None,
        token_uri=GOOGLE_TOKEN_URI,
        user_agent="pythonclient",
        scopes = SCOPES)

    credentials.refresh(httplib2.Http())  # refresh the access token (optional) 
    return credentials

def SendMessage(sender, to, subject, msgHtml, msgPlain):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message1 = CreateMessage(sender, to, subject, msgHtml, msgPlain)
    SendMessageInternal(service, "me", message1)

def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def CreateMessage(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body

def verification_email(code,User,Email_To):
    host = 'www.wizardsandassociates.me'
    #host = 'localhost:8080'
    link = f'{host}/verify/{code}'
    to = Email_To
    sender = "wizardsandassociates@gmail.com"
    subject = "Modern Art Account Creation!"
    msgHtml = f"""<html>
                <head></head>
                <body>
                </p>Hello {User}!<br/>Thank you for signing up for Modern Art! Please follow this Link to verify your account! <br/> {link}</p>
                </body>
                </html>
"""
    msgPlain = f"Hello {User}!<br/>Thank you for signing up for Modern Art! Please follow this link to verify your account! <br/> {link}"
    SendMessage(sender, to, subject, msgHtml, msgPlain)

def make_url_for_ver():
    verification_code = secrets.token_hex(100)
    return verification_code
