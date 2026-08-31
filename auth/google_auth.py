import os
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def authenticate_google():
    
    creds = None
    token_path = os.path.join(BASE_DIR, "token.json")
    secret_path = os.path.join(BASE_DIR, "client_secret.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise RuntimeError("Token expirado ou inválido e não é possível reautenticar em ambiente não interativo. Atualize o secret TOKEN_JSON no GitHub.")
        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    
    return creds