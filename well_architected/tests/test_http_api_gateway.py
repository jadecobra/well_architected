from tests.utilities import TestTemplates, true, false


class TestHTTPAPI(TestTemplates):

    def test_http_api_gateway(self):
        self.assert_template_equal(
            'LambdaHttpApiGateway',
            {
  "Resources": {
    "HttpAPI8D545486": {
      "Type": "AWS::ApiGatewayV2::Api",
      "Properties": {
        "Name": "HttpAPI",
        "ProtocolType": "HTTP"
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/HttpAPI/Resource"
      }
    },
    "HttpAPIDefaultRouteHTTPLambdaIntegrationPermission5A5BB64C": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::ImportValue": "LambdaFunction:ExportsOutputFnGetAttLambdaFunctionBF21E41FArn8BD9CD14"
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
                "Ref": "HttpAPI8D545486"
              },
              "/*/*"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/HttpAPI/DefaultRoute/HTTPLambdaIntegration-Permission"
      }
    },
    "HttpAPIDefaultRouteHTTPLambdaIntegration7A40D12F": {
      "Type": "AWS::ApiGatewayV2::Integration",
      "Properties": {
        "ApiId": {
          "Ref": "HttpAPI8D545486"
        },
        "IntegrationType": "AWS_PROXY",
        "IntegrationUri": {
          "Fn::ImportValue": "LambdaFunction:ExportsOutputFnGetAttLambdaFunctionBF21E41FArn8BD9CD14"
        },
        "PayloadFormatVersion": "2.0"
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/HttpAPI/DefaultRoute/HTTPLambdaIntegration/Resource"
      }
    },
    "HttpAPIDefaultRouteF9949FE6": {
      "Type": "AWS::ApiGatewayV2::Route",
      "Properties": {
        "ApiId": {
          "Ref": "HttpAPI8D545486"
        },
        "RouteKey": "$default",
        "AuthorizationType": "NONE",
        "Target": {
          "Fn::Join": [
            "",
            [
              "integrations/",
              {
                "Ref": "HttpAPIDefaultRouteHTTPLambdaIntegration7A40D12F"
              }
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/HttpAPI/DefaultRoute/Resource"
      }
    },
    "HttpAPIDefaultStage1BC7D78F": {
      "Type": "AWS::ApiGatewayV2::Stage",
      "Properties": {
        "ApiId": {
          "Ref": "HttpAPI8D545486"
        },
        "StageName": "$default",
        "AutoDeploy": true
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/HttpAPI/DefaultStage/Resource"
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
                      "Ref": "HttpAPI8D545486"
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
                      "Ref": "HttpAPI8D545486"
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
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/ApiGatewayCloudWatch/API Gateway 4XX Errors > 1%/Resource"
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
                      "Ref": "HttpAPI8D545486"
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
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/ApiGatewayCloudWatch/API Gateway 5XX Errors > 0/Resource"
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
                      "Ref": "HttpAPI8D545486"
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
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/ApiGatewayCloudWatch/API p99 latency alarm >= 1s/Resource"
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
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"# Requests\",\"period\":900,\"stat\":\"Sum\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"API GW Latency\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/ApiGateway\",\"Latency\",\"ApiId\",\"",
              {
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"API Latency p50\",\"period\":900,\"stat\":\"p50\"}],[\"AWS/ApiGateway\",\"Latency\",\"ApiId\",\"",
              {
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"API Latency p90\",\"period\":900,\"stat\":\"p90\"}],[\"AWS/ApiGateway\",\"Latency\",\"ApiId\",\"",
              {
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"API Latency p99\",\"period\":900,\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"API GW Errors\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/ApiGateway\",\"4XXError\",\"ApiId\",\"",
              {
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"4XX Errors\",\"period\":900,\"stat\":\"Sum\"}],[\"AWS/ApiGateway\",\"5XXError\",\"ApiId\",\"",
              {
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"5XX Errors\",\"period\":900,\"stat\":\"Sum\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/ApiGatewayCloudWatch/CloudWatchDashBoard/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/12OwY7CMAxEv4V7MBQOXEFwWE5U5QtMEtosbVIlDhWK8u/UQWKlPc0ba8Z2BdV2B+vFHqewlOqxStJ5DelKKB/i6GwgHyWJ491eIo2xUKODi15q5jmiDBlns+AVCUfTIukJX88NpB+i8TAaDrKwbVwkXehsSbceucyBf/YvN//SllsFsuhxuCmEeVBrP5gQuCF7F9WEJDtIhx79UG4WOGHobg694tHX5JxF/aLO2dUWqjVUi99gzNJHS2bQ0Hz0DQxdpwggAQAA"
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/CDKMetadata/Default"
      },
      "Condition": "CDKMetadataAvailable"
    }
  },
  "Outputs": {
    "HTTPAPIUrl": {
      "Value": {
        "Fn::Join": [
          "",
          [
            "https://",
            {
              "Ref": "HttpAPI8D545486"
            },
            ".execute-api.",
            {
              "Ref": "AWS::Region"
            },
            ".",
            {
              "Ref": "AWS::URLSuffix"
            },
            "/"
          ]
        ]
      }
    }
  },
  "Conditions": {
    "CDKMetadataAvailable": {
      "Fn::Or": [
        {
          "Fn::Or": [
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "af-south-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ap-east-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ap-northeast-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ap-northeast-2"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ap-south-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ap-southeast-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ap-southeast-2"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ca-central-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "cn-north-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "cn-northwest-1"
              ]
            }
          ]
        },
        {
          "Fn::Or": [
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "eu-central-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "eu-north-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "eu-south-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "eu-west-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "eu-west-2"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "eu-west-3"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "me-south-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "sa-east-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "us-east-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "us-east-2"
              ]
            }
          ]
        },
        {
          "Fn::Or": [
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "us-west-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "us-west-2"
              ]
            }
          ]
        }
      ]
    }
  }
}
        )