import json
import getpass


import requests
from bs4 import BeautifulSoup


import os
import sys
file_path = os.path.dirname(__file__)
module_path = os.path.join(file_path, "lib")
sys.path.append(module_path)

from googleapiclient.discovery import build
from google.oauth2 import service_account



# `getpass.getuser()` でカレントユーザの名前を取得する
CHROME_BOOKMARK_PATH = (
    '/Users/mitsuinaoki/Library/Application Support/'
    'Google/Chrome/Default/Bookmarks'
).format(username=getpass.getuser())

def get_chrome_bookmark_data() -> dict:
    '''Get the json of user's Chrome bookmark.'''
    with open(CHROME_BOOKMARK_PATH) as f:
        return json.load(f)

# just print out to commandline
def print_word_name_from_url(weblio_url):

    print(weblio_url)

    if (weblio_url[:31] == "https://ejje.weblio.jp/content/"):
        word = weblio_url[31:]
    else:
        print('{0} is not managable url'.format(weblio_url))
        return

    html = requests.get(weblio_url)
    soup = BeautifulSoup(html.content, "html.parser")

    meaning = soup.find(class_ = "content-explanation ej")

    if meaning:
        print('{0}: {1}'.format(word, meaning.text))
    else:
        meaning = meaning = soup.find(class_ = "content-explanation renewal ej")
        if meaning:
            print('{0}: {1}'.format(word, meaning.text))
        else:
            print('cannot extract from {0}'.format(weblio_url))


# return [word, meaning] if they can be extracted.
# return an empty array if not.
def make_words_array_1D_from_url(weblio_url):

    print(weblio_url)

    if (weblio_url[:31] == "https://ejje.weblio.jp/content/"):
        word = weblio_url[31:]
    else:
        print('{0} is not managable url'.format(weblio_url))
        return []

    html = requests.get(weblio_url)
    soup = BeautifulSoup(html.content, "html.parser")

    meaning = soup.find(class_ = "content-explanation ej")

    if meaning:
        print('{0}: {1}'.format(word, meaning.text))
        return [word, meaning.text]
    else:
        meaning = meaning = soup.find(class_ = "content-explanation renewal ej")
        if meaning:
            print('{0}: {1}'.format(word, meaning.text))
            return [word, meaning.text]
        else:
            print('cannot extract from {0}'.format(weblio_url))
            return []


# make words array to put into spread sheet
def make_words_array_from_bookmark():
    # JSON 内のデータを取得する
    bookmark_data = get_chrome_bookmark_data()

    bookmark_bar = bookmark_data['roots']['synced']['children']

    array2D = []

    for entry in bookmark_bar:
        if entry['name'] == 'English vocabularies':
            for vocabularies in entry['children']:
                array1D = make_words_array_1D_from_url(vocabularies['url'])
                if array1D:
                    array2D.append(array1D)
            # Now we are interested in only one entry
            break

    return array2D

# 認証キー (変更しない)
SERVICE_ACCOUNT_FILE = 'keys.json'
# これも変更しない
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1urSz2qiJFUHtXm6v9FKtSS6VfKgU1y92fry-gc5O8eo'

def write_to_spreadsheet(arrray2D):

    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Sheet1!B2", valueInputOption="USER_ENTERED", body={"values": arrray2D}).execute()


def main():
    extracted = make_words_array_from_bookmark()
    write_to_spreadsheet(extracted)


main()
