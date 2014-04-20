# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# For more information on the Calendar API you can visit:
#
#   https://developers.google.com/google-apps/calendar/firstapp
#
# For more information on the Calendar API Python library surface you
# can visit:
#
#   https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/
#
# For information on the Python Client Library visit:
#
#   https://developers.google.com/api-client-library/python/start/get_started
"""
You can also get help on all the command-line flags the program understands
by running:

  $ python sample.py --help

adapted from fun Google sample code by SDC
4/20/2014

"""

import argparse
import httplib2
import os
import sys
import pytz
import pprint
from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools
from datetime import datetime
from datetime import timedelta
import time

import SignQueue

UPDATE_INTERVAL = 600 # seconds

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])
#

# CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console:
# <https://cloud.google.com/console#/project/224204431984/apiui>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))

"""
things to do
credentials good for longer
https://developers.google.com/google-apps/calendar/v3/reference/events/list?hl=ja
"""

def formatEvent(event):
  return('%s %s'%(event['summary'],datetime.strptime(event['start']['dateTime'][:-6],'%Y-%m-%dT%H:%M:%S').strftime('%a %b %d %I:%M %p')))

def main(argv):
  # Parse the command-line flags.
  flags = parser.parse_args(argv[1:])

  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to the file.
  storage = file.Storage('sample.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(FLOW, storage, flags)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # Construct the service object for the interacting with the Calendar API.
  service = discovery.build('calendar', 'v3', http=http)
  # queue to put the sign messages on
  signQueue = SignQueue.SignQueue()

  try:
    easternTime = pytz.timezone('US/Eastern')
    calendar = service.calendars().get(calendarId='primary').execute()
#    print calendar['summary']

    page_token = None
    while True:
      now = datetime.now(tz=easternTime)
      timeMin = datetime(year=now.year, month=now.month, day=now.day, tzinfo=easternTime) 
      timeMin = timeMin.isoformat()
      timeMax = datetime(year=now.year, month=now.month, day=now.day, tzinfo=easternTime) + timedelta(days=14)
      timeMax = timeMax.isoformat()


      events = service.events().list(calendarId='primary',
                                     pageToken=page_token,
                                     timeMin = timeMin,
                                     timeMax = timeMax,
                                     maxResults = 5,
                                     singleEvents = True
                                   #  orderBy='startTime',
                                     ).execute()

      sortEvents = sorted(events['items'], key = lambda x: x['start']['dateTime'])
      #pprint.pprint(sortEvents)
      for event in sortEvents:
        print(formatEvent(event))
        signQueue.addMessage(message = formatEvent(event), life_time = UPDATE_INTERVAL - 10)  
      #page_token = events.get('nextPageToken')
      #if not page_token:
      #  break - we are not paging
      time.sleep(UPDATE_INTERVAL)
  except client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")

if __name__ == '__main__':
  main(sys.argv)
