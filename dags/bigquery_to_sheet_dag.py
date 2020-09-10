###########################################################################
#
#  Copyright 2020 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

'''
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer from open source:

    pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu	
    l) Install All

--------------------------------------------------------------

Query to Sheet

Copy the contents of a query into a Google Sheet.

Specify the sheet and the query.
Leave range blank or set to A2 to insert one line down.
The range is cleared before the sheet is written to.
To select a table use SELECT * FROM table.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'sheet': '',  # Either sheet url or sheet name.
  'auth_read': 'user',  # Credentials used for reading data.
  'tab': '',  # Name of the tab where to put the data.
  'range': '',  # Range in the sheet to place the data, leave blank for whole sheet.
  'dataset': '',  # Existing BigQuery dataset.
  'query': '',  # Query to pull data from the table.
  'legacy': True,  # Use Legacy SQL
}

TASKS = [
  {
    'bigquery': {
      'from': {
        'legacy': {
          'field': {
            'description': 'Use Legacy SQL',
            'kind': 'boolean',
            'name': 'legacy',
            'order': 6,
            'default': True
          }
        },
        'auth': 'service',
        'query': {
          'field': {
            'description': 'Query to pull data from the table.',
            'kind': 'text',
            'name': 'query',
            'order': 5,
            'default': ''
          }
        },
        'dataset': {
          'field': {
            'description': 'Existing BigQuery dataset.',
            'kind': 'string',
            'name': 'dataset',
            'order': 4,
            'default': ''
          }
        }
      },
      'to': {
        'sheet': {
          'field': {
            'description': 'Either sheet url or sheet name.',
            'kind': 'string',
            'name': 'sheet',
            'order': 1,
            'default': ''
          }
        },
        'tab': {
          'field': {
            'description': 'Name of the tab where to put the data.',
            'kind': 'string',
            'name': 'tab',
            'order': 2,
            'default': ''
          }
        },
        'range': {
          'field': {
            'description': 'Range in the sheet to place the data, leave blank for whole sheet.',
            'kind': 'string',
            'name': 'range',
            'order': 3,
            'default': ''
          }
        }
      },
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('bigquery_to_sheet', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
