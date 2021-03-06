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

Transparency Dashboard

Reports the percentage of CM impressions that can be attributed to a specific domain or application.  Allows diagnostic of which domains and apps are misconfigured by publisher resulting in underreporting.

Wait for <a href='https://console.cloud.google.com/bigquery?project=UNDEFINED&d=UNDEFINED' target='_blank'>BigQuery : UNDEFINED</a> : UNDEFINED : UNDEFINED</a> to be created.
Copy DataStudio <a href='https://datastudio.google.com/c/u/0/datasources/1Az6d9loAHo69GSIyKUfusrtyf_IDqTVs' target='_blank'>Transparency Combined KPI</a> and connect.
Copy DataStudio <a href='https://datastudio.google.com/c/u/0/reporting/1foircGRxgYCL_PR8gfdmYOleBacnPKwB/page/QCXj' target='_blank'>Transparency Breakdown</a>.
When prompted choose the new data source you just created.
Or give these intructions to the client, they will have to join the <a hre='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a>.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'recipe_project': '',  # Project where BigQuery dataset will be created.
  'recipe_name': '',  # Name of report in CM, should be unique.
  'recipe_slug': '',  # Name of Google BigQuery dataset to create.
  'dcm_account': '',  # CM account id of client.
  'dcm_advertisers': '',  # Comma delimited list of CM advertiser ids.
}

TASKS = [
  {
    'dataset': {
      'hour': [
        1
      ],
      'dataset': {
        'field': {
          'order': 1,
          'kind': 'string',
          'name': 'recipe_slug',
          'description': 'Name of Google BigQuery dataset to create.',
          'default': ''
        }
      },
      'auth': 'service'
    }
  },
  {
    'dcm': {
      'hour': [
        2
      ],
      'auth': 'user',
      'report': {
        'filters': {
          'dfa:advertiser': {
            'values': {
              'field': {
                'order': 3,
                'kind': 'integer_list',
                'name': 'dcm_advertisers',
                'description': 'Comma delimited list of CM advertiser ids.'
              }
            }
          }
        },
        'account': {
          'field': {
            'order': 2,
            'kind': 'integer',
            'name': 'dcm_account',
            'description': 'CM account id of client.',
            'default': ''
          }
        },
        'body': {
          'format': 'CSV',
          'name': {
            'field': {
              'kind': 'string',
              'name': 'recipe_name',
              'description': 'Name of report in CM, unique.',
              'prefix': 'Transparency App For '
            }
          },
          'type': 'STANDARD',
          'criteria': {
            'metricNames': [
              'dfa:impressions'
            ],
            'dimensions': [
              {
                'name': 'dfa:advertiser'
              },
              {
                'name': 'dfa:advertiserId'
              },
              {
                'name': 'dfa:campaign'
              },
              {
                'name': 'dfa:campaignId'
              },
              {
                'name': 'dfa:siteId'
              },
              {
                'name': 'dfa:site'
              },
              {
                'name': 'dfa:adType'
              },
              {
                'name': 'dfa:environment'
              },
              {
                'name': 'dfa:appId'
              },
              {
                'name': 'dfa:app'
              }
            ],
            'dateRange': {
              'relativeDateRange': 'PREVIOUS_MONTH'
            }
          },
          'schedule': {
            'every': 1,
            'runsOnDayOfMonth': 'DAY_OF_MONTH',
            'repeats': 'MONTHLY',
            'active': True
          }
        }
      }
    }
  },
  {
    'dcm': {
      'hour': [
        2
      ],
      'auth': 'user',
      'report': {
        'filters': {
          'dfa:advertiser': {
            'values': {
              'field': {
                'order': 3,
                'kind': 'integer_list',
                'name': 'dcm_advertisers',
                'description': 'Comma delimited list of CM advertiser ids.'
              }
            }
          }
        },
        'account': {
          'field': {
            'order': 2,
            'kind': 'integer',
            'name': 'dcm_account',
            'description': 'CM account id of client.',
            'default': ''
          }
        },
        'body': {
          'format': 'CSV',
          'name': {
            'field': {
              'kind': 'string',
              'name': 'recipe_name',
              'description': 'Name of report in CM, unique.',
              'prefix': 'Transparency Domain For '
            }
          },
          'type': 'STANDARD',
          'criteria': {
            'metricNames': [
              'dfa:verificationVerifiableImpressions'
            ],
            'dimensions': [
              {
                'name': 'dfa:advertiser'
              },
              {
                'name': 'dfa:advertiserId'
              },
              {
                'name': 'dfa:campaign'
              },
              {
                'name': 'dfa:campaignId'
              },
              {
                'name': 'dfa:site'
              },
              {
                'name': 'dfa:siteId'
              },
              {
                'name': 'dfa:adType'
              },
              {
                'name': 'dfa:domain'
              }
            ],
            'dateRange': {
              'relativeDateRange': 'PREVIOUS_MONTH'
            }
          },
          'schedule': {
            'every': 1,
            'runsOnDayOfMonth': 'DAY_OF_MONTH',
            'repeats': 'MONTHLY',
            'active': True
          }
        }
      }
    }
  },
  {
    'dcm': {
      'hour': [
        4
      ],
      'auth': 'user',
      'out': {
        'bigquery': {
          'table': 'Transparency_Domain_KPI',
          'dataset': {
            'field': {
              'order': 1,
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Name of Google BigQuery dataset to create.',
              'default': ''
            }
          },
          'auth': 'service'
        }
      },
      'report': {
        'name': {
          'field': {
            'kind': 'string',
            'name': 'recipe_name',
            'description': 'Name of report in CM, should be unique.',
            'prefix': 'Transparency Domain For '
          }
        },
        'account': {
          'field': {
            'order': 2,
            'kind': 'integer',
            'name': 'dcm_account',
            'description': 'CM account id of client.',
            'default': ''
          }
        }
      }
    }
  },
  {
    'dcm': {
      'hour': [
        4
      ],
      'auth': 'user',
      'out': {
        'bigquery': {
          'table': 'Transparency_App_KPI',
          'dataset': {
            'field': {
              'order': 1,
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Name of Google BigQuery dataset to create.',
              'default': ''
            }
          },
          'auth': 'service'
        }
      },
      'report': {
        'name': {
          'field': {
            'kind': 'string',
            'name': 'recipe_name',
            'description': 'Name of report in CM, should be unique.',
            'prefix': 'Transparency App For '
          }
        },
        'account': {
          'field': {
            'order': 2,
            'kind': 'integer',
            'name': 'dcm_account',
            'description': 'CM account id of client.',
            'default': ''
          }
        }
      }
    }
  },
  {
    'bigquery': {
      'hour': [
        5
      ],
      'auth': 'user',
      'from': {
        'query': "With \r\nTransparent_Domains AS ( \r\n  SELECT\r\n    CONCAT(Advertiser, ' - ', CAST(Advertiser_Id AS STRING)) AS Advertiser,\r\n    CONCAT(Campaign, ' - ', CAST(Campaign_Id AS STRING)) AS Campaign,\r\n    CONCAT(Site_Dcm, ' - ', CAST(Site_Id_Dcm AS STRING)) AS Site,\r\n    Domain,\r\n    Ad_Type,\r\n    Verifiable_Impressions AS Impressions,\r\n    IF(Domain IS NOT NULL, Verifiable_Impressions, 0) AS Visible_Impressions,\r\n    IF(Domain IS NULL, Verifiable_Impressions, 0) AS Null_Impressions\r\n  FROM `[PARAMETER].[PARAMETER].Transparency_Domain_KPI`\r\n),\r\nTransparent_Apps AS ( \r\n  SELECT\r\n    CONCAT(Advertiser, ' - ', CAST(Advertiser_Id AS STRING)) AS Advertiser,\r\n    CONCAT(Campaign, ' - ', CAST(Campaign_Id AS STRING)) AS Campaign,\r\n    CONCAT(Site_Dcm, ' - ', CAST(Site_Id_Dcm AS STRING)) AS Site,\r\n    /*If(App IS NOT NULL, CONCAT(App, ' - ', CAST(App_Id AS STRING)), App_Id) AS App, */\r\n    CASE \r\n      WHEN App IS NOT NULL THEN CONCAT(App, ' - ', CAST(App_Id AS STRING))\r\n      WHEN App_Id IS NOT NULL THEN App_Id\r\n      ELSE NULL\r\n    END AS App,\r\n    Ad_Type,\r\n    Impressions,\r\n    IF(App IS NOT NULL OR App_ID IS NOT NULL, Impressions, 0) AS Visible_Impressions,\r\n    IF(App IS NULL AND App_Id IS NULL, Impressions, 0) AS Null_Impressions\r\n  FROM `[PARAMETER].[PARAMETER].Transparency_App_KPI`\r\n  WHERE Environment = 'App'\r\n),\r\nDomains_And_Apps AS (\r\n  SELECT \r\n    TD.Advertiser,\r\n    TD.Campaign,\r\n    TD.Site,\r\n    TD.Ad_Type,\r\n    TD.Domain,\r\n    TD.Impressions AS Domain_Impressions,\r\n    TD.Visible_Impressions AS Domain_Visible_Impressions,\r\n    TD.Null_Impressions AS Domain_Null_Impressions,\r\n    NULL AS App,\r\n    0 AS App_Impressions,\r\n    0 AS App_Visible_Impressions,\r\n    0 AS App_Null_Impressions\r\n  FROM Transparent_Domains AS TD\r\n  UNION ALL\r\n  SELECT \r\n    TA.Advertiser,\r\n    TA.Campaign,\r\n    TA.Site,\r\n    TA.Ad_Type,\r\n    NULL AS Domain,\r\n    0 AS Domain_Impressions,\r\n    0 AS Domain_Visible_Impressions,\r\n    0 AS Domain_Null_Impressions,\r\n    TA.App,\r\n    TA.Impressions AS App_Impressions,\r\n    TA.Visible_Impressions AS App_Visible_Impressions,\r\n    TA.Null_Impressions AS App_Null_Impressions\r\n  FROM Transparent_Apps AS TA\r\n)\r\n\r\n  SELECT\r\n    Advertiser,\r\n    Campaign,\r\n    Site,\r\n    COALESCE(Domain, App, '') AS Domain_Or_App,\r\n    Ad_Type,\r\n    CASE\r\n      WHEN App IS NOT NULL AND Domain IS NOT NULL THEN 'Both' /* SHOULD NOT HAPPEN */\r\n      WHEN App IS NOT NULL THEN 'App'\r\n      WHEN Domain IS NOT NULL Then 'Domain'\r\n      ELSE 'Neither'\r\n    END AS Category,\r\n\r\n    SUM(Domain_Impressions) AS Domain_Impressions,\r\n    SUM(Domain_Visible_Impressions) AS Domain_Visible_Impressions,\r\n    SUM(Domain_Null_Impressions) AS Domain_Null_Impressions,\r\n\r\n    SUM(App_Impressions) AS App_Impressions,\r\n    SUM(App_Visible_Impressions) AS App_Visible_Impressions,\r\n    SUM(App_Null_Impressions) AS App_Null_Impressions,\r\n\r\n    SUM(App_Impressions + Domain_Impressions) AS Impressions /* Could also be MAX as its always one or the other*/\r\n\r\n  FROM Domains_And_Apps\r\n  GROUP By 1,2,3,4,5,6",
        'parameters': [
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Project where BigQuery dataset will be created.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Place where tables will be written in BigQuery.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_project',
              'description': 'Project where BigQuery dataset will be created.'
            }
          },
          {
            'field': {
              'kind': 'string',
              'name': 'recipe_slug',
              'description': 'Place where tables will be written in BigQuery.'
            }
          }
        ],
        'legacy': False
      },
      'to': {
        'view': 'Transparency_Combined_KPI',
        'dataset': {
          'field': {
            'order': 1,
            'kind': 'string',
            'name': 'recipe_slug',
            'description': 'Name of Google BigQuery dataset to create.',
            'default': ''
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('transparency', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
