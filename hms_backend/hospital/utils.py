from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_calendar_event(summary, start_time, end_time):

    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)

    creds = flow.run_local_server(port=0)

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        }
    }

    service.events().insert(calendarId='primary', body=event).execute()