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

Line Item To BigQuery Via Query

Move using an Id query.

Specify the query that will pull the lineitem ids to download.
Specify the dataset and table where the lineitems will be written.
The schema will match <a href='https://developers.google.com/bid-manager/guides/entity-write/format' target='_blank'>Entity Write Format</a>.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'id_dataset': '',
  'id_query': 'SELECT * FROM `Dataset.Table`;',
  'id_legacy': False,
  'destination_dataset': '',
  'destination_table': '',
}

TASKS = [
  {
    'lineitem': {
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'read': {
        'line_items': {
          'single_cell': True,
          'bigquery': {
            'query': {
              'field': {
                'order': 2,
                'kind': 'string',
                'name': 'id_query',
                'default': 'SELECT * FROM `Dataset.Table`;'
              }
            },
            'legacy': {
              'field': {
                'order': 3,
                'kind': 'boolean',
                'name': 'id_legacy',
                'default': False
              }
            },
            'dataset': {
              'field': {
                'order': 1,
                'kind': 'string',
                'name': 'id_dataset',
                'default': ''
              }
            }
          }
        },
        'out': {
          'bigquery': {
            'table': {
              'field': {
                'order': 5,
                'kind': 'string',
                'name': 'destination_table',
                'default': ''
              }
            },
            'dataset': {
              'field': {
                'order': 4,
                'kind': 'string',
                'name': 'destination_dataset',
                'default': ''
              }
            }
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('lineitem_read_to_bigquery_via_query', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
