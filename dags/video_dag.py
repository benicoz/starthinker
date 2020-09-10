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

Video Overlay

Add images, text, and audio to videos.

Provide either a sheet or a BigQuery table.
Each video edit will be read from the sheet or table.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'sheet': '',  # Name or URL of sheet.
  'auth_read': 'user',  # Credentials used for reading data.
  'tab': '',  # Name of sheet tab.
  'project': '',  # Google Cloud Project Identifier.
  'dataset': '',  # Name of dataset.
  'table': '',  # Name of table.
}

TASKS = [
  {
    'sheets': {
      'template': {
        'sheet': 'https://docs.google.com/spreadsheets/d/1BXRHWz-1P3gNS92WZy-3sPZslU8aalXa8heOgygWEFs/edit#gid=0',
        'tab': 'Video'
      },
      'sheet': {
        'field': {
          'description': 'Name or URL of sheet.',
          'kind': 'string',
          'name': 'sheet',
          'order': 1,
          'default': ''
        }
      },
      'tab': {
        'field': {
          'description': 'Name of sheet tab.',
          'kind': 'string',
          'name': 'tab',
          'order': 2,
          'default': ''
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
      },
      '__comment__': 'Copy the tamplate sheet to the users sheet.  If it already exists, nothing happens.'
    }
  },
  {
    'video': {
      'bigquery': {
        'project': {
          'field': {
            'description': 'Google Cloud Project Identifier.',
            'kind': 'string',
            'name': 'project',
            'order': 3,
            'default': ''
          }
        },
        'dataset': {
          'field': {
            'description': 'Name of dataset.',
            'kind': 'string',
            'name': 'dataset',
            'order': 4,
            'default': ''
          }
        },
        'table': {
          'field': {
            'description': 'Name of table.',
            'kind': 'string',
            'name': 'table',
            'order': 5,
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
      },
      '__comment__': 'Read video effects and values from sheet and/or bigquery.',
      'sheets': {
        'sheet': {
          'field': {
            'description': 'Name or URL of sheet.',
            'kind': 'string',
            'name': 'sheet',
            'order': 1,
            'default': ''
          }
        },
        'tab': {
          'field': {
            'description': 'Name of sheet tab.',
            'kind': 'string',
            'name': 'tab',
            'order': 2,
            'default': ''
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('video', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
