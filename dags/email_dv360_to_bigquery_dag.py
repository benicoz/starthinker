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

DV360 Report Emailed To BigQuery

Pulls a DV360 Report from a gMail email into BigQuery.

The person executing this recipe must be the recipient of the email.
Schedule a DV360 report to be sent to an email like <b>UNDEFINED</b>.
Or set up a redirect rule to forward a report you already receive.
The report can be sent as an attachment or a link.
Ensure this recipe runs after the report is email daily.
Give a regular expression to match the email subject.
Configure the destination in BigQuery to write the data.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'email': '',  # Email address report was sent to.
  'auth_read': 'user',  # Credentials used for reading data.
  'subject': '.*',  # Regular expression to match subject. Double escape backslashes.
  'dataset': '',  # Existing dataset in BigQuery.
  'table': '',  # Name of table to be written to.
  'dbm_schema': '[]',  # Schema provided in JSON list format or empty list.
  'is_incremental_load': False,  # Append report data to table based on date column, de-duplicates.
}

TASKS = [
  {
    'email': {
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'read': {
        'from': 'noreply-dv360@google.com',
        'subject': {
          'field': {
            'description': 'Regular expression to match subject. Double escape backslashes.',
            'kind': 'string',
            'name': 'subject',
            'order': 2,
            'default': '.*'
          }
        },
        'out': {
          'bigquery': {
            'schema': {
              'field': {
                'description': 'Schema provided in JSON list format or empty list.',
                'kind': 'json',
                'name': 'dbm_schema',
                'order': 5,
                'default': '[]'
              }
            },
            'dataset': {
              'field': {
                'description': 'Existing dataset in BigQuery.',
                'kind': 'string',
                'name': 'dataset',
                'order': 3,
                'default': ''
              }
            },
            'table': {
              'field': {
                'description': 'Name of table to be written to.',
                'kind': 'string',
                'name': 'table',
                'order': 4,
                'default': ''
              }
            },
            'is_incremental_load': {
              'field': {
                'description': 'Append report data to table based on date column, de-duplicates.',
                'kind': 'boolean',
                'name': 'is_incremental_load',
                'order': 6,
                'default': False
              }
            }
          }
        },
        'to': {
          'field': {
            'description': 'Email address report was sent to.',
            'kind': 'string',
            'name': 'email',
            'order': 1,
            'default': ''
          }
        },
        'link': 'https://storage.googleapis.com/.*',
        'attachment': '.*'
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('email_dv360_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
