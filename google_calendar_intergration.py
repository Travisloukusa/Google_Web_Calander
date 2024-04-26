import os
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scope needed for the Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """Authenticate and create the service for Google Calendar."""
    creds = None
    client_secrets_file = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(service, event):
    """Create an event on the Google Calendar."""
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event_result.get('htmlLink')}")

def load_events_from_json(json_data):
    """Load events from a JSON string and create them on the calendar."""
    service = authenticate_google_calendar()
    assignments = json.loads(json_data)
    for assignment in assignments:
        due_date = datetime.strptime(assignment['Due Date'], '%b %d, %Y %I:%M %p')
        event = {
            'summary': assignment['Title'],
            'description': assignment['Class'],
            'start': {
                'dateTime': due_date.isoformat(),
                'timeZone': 'America/Chicago',
            },
            'end': {
                'dateTime': (due_date + timedelta(hours=1)).isoformat(),
                'timeZone': 'America/Chicago',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }
        create_event(service, event)

if __name__ == '__main__':
    pass
