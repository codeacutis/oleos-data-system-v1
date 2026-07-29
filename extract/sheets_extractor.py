from auth.google_auth import authenticate_google

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import yaml
from retry import retry

@retry(HttpError, tries=3, delay=2)
def extractor_sheet(spreadsheet, range_name):
    creds = authenticate_google()
    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=spreadsheet, range=range_name)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        return values
        
    except HttpError as err:
        raise err


def extractor_all_sheets():
    with open("config.yaml") as file:
        config = yaml.safe_load(file)
        
    data = []
    for form in config["forms"]:
        values = extractor_sheet(form["spreadsheet_id"], form["range"])
        data.append({
            "name" : form["name"], 
            "type" : form["type"], 
            "fase" : form["fase"], 
            "value" : values
            })
    
    return data