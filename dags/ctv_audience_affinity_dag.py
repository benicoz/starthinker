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

cTV Inventory Availability Dashboard

The cTV Audience Affinity dashboard is designed to give clients insights into which cTV apps their audiences have a high affinity for using.  The goal of this dashboard is to provide some assistance with the lack of audience targeting for cTV within DV360.

Find instructions and recommendations for this dashboard <a href="https://docs.google.com/document/d/120kcR9OrS4hGdTxRK0Ig2koNmm6Gl7sH0L6U56N0SAM/view?usp=sharing" target="_blank">here</a>

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'dataset': '',  # BigQuery Dataset where all data will live.
  'recipe_project': '',  # Project where BigQuery dataset will be created.
  'partner_id': '',  # DV360 Partner id.
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'recipe_name': '',  # Name of document to deploy to.
  'audience_ids': '',  # Comma separated list of Audience Ids
}

TASKS = [
  {
    'drive': {
      'auth': 'user',
      'copy': {
        'source': 'https://docs.google.com/spreadsheets/d/1PPPk2b4gGJHNgQ4hXLiTKzH8pRIdlF5fNy9VCw1v7tM/',
        'destination': {
          'field': {
            'description': 'Name of document to deploy to.',
            'name': 'recipe_name',
            'kind': 'string',
            'order': 1,
            'prefix': 'cTV App Match Table ',
            'default': ''
          }
        }
      }
    }
  },
  {
    'dataset': {
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
          'description': 'BigQuery Dataset where all data will live.',
          'kind': 'string',
          'name': 'dataset',
          'order': 3,
          'default': ''
        }
      }
    }
  },
  {
    'dbm': {
      'auth': 'user',
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery Dataset where all data will live.',
              'kind': 'string',
              'name': 'dataset',
              'order': 3,
              'default': ''
            }
          },
          'table': 'us_country_app',
          'schema': [
            {
              'type': 'STRING',
              'name': 'app_url',
              'mode': 'NULLABLE'
            },
            {
              'type': 'STRING',
              'name': 'impressions',
              'mode': 'NULLABLE'
            },
            {
              'type': 'STRING',
              'name': 'uniques',
              'mode': 'NULLABLE'
            }
          ]
        }
      },
      'report': {
        'body': {
          'metadata': {
            'title': {
              'field': {
                'name': 'recipe_name',
                'prefix': 'us_country_app_',
                'kind': 'string'
              }
            },
            'dataRange': 'LAST_30_DAYS',
            'format': 'CSV',
            'sendNotification': False
          },
          'timezoneCode': 'America/Los_Angeles',
          'kind': 'doubleclickbidmanager#query',
          'schedule': {
            'endTimeMs': 7983727200000,
            'frequency': 'DAILY',
            'nextRunMinuteOfDay': 0,
            'nextRunTimezoneCode': 'America/Los_Angeles'
          },
          'params': {
            'filters': [
              {
                'type': 'FILTER_PARTNER',
                'value': {
                  'field': {
                    'order': 1,
                    'name': 'partner_id',
                    'description': 'DV360 Partner id.',
                    'kind': 'integer'
                  }
                }
              },
              {
                'type': 'FILTER_INVENTORY_FORMAT',
                'value': 'VIDEO'
              },
              {
                'type': 'FILTER_COUNTRY',
                'value': 'US'
              }
            ],
            'type': 'TYPE_INVENTORY_AVAILABILITY',
            'groupBys': [
              'FILTER_APP_URL'
            ],
            'metrics': [
              'METRIC_BID_REQUESTS',
              'METRIC_UNIQUE_VISITORS_COOKIES'
            ],
            'includeInviteData': True
          }
        }
      }
    }
  },
  {
    'dbm': {
      'auth': 'user',
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery Dataset where all data will live.',
              'kind': 'string',
              'name': 'dataset',
              'order': 3,
              'default': ''
            }
          },
          'table': 'us_country_baseline',
          'schema': [
            {
              'type': 'STRING',
              'name': 'impressions',
              'mode': 'NULLABLE'
            },
            {
              'type': 'STRING',
              'name': 'uniques',
              'mode': 'NULLABLE'
            }
          ]
        }
      },
      'report': {
        'body': {
          'metadata': {
            'title': {
              'field': {
                'name': 'recipe_name',
                'prefix': 'us_country_baseline_',
                'kind': 'string'
              }
            },
            'dataRange': 'LAST_30_DAYS',
            'format': 'CSV',
            'sendNotification': False
          },
          'timezoneCode': 'America/Los_Angeles',
          'kind': 'doubleclickbidmanager#query',
          'schedule': {
            'endTimeMs': 7983727200000,
            'frequency': 'DAILY',
            'nextRunMinuteOfDay': 0,
            'nextRunTimezoneCode': 'America/Los_Angeles'
          },
          'params': {
            'filters': [
              {
                'type': 'FILTER_PARTNER',
                'value': {
                  'field': {
                    'order': 1,
                    'name': 'partner_id',
                    'description': 'DV360 Partner id.',
                    'kind': 'integer'
                  }
                }
              },
              {
                'type': 'FILTER_COUNTRY',
                'value': 'US'
              }
            ],
            'type': 'TYPE_INVENTORY_AVAILABILITY',
            'includeInviteData': True,
            'metrics': [
              'METRIC_BID_REQUESTS',
              'METRIC_UNIQUE_VISITORS_COOKIES'
            ]
          }
        }
      }
    }
  },
  {
    'dbm': {
      'auth': 'user',
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery Dataset where all data will live.',
              'kind': 'string',
              'name': 'dataset',
              'order': 3,
              'default': ''
            }
          },
          'table': 'us_audience_baseline',
          'schema': [
            {
              'type': 'STRING',
              'name': 'user_list',
              'mode': 'NULLABLE'
            },
            {
              'type': 'STRING',
              'name': 'impressions',
              'mode': 'NULLABLE'
            },
            {
              'type': 'STRING',
              'name': 'uniques',
              'mode': 'NULLABLE'
            }
          ]
        }
      },
      'report': {
        'filters': {
          'FILTER_USER_LIST': {
            'values': {
              'field': {
                'order': 2,
                'name': 'audience_ids',
                'description': 'Comma separated list of Audience Ids',
                'kind': 'integer_list'
              }
            },
            'single_cell': True
          }
        },
        'body': {
          'metadata': {
            'title': {
              'field': {
                'name': 'recipe_name',
                'prefix': 'us_audience_baseline_',
                'kind': 'string'
              }
            },
            'dataRange': 'LAST_30_DAYS',
            'format': 'CSV',
            'sendNotification': False
          },
          'timezoneCode': 'America/Los_Angeles',
          'kind': 'doubleclickbidmanager#query',
          'schedule': {
            'endTimeMs': 7983727200000,
            'frequency': 'DAILY',
            'nextRunMinuteOfDay': 0,
            'nextRunTimezoneCode': 'America/Los_Angeles'
          },
          'params': {
            'filters': [
              {
                'type': 'FILTER_PARTNER',
                'value': {
                  'field': {
                    'order': 1,
                    'name': 'partner_id',
                    'description': 'DV360 Partner id.',
                    'kind': 'integer'
                  }
                }
              },
              {
                'type': 'FILTER_COUNTRY',
                'value': 'US'
              }
            ],
            'type': 'TYPE_INVENTORY_AVAILABILITY',
            'groupBys': [
              'FILTER_AUDIENCE_LIST'
            ],
            'metrics': [
              'METRIC_BID_REQUESTS',
              'METRIC_UNIQUE_VISITORS_COOKIES'
            ],
            'includeInviteData': True
          }
        }
      }
    }
  },
  {
    'dbm': {
      'auth': 'user',
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery Dataset where all data will live.',
              'kind': 'string',
              'name': 'dataset',
              'order': 3,
              'default': ''
            }
          },
          'table': 'us_audience_app',
          'schema': [
            {
              'type': 'STRING',
              'name': 'app_url',
              'mode': 'NULLABLE'
            },
            {
              'type': 'STRING',
              'name': 'user_list',
              'mode': 'NULLABLE'
            },
            {
              'type': 'STRING',
              'name': 'impressions',
              'mode': 'NULLABLE'
            },
            {
              'type': 'STRING',
              'name': 'uniques',
              'mode': 'NULLABLE'
            }
          ]
        }
      },
      'report': {
        'filters': {
          'FILTER_USER_LIST': {
            'values': {
              'field': {
                'order': 2,
                'name': 'audience_ids',
                'description': 'Comma separated list of Audience Ids',
                'kind': 'integer_list'
              }
            },
            'single_cell': True
          }
        },
        'body': {
          'metadata': {
            'title': {
              'field': {
                'name': 'recipe_name',
                'prefix': 'us_audience_app_',
                'kind': 'string'
              }
            },
            'dataRange': 'LAST_30_DAYS',
            'format': 'CSV',
            'sendNotification': False
          },
          'timezoneCode': 'America/Los_Angeles',
          'kind': 'doubleclickbidmanager#query',
          'schedule': {
            'endTimeMs': 7983727200000,
            'frequency': 'DAILY',
            'nextRunMinuteOfDay': 0,
            'nextRunTimezoneCode': 'America/Los_Angeles'
          },
          'params': {
            'filters': [
              {
                'type': 'FILTER_PARTNER',
                'value': {
                  'field': {
                    'order': 1,
                    'name': 'partner_id',
                    'description': 'DV360 Partner id.',
                    'kind': 'integer'
                  }
                }
              },
              {
                'type': 'FILTER_INVENTORY_FORMAT',
                'value': 'VIDEO'
              },
              {
                'type': 'FILTER_COUNTRY',
                'value': 'US'
              }
            ],
            'type': 'TYPE_INVENTORY_AVAILABILITY',
            'groupBys': [
              'FILTER_APP_URL',
              'FILTER_AUDIENCE_LIST'
            ],
            'metrics': [
              'METRIC_BID_REQUESTS',
              'METRIC_UNIQUE_VISITORS_COOKIES'
            ],
            'includeInviteData': True
          }
        }
      }
    }
  },
  {
    'sheets': {
      'tab': 'data',
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'description': 'BigQuery Dataset where all data will live.',
              'name': 'dataset',
              'kind': 'string'
            }
          },
          'table': 'CTV_App_Lookup',
          'schema': [
            {
              'type': 'STRING',
              'name': 'Publisher_Name',
              'mode': 'NULLABLE'
            },
            {
              'type': 'STRING',
              'name': 'CTV_App_name',
              'mode': 'NULLABLE'
            }
          ]
        },
        'auth': {
          'field': {
            'description': 'Credentials used for writing data.',
            'kind': 'authentication',
            'name': 'auth_write',
            'order': 1,
            'default': 'service'
          }
        }
      },
      'header': True,
      'sheet': {
        'field': {
          'description': 'Name of document to deploy to.',
          'name': 'recipe_name',
          'kind': 'string',
          'order': 1,
          'prefix': 'cTV App Match Table ',
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
      'range': 'A:Z'
    }
  },
  {
    'bigquery': {
      'from': {
        'legacy': False,
        'parameters': [
          {
            'field': {
              'description': 'Project where BigQuery dataset will be created.',
              'name': 'recipe_project',
              'kind': 'string'
            }
          },
          {
            'field': {
              'description': 'Place where tables will be written in BigQuery.',
              'name': 'dataset',
              'kind': 'string'
            }
          },
          {
            'field': {
              'description': 'Project where BigQuery dataset will be created.',
              'name': 'recipe_project',
              'kind': 'string'
            }
          },
          {
            'field': {
              'description': 'Place where tables will be written in BigQuery.',
              'name': 'dataset',
              'kind': 'string'
            }
          },
          {
            'field': {
              'description': 'Project where BigQuery dataset will be created.',
              'name': 'recipe_project',
              'kind': 'string'
            }
          },
          {
            'field': {
              'description': 'Place where tables will be written in BigQuery.',
              'name': 'dataset',
              'kind': 'string'
            }
          },
          {
            'field': {
              'description': 'Project where BigQuery dataset will be created.',
              'name': 'recipe_project',
              'kind': 'string'
            }
          },
          {
            'field': {
              'description': 'Place where tables will be written in BigQuery.',
              'name': 'dataset',
              'kind': 'string'
            }
          },
          {
            'field': {
              'description': 'Project where BigQuery dataset will be created.',
              'name': 'recipe_project',
              'kind': 'string'
            }
          },
          {
            'field': {
              'description': 'Place where tables will be written in BigQuery.',
              'name': 'dataset',
              'kind': 'string'
            }
          },
          {
            'field': {
              'description': 'Project where BigQuery dataset will be created.',
              'name': 'recipe_project',
              'kind': 'string'
            }
          },
          {
            'field': {
              'description': 'Place where tables will be written in BigQuery.',
              'name': 'dataset',
              'kind': 'string'
            }
          }
        ],
        'query': "SELECT    audience_app.app_url,    audience_app.ctv_app_name,  IF    (audience_app.app_url LIKE '%Android%'      OR audience_app.app_url LIKE '%iOS',      'App',      'Domain') AS app_or_domain,    audience_app.user_list AS audience_list,    audience_app.Potential_Impressions AS audience_app_impressions,    audience_app.Unique_Cookies_With_Impressions AS audience_app_uniques,    audience_baseline.Potential_Impressions AS audience_baseline_impressions,    audience_baseline.Unique_Cookies_With_Impressions AS audience_baseline_uniques,    country_app.Potential_Impressions AS country_app_impressions,    country_app.Unique_Cookies_With_Impressions AS country_app_uniques,    country_baseline.Potential_Impressions AS country_baseline_impressions,    country_baseline.Unique_Cookies_With_Impressions AS country_baseline_uniques,    ((audience_app.Unique_Cookies_With_Impressions/NULLIF(audience_baseline.Unique_Cookies_With_Impressions,          0))/NULLIF((country_app.Unique_Cookies_With_Impressions/NULLIF(CAST(country_baseline.Unique_Cookies_With_Impressions AS int64),            0)),        0))*100 AS affinity_index  FROM (    SELECT      user_list,      CAST(      IF        (impressions LIKE '%< 1000%',          0,          CAST(impressions AS int64)) AS int64) AS potential_impressions,      CAST(      IF        (uniques LIKE '%< 100%',          0,          CAST(uniques AS int64)) AS int64) AS unique_cookies_with_impressions    FROM      `[PARAMETER].[PARAMETER].us_audience_baseline` ) AS audience_baseline  JOIN (    SELECT      ctv_app.CTV_App_name AS ctv_app_name,      user_list,      app_url,      CAST(      IF        (impressions LIKE '%< 1000%',          0,          CAST(impressions AS int64)) AS int64) AS potential_impressions,      CAST(      IF        (uniques LIKE '%< 1000%',          0,          CAST(uniques AS int64)) AS int64) AS unique_cookies_with_impressions    FROM      `[PARAMETER].[PARAMETER].us_audience_app` AS a    LEFT JOIN      `[PARAMETER].[PARAMETER].CTV_App_Lookup` AS ctv_app    ON      a.app_url = ctv_app.Publisher_Name ) AS audience_app  ON    audience_baseline.user_list = audience_app.user_list  LEFT JOIN (    SELECT      app_url,      CAST(      IF        (CAST(impressions AS STRING) LIKE '%< 1000%',          0,          CAST(impressions AS int64)) AS int64) AS Potential_Impressions,      CAST(      IF        (CAST(uniques AS STRING) LIKE '%< 1000%',          0,          CAST(uniques AS int64)) AS int64) AS Unique_Cookies_With_Impressions    FROM      `[PARAMETER].[PARAMETER].us_country_app` ) AS country_app  ON    country_app.app_url = audience_app.app_url  CROSS JOIN (    SELECT      CAST(      IF        (CAST(impressions AS STRING) LIKE '%< 1000%',          0,          CAST(impressions AS int64)) AS int64) AS Potential_Impressions,      CAST(      IF        (CAST(uniques AS STRING) LIKE '%< 1000%',          0,          CAST(uniques AS int64)) AS int64) AS Unique_Cookies_With_Impressions    FROM      `[PARAMETER].[PARAMETER].us_country_baseline` ) AS country_baseline"
      },
      'to': {
        'dataset': {
          'field': {
            'description': 'BigQuery Dataset where all data will live.',
            'name': 'dataset',
            'kind': 'string'
          }
        },
        'table': 'final_table'
      },
      'description': 'The query to join all the IAR reports into an Affinity Index.',
      'auth': {
        'field': {
          'description': 'Credentials used for writing data.',
          'kind': 'authentication',
          'name': 'auth_write',
          'order': 1,
          'default': 'service'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('ctv_audience_affinity', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
