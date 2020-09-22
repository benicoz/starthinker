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

CM To Sheets

Move existing CM report into a Sheet tab.

Specify an account id.
Specify either report name or report id to move a report.
The most recent valid file will be moved to the sheet.
Schema is pulled from the official CM specification.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'account': '',
  'report_id': '',
  'report_name': '',
  'sheet': '',
  'tab': '',
}

TASKS = [
  {
    'dcm': {
      'report': {
        'name': {
          'field': {
            'order': 4,
            'kind': 'string',
            'name': 'report_name',
            'default': ''
          }
        },
        'report_id': {
          'field': {
            'order': 3,
            'kind': 'integer',
            'name': 'report_id',
            'default': ''
          }
        },
        'account': {
          'field': {
            'order': 2,
            'kind': 'integer',
            'name': 'account',
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
      },
      'out': {
        'sheets': {
          'range': 'A1',
          'sheet': {
            'field': {
              'order': 5,
              'kind': 'string',
              'name': 'sheet',
              'default': ''
            }
          },
          'tab': {
            'field': {
              'order': 6,
              'kind': 'string',
              'name': 'tab',
              'default': ''
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dcm_to_sheets', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
