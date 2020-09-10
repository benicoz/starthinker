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

DT To Table

Move data from a DT bucket into a BigQuery table.

Ensure your user has <a href='https://developers.google.com/doubleclick-advertisers/dtv2/getting-started' target='_blank'>access to the bucket</a>.
Provide the DT bucket name to read from.
Provide the path of the files to read.
Each file is synchronized to a unique table.  Use a view or aggregate select.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'bucket': '',  # Name of bucket where DT files are stored.
  'paths': [],  # List of prefixes to pull specific DT files.
  'days': 2,  # Number of days back to synchronize.
  'hours': 0,  # Number of hours back to synchronize.
  'dataset': '',  # Existing dataset in BigQuery.
}

TASKS = [
  {
    'dt': {
      'from': {
        'bucket': {
          'field': {
            'description': 'Name of bucket where DT files are stored.',
            'kind': 'string',
            'name': 'bucket',
            'order': 2,
            'default': ''
          }
        },
        'days': {
          'field': {
            'description': 'Number of days back to synchronize.',
            'kind': 'integer',
            'name': 'days',
            'order': 4,
            'default': 2
          }
        },
        'hours': {
          'field': {
            'description': 'Number of hours back to synchronize.',
            'kind': 'integer',
            'name': 'hours',
            'order': 5,
            'default': 0
          }
        },
        'paths': {
          'field': {
            'description': 'List of prefixes to pull specific DT files.',
            'kind': 'string_list',
            'name': 'paths',
            'order': 3,
            'default': [
            ]
          }
        }
      },
      'to': {
        'auth': {
          'field': {
            'description': 'Credentials used for writing data.',
            'kind': 'authentication',
            'name': 'auth_write',
            'order': 1,
            'default': 'service'
          }
        },
        'dataset': {
          'field': {
            'description': 'Existing dataset in BigQuery.',
            'kind': 'string',
            'name': 'dataset',
            'order': 6,
            'default': ''
          }
        }
      },
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 0,
          'default': 'user'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dt', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
