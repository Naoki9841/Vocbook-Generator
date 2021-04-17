import os
import sys
file_path = os.path.dirname(__file__)
module_path = os.path.join(file_path, "lib")
sys.path.append(module_path)

from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1urSz2qiJFUHtXm6v9FKtSS6VfKgU1y92fry-gc5O8eo'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

example = [["a", 1], ["b", 2]]

request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Sheet1!B2", valueInputOption="USER_ENTERED", body={"values": example}).execute()




