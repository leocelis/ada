import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import get_service

# Define the auth scopes to request.
scope = 'https://www.googleapis.com/auth/analytics.readonly'
key_file_location = 'client_secrets.json'

# Authenticate and construct service.
service = get_service(api_name='analytics',
                      api_version='v3',
                      scopes=[scope],
                      key_file_location=key_file_location)

# Get a list of all Google Analytics accounts for this user
try:
    accounts = service.management().accounts().list().execute()

