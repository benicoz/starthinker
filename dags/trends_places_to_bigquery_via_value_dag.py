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

Trends Places To BigQuery Via Values

Move using hard coded WOEID values.

Provide <a href='https://apps.twitter.com/' target='_blank'>Twitter credentials</a>.
Provide a comma delimited list of WOEIDs.
Specify BigQuery dataset and table to write API call results to.
Writes: WOEID, Name, Url, Promoted_Content, Query, Tweet_Volume
Note Twitter API is rate limited to 15 requests per 15 minutes. So keep WOEID lists short.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_write': 'service',  # Credentials used for writing data.
  'secret': '',
  'key': '',
  'woeids': [],
  'destination_dataset': '',
  'destination_table': '',
}

TASKS = [
  {
    'twitter': {
      'secret': {
        'field': {
          'order': 1,
          'kind': 'string',
          'name': 'secret',
          'default': ''
        }
      },
      'trends': {
        'places': {
          'values': {
            'field': {
              'order': 3,
              'kind': 'integer_list',
              'name': 'woeids',
              'default': [
              ]
            }
          },
          'single_cell': True
        }
      },
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_write',
          'description': 'Credentials used for writing data.',
          'default': 'service'
        }
      },
      'key': {
        'field': {
          'order': 2,
          'kind': 'string',
          'name': 'key',
          'default': ''
        }
      },
      'out': {
        'bigquery': {
          'table': {
            'field': {
              'order': 7,
              'kind': 'string',
              'name': 'destination_table',
              'default': ''
            }
          },
          'dataset': {
            'field': {
              'order': 6,
              'kind': 'string',
              'name': 'destination_dataset',
              'default': ''
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('trends_places_to_bigquery_via_value', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
