from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
FANTRAX_ROSTER_SPREADSHEET_ID = '1CC0YMzxfQUzV_0ukdChjrPCFqpUp342BUUkRvVdHnew'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'
FANTRAX_ROSTER_RANGE_NAME = 'Roster!C3:C26'

class SheetsService():
    def __init__(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('../cfg/token.json'):
            creds = Credentials.from_authorized_user_file('../cfg/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../cfg/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../cfg/token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            self.service = build('sheets', 'v4', credentials=creds)

        except HttpError as err:
            print(err)

    def read_sheet(self, worksheet_id, sheet_name, range=None):
        if range is None:
            range=sheet_name
        else:
            range=sheet_name + ':' + range

        values = self.service.spreadsheets().values().get(spreadsheetId=worksheet_id, range=range).execute()
        data = values.get('values', [])

        return data

    def add_sheet(self, worksheet_id, sheet_name):
        request = {'requests': [{
            'addSheet': {'properties': {'title': sheet_name}}
        }]}
        self.service.spreadsheets().batchUpdate(spreadsheetId=worksheet_id, body=request).execute()

    def create_worksheet(self, name):
        spreadsheet_properties = {
            'properties': {'title': name }
        }
        spreadsheet = self.service.spreadsheets().create(
            body=spreadsheet_properties, fields='spreadsheetId').execute()
        return spreadsheet.get('spreadsheetId')

    def write_sheet(self, worksheet_id, sheet_name, data):
        self.service.spreadsheets().values().append(
            spreadsheetId=worksheet_id, valueInputOption='RAW', range=sheet_name, body={'values': data}).execute()
            
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../cfg/token.json'):
        creds = Credentials.from_authorized_user_file('../cfg/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../cfg/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../cfg/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=FANTRAX_ROSTER_SPREADSHEET_ID,
                                    range=FANTRAX_ROSTER_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s' % (row[0]))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    # main()
    service = SheetsService()
    steve_id = service.create_worksheet('SteveSheet')
    # service.write_sheet(steve_id, [[1,2,3],[4,5,6]])
    # data = service.read_sheet(FANTRAX_ROSTER_SPREADSHEET_ID, 'Roster')
    service.add_sheet(steve_id, 'NewSheet')
    # print(type(data[0]))
    # print(data)

    # print('ID: {}'.format(steve_id))