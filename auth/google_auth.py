import os

from google.oauth2 import service_account

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def authenticate_google():
    service_account_path = os.path.join(BASE_DIR, "service_account.json")
    return service_account.Credentials.from_service_account_file(service_account_path, scopes=SCOPES)