from __future__ import print_function

import os.path
import time

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
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
    _TOKEN_PATH = 'UpdateTeamSheets/cfg/token.json'

    def __init__(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        count = 0
        success = False
        error = None
        while (success is False) and (count < 5):
            count += 1
            try:
                creds = None
                # The file token.json stores the user's access and refresh tokens, and is
                # created automatically when the authorization flow completes for the first
                # time.
                if os.path.exists(self._TOKEN_PATH):
                    creds = Credentials.from_authorized_user_file(self._TOKEN_PATH, SCOPES)
                # If there are no (valid) credentials available, let the user log in.
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'UpdateTeamSheets/cfg/credentials.json', SCOPES)
                        creds = flow.run_local_server(port=0)
                    # Save the credentials for the next run
                    with open(self._TOKEN_PATH, 'w') as token:
                        token.write(creds.to_json())

                self.service = build('sheets', 'v4', credentials=creds)
                success = True

            except HttpError as err:
                print(err)
                break

            except RefreshError as err:
                print(str(err) + '\nReplacing expired token...')
                if os.path.exists(self._TOKEN_PATH):
                    os.remove(self._TOKEN_PATH)

    def execute_sheets_operation(self, op, worksheet_id=None, workbook_name=None, sheet_name=None, \
        data_range=None, data=None, sheet_id=None):
        success = False
        ret = None
        while success is False:
            try:
                success = True
                if op == 'read':
                    ret = self._read_sheet(worksheet_id, sheet_name, data_data_range)
                elif op == 'get_ids':
                    ret = self._get_sheet_ids(worksheet_id)
                elif op == 'add_sheet':
                    self._add_sheet(worksheet_id, sheet_name)
                elif op == 'create':
                    ret = self._create_worksheet(workbook_name)
                elif op == 'write':
                    self._write_sheet(worksheet_id, sheet_name, data)
                elif op == 'delete_sheet':
                    self._delete_sheet(worksheet_id, sheet_id)
                else:
                    success = False
            except HttpError as err:
                if err.status_code == 429:
                    time.sleep(30)
                    success = False
                else:
                    break
            except:
                break    

        return ret

    def _read_sheet(self, worksheet_id, sheet_name, data_range=None):
        if data_range is None:
            data_range=sheet_name
        else:
            data_range=sheet_name + ':' + data_range

        values = self.service.spreadsheets().values().get(spreadsheetId=worksheet_id, range=data_range).execute()
        data = values.get('values', [])

        return data       

    def _get_sheet_ids(self, worksheet_id):
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=worksheet_id).execute()
        idList = list()
        for sheet in spreadsheet['sheets']:
            idList.append(sheet['properties']['sheetId'])

        return idList

    def _add_sheet(self, worksheet_id, sheet_name):
        request = {'requests': [{
            'addSheet': {'properties': {'title': sheet_name}}
        }]}
        self.service.spreadsheets().batchUpdate(spreadsheetId=worksheet_id, body=request).execute()

    def _create_worksheet(self, name):
        spreadsheet_properties = {
            'properties': {'title': name }
        }
        spreadsheet = self.service.spreadsheets().create(
            body=spreadsheet_properties, fields='spreadsheetId').execute()
        return spreadsheet.get('spreadsheetId')

    def _write_sheet(self, worksheet_id, sheet_name, data):
        self.service.spreadsheets().values().append(
            spreadsheetId=worksheet_id, valueInputOption='RAW', range=sheet_name, body={'values': data}).execute()

    def _delete_sheet(self, worksheet_id, sheet_id):
        request = {'requests': [{
            'deleteSheet': {'sheetId': sheet_id}
        }]}
        self.service.spreadsheets().batchUpdate(spreadsheetId=worksheet_id, body=request).execute()

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