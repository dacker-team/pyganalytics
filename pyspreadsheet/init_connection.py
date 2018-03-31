import argparse
import os
# Path to get client_secrets.json and to store credentials
import httplib2
from googleapiclient.discovery import build
from oauth2client import client, file
from oauth2client import tools

GOOGLE_CLIENT_SECRET_PATH = os.environ.get("GOOGLE_CLIENT_SECRET_PATH")
GOOGLE_CREDENTIALS_PATH = os.environ.get("GOOGLE_CREDENTIALS_PATH")

if not GOOGLE_CLIENT_SECRET_PATH:
    GOOGLE_CLIENT_SECRET_PATH = './'

if not GOOGLE_CREDENTIALS_PATH:
    GOOGLE_CREDENTIALS_PATH = './'

if GOOGLE_CLIENT_SECRET_PATH[-1] == '/':
    GOOGLE_CLIENT_SECRET_PATH = GOOGLE_CLIENT_SECRET_PATH[:-1]

if GOOGLE_CREDENTIALS_PATH[-1] == '/':
    GOOGLE_CREDENTIALS_PATH = GOOGLE_CREDENTIALS_PATH[:-1]

GOOGLE_CLIENT_SECRET_PATH = GOOGLE_CLIENT_SECRET_PATH + '/client_secrets.json'


def get_api_account(version='v4'):
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    discovery_uri = 'https://sheets.googleapis.com/$discovery/rest'
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser])
    flags = parser.parse_args([])

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(
        GOOGLE_CLIENT_SECRET_PATH,
        scope=scopes,
        message=tools.message_if_missing(GOOGLE_CLIENT_SECRET_PATH))

    path_storage = GOOGLE_CREDENTIALS_PATH + "spreadsheet.json"
    storage = file.Storage(path_storage)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())

    # Build the service object.
    if version == 'v3':
        account = build('analytics', version, http=http)
    else:
        account = build('analytics', version, http=http, discoveryServiceUrl=discovery_uri)

    return account.spreadsheets()
