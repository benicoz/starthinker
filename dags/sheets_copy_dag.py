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

Sheet Copy

Copy tab from a sheet to a sheet.

Provide the full edit URL for both sheets.
Provide the tab name for both sheets.
The tab will only be copied if it does not already exist.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'from_sheet': '',
  'from_tab': '',
  'to_sheet': '',
  'to_tab': '',
}

TASKS = [
  {
    'sheets': {
      'sheet': {
        'field': {
          'order': 3,
          'kind': 'string',
          'name': 'to_sheet',
          'default': ''
        }
      },
      'tab': {
        'field': {
          'order': 4,
          'kind': 'string',
          'name': 'to_tab',
          'default': ''
        }
      },
      'template': {
        'sheet': {
          'field': {
            'order': 1,
            'kind': 'string',
            'name': 'from_sheet',
            'default': ''
          }
        },
        'tab': {
          'field': {
            'order': 2,
            'kind': 'string',
            'name': 'from_tab',
            'default': ''
          }
        }
      },
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('sheets_copy', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
