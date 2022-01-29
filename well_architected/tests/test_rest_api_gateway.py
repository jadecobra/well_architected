from tests.utilities import TestTemplates, true, false


class TestRestAPIGateway(TestTemplates):

    def test_rest_api_gateway(self):
        self.assert_template_equal(
            'LambdaRestAPIGateway',
            {
  "Resources": {
    "helloAPILogs01DC10B3": {
      "Type": "AWS::Logs::LogGroup",
      "Properties": {
        "RetentionInDays": 731
      },
      "UpdateReplacePolicy": "Retain",
      "DeletionPolicy": "Retain"
    },
    "LambdaAPIGateway527FD988": {
      "Type": "AWS::ApiGateway::RestApi",
      "Properties": {
        "EndpointConfiguration": {
          "Types": [
            "REGIONAL"
          ]
        },
        "Name": "hello"
      }
    },
    "LambdaAPIGatewayCloudWatchRoleA621D6AA": {
      "Type": "AWS::IAM::Role",
      "Properties": {
        "AssumeRolePolicyDocument": {
          "Statement": [
            {
              "Action": "sts:AssumeRole",
              "Effect": "Allow",
              "Principal": {
                "Service": "apigateway.amazonaws.com"
              }
            }
          ],
          "Version": "2012-10-17"
        },
        "ManagedPolicyArns": [
          {
            "Fn::Join": [
              "",
              [
                "arn:",
                {
                  "Ref": "AWS::Partition"
                },
                ":iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
              ]
            ]
          }
        ]
      }
    },
    "LambdaAPIGatewayAccount80C6550F": {
      "Type": "AWS::ApiGateway::Account",
      "Properties": {
        "CloudWatchRoleArn": {
          "Fn::GetAtt": [
            "LambdaAPIGatewayCloudWatchRoleA621D6AA",
            "Arn"
          ]
        }
      },
      "DependsOn": [
        "LambdaAPIGateway527FD988"
      ]
    },
    "LambdaAPIGatewayDeploymentE937914C5c746fc97cfebd293610d5e7f299055c": {
      "Type": "AWS::ApiGateway::Deployment",
      "Properties": {
        "RestApiId": {
          "Ref": "LambdaAPIGateway527FD988"
        },
        "Description": "Automatically created by the RestApi construct"
      },
      "DependsOn": [
        "LambdaAPIGatewayhelloGET71776088",
        "LambdaAPIGatewayhello24FCF180"
      ]
    },
    "LambdaAPIGatewayDeploymentStageprod74ACA052": {
      "Type": "AWS::ApiGateway::Stage",
      "Properties": {
        "RestApiId": {
          "Ref": "LambdaAPIGateway527FD988"
        },
        "AccessLogSetting": {
          "DestinationArn": {
            "Fn::GetAtt": [
              "helloAPILogs01DC10B3",
              "Arn"
            ]
          },
          "Format": "$context.identity.sourceIp $context.identity.caller $context.identity.user [$context.requestTime] \"$context.httpMethod $context.resourcePath $context.protocol\" $context.status $context.responseLength $context.requestId"
        },
        "DeploymentId": {
          "Ref": "LambdaAPIGatewayDeploymentE937914C5c746fc97cfebd293610d5e7f299055c"
        },
        "MethodSettings": [
          {
            "DataTraceEnabled": false,
            "HttpMethod": "*",
            "ResourcePath": "/*",
            "ThrottlingBurstLimit": 200,
            "ThrottlingRateLimit": 100
          }
        ],
        "StageName": "prod"
      },
      "DependsOn": [
        "LambdaAPIGatewayAccount80C6550F"
      ]
    },
    "LambdaAPIGatewayhello24FCF180": {
      "Type": "AWS::ApiGateway::Resource",
      "Properties": {
        "ParentId": {
          "Fn::GetAtt": [
            "LambdaAPIGateway527FD988",
            "RootResourceId"
          ]
        },
        "PathPart": "hello",
        "RestApiId": {
          "Ref": "LambdaAPIGateway527FD988"
        }
      }
    },
    "LambdaAPIGatewayhelloGETApiPermissionLambdaRestAPIGatewayLambdaAPIGateway33BA6F57GEThello1DD4CFC3": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::ImportValue": "LambdaFunction:ExportsOutputFnGetAtthitcounterLambdaFunctionB862C182Arn3B74EE41"
        },
        "Principal": "apigateway.amazonaws.com",
        "SourceArn": {
          "Fn::Join": [
            "",
            [
              "arn:",
              {
                "Ref": "AWS::Partition"
              },
              ":execute-api:",
              {
                "Ref": "AWS::Region"
              },
              ":",
              {
                "Ref": "AWS::AccountId"
              },
              ":",
              {
                "Ref": "LambdaAPIGateway527FD988"
              },
              "/",
              {
                "Ref": "LambdaAPIGatewayDeploymentStageprod74ACA052"
              },
              "/GET/hello"
            ]
          ]
        }
      }
    },
    "LambdaAPIGatewayhelloGETApiPermissionTestLambdaRestAPIGatewayLambdaAPIGateway33BA6F57GEThello193DFB32": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::ImportValue": "LambdaFunction:ExportsOutputFnGetAtthitcounterLambdaFunctionB862C182Arn3B74EE41"
        },
        "Principal": "apigateway.amazonaws.com",
        "SourceArn": {
          "Fn::Join": [
            "",
            [
              "arn:",
              {
                "Ref": "AWS::Partition"
              },
              ":execute-api:",
              {
                "Ref": "AWS::Region"
              },
              ":",
              {
                "Ref": "AWS::AccountId"
              },
              ":",
              {
                "Ref": "LambdaAPIGateway527FD988"
              },
              "/test-invoke-stage/GET/hello"
            ]
          ]
        }
      }
    },
    "LambdaAPIGatewayhelloGET71776088": {
      "Type": "AWS::ApiGateway::Method",
      "Properties": {
        "HttpMethod": "GET",
        "ResourceId": {
          "Ref": "LambdaAPIGatewayhello24FCF180"
        },
        "RestApiId": {
          "Ref": "LambdaAPIGateway527FD988"
        },
        "AuthorizationType": "NONE",
        "Integration": {
          "IntegrationHttpMethod": "POST",
          "IntegrationResponses": [
            {
              "ResponseParameters": {
                "method.response.header.Access-Control-Allow-Origin": "'*'"
              },
              "StatusCode": "200"
            }
          ],
          "Type": "AWS",
          "Uri": {
            "Fn::Join": [
              "",
              [
                "arn:",
                {
                  "Ref": "AWS::Partition"
                },
                ":apigateway:",
                {
                  "Ref": "AWS::Region"
                },
                ":lambda:path/2015-03-31/functions/",
                {
                  "Fn::ImportValue": "LambdaFunction:ExportsOutputFnGetAtthitcounterLambdaFunctionB862C182Arn3B74EE41"
                },
                "/invocations"
              ]
            ]
          }
        },
        "MethodResponses": [
          {
            "ResponseParameters": {
              "method.response.header.Access-Control-Allow-Origin": true
            },
            "StatusCode": "200"
          }
        ]
      }
    },
    "ApiGatewayCloudWatchErrorTopicB01304FE": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic"
      }
    },
    "ApiGatewayCloudWatchAPIGateway4XXErrors11FFC618F": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Fn::ImportValue": "SnsTopic:ExportsOutputRefSnsTopic2C1570A4EE4BCC49"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "m1/m2*100",
            "Id": "expr_1",
            "Label": "% API Gateway 4xx Errors"
          },
          {
            "Id": "m1",
            "Label": "4XX Errors",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "ApiId",
                    "Value": {
                      "Ref": "LambdaAPIGateway527FD988"
                    }
                  }
                ],
                "MetricName": "4XXError",
                "Namespace": "AWS/ApiGateway"
              },
              "Period": 300,
              "Stat": "Sum",
              "Unit": "Count"
            },
            "ReturnData": false
          },
          {
            "Id": "m2",
            "Label": "# Requests",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "ApiId",
                    "Value": {
                      "Ref": "LambdaAPIGateway527FD988"
                    }
                  }
                ],
                "MetricName": "Count",
                "Namespace": "AWS/ApiGateway"
              },
              "Period": 300,
              "Stat": "Sum",
              "Unit": "Count"
            },
            "ReturnData": false
          }
        ],
        "Threshold": 1,
        "TreatMissingData": "notBreaching"
      }
    },
    "ApiGatewayCloudWatchAPIGateway5XXErrors0001B6606": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Fn::ImportValue": "SnsTopic:ExportsOutputRefSnsTopic2C1570A4EE4BCC49"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Id": "m1",
            "Label": "5XX Errors",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "ApiId",
                    "Value": {
                      "Ref": "LambdaAPIGateway527FD988"
                    }
                  }
                ],
                "MetricName": "5XXError",
                "Namespace": "AWS/ApiGateway"
              },
              "Period": 900,
              "Stat": "p99",
              "Unit": "Count"
            },
            "ReturnData": true
          }
        ],
        "Threshold": 0,
        "TreatMissingData": "notBreaching"
      }
    },
    "ApiGatewayCloudWatchAPIp99latencyalarm1s6545CFD1": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Fn::ImportValue": "SnsTopic:ExportsOutputRefSnsTopic2C1570A4EE4BCC49"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Id": "m1",
            "Label": "API GW Latency",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "ApiId",
                    "Value": {
                      "Ref": "LambdaAPIGateway527FD988"
                    }
                  }
                ],
                "MetricName": "Latency",
                "Namespace": "AWS/ApiGateway"
              },
              "Period": 900,
              "Stat": "p99",
              "Unit": "Count"
            },
            "ReturnData": true
          }
        ],
        "Threshold": 1000,
        "TreatMissingData": "notBreaching"
      }
    },
    "ApiGatewayCloudWatchCloudWatchDashBoard278188F3": {
      "Type": "AWS::CloudWatch::Dashboard",
      "Properties": {
        "DashboardBody": {
          "Fn::Join": [
            "",
            [
              "{\"widgets\":[{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Requests\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[\"AWS/ApiGateway\",\"Count\",\"ApiId\",\"",
              {
                "Ref": "LambdaAPIGateway527FD988"
              },
              "\",{\"label\":\"# Requests\",\"period\":900,\"stat\":\"Sum\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"API GW Latency\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/ApiGateway\",\"Latency\",\"ApiId\",\"",
              {
                "Ref": "LambdaAPIGateway527FD988"
              },
              "\",{\"label\":\"API Latency p50\",\"period\":900,\"stat\":\"p50\"}],[\"AWS/ApiGateway\",\"Latency\",\"ApiId\",\"",
              {
                "Ref": "LambdaAPIGateway527FD988"
              },
              "\",{\"label\":\"API Latency p90\",\"period\":900,\"stat\":\"p90\"}],[\"AWS/ApiGateway\",\"Latency\",\"ApiId\",\"",
              {
                "Ref": "LambdaAPIGateway527FD988"
              },
              "\",{\"label\":\"API Latency p99\",\"period\":900,\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"API GW Errors\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/ApiGateway\",\"4XXError\",\"ApiId\",\"",
              {
                "Ref": "LambdaAPIGateway527FD988"
              },
              "\",{\"label\":\"4XX Errors\",\"period\":900,\"stat\":\"Sum\"}],[\"AWS/ApiGateway\",\"5XXError\",\"ApiId\",\"",
              {
                "Ref": "LambdaAPIGateway527FD988"
              },
              "\",{\"label\":\"5XX Errors\",\"period\":900,\"stat\":\"Sum\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      }
    }
  },
  "Outputs": {
    "LambdaAPIGatewayEndpoint5DC258E1": {
      "Value": {
        "Fn::Join": [
          "",
          [
            "https://",
            {
              "Ref": "LambdaAPIGateway527FD988"
            },
            ".execute-api.",
            {
              "Ref": "AWS::Region"
            },
            ".",
            {
              "Ref": "AWS::URLSuffix"
            },
            "/",
            {
              "Ref": "LambdaAPIGatewayDeploymentStageprod74ACA052"
            },
            "/"
          ]
        ]
      }
    },
    "ExportsOutputRefLambdaAPIGateway527FD98828FC969E": {
      "Value": {
        "Ref": "LambdaAPIGateway527FD988"
      },
      "Export": {
        "Name": "LambdaRestAPIGateway:ExportsOutputRefLambdaAPIGateway527FD98828FC969E"
      }
    },
    "ExportsOutputRefLambdaAPIGatewayDeploymentStageprod74ACA052509E0E94": {
      "Value": {
        "Ref": "LambdaAPIGatewayDeploymentStageprod74ACA052"
      },
      "Export": {
        "Name": "LambdaRestAPIGateway:ExportsOutputRefLambdaAPIGatewayDeploymentStageprod74ACA052509E0E94"
      }
    }
  }
}
        )