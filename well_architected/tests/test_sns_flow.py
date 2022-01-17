from tests.utilities import TestTemplates, true, false


class TestSnsFlow(TestTemplates):

    def test_sns_flow(self):
        self.assert_template_equal(
            'SnsFlow',
            {
  "Resources": {
    "TheXRayTracerSnsTopicCCE2005E": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "The XRay Tracer CDK Pattern Topic"
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/TheXRayTracerSnsTopic/Resource"
      }
    },
    "snspublishErrorTopic167BD513": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic",
        "TopicName": "ErrorTopic"
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/ErrorTopic/Resource"
      }
    },
    "snspublishLambdaFunctionServiceRoleBE8DA9C2": {
      "Type": "AWS::IAM::Role",
      "Properties": {
        "AssumeRolePolicyDocument": {
          "Statement": [
            {
              "Action": "sts:AssumeRole",
              "Effect": "Allow",
              "Principal": {
                "Service": "lambda.amazonaws.com"
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
                ":iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
              ]
            ]
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/LambdaFunction/ServiceRole/Resource"
      }
    },
    "snspublishLambdaFunctionServiceRoleDefaultPolicyD927DA99": {
      "Type": "AWS::IAM::Policy",
      "Properties": {
        "PolicyDocument": {
          "Statement": [
            {
              "Action": [
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords"
              ],
              "Effect": "Allow",
              "Resource": "*"
            },
            {
              "Action": "sns:Publish",
              "Effect": "Allow",
              "Resource": {
                "Ref": "TheXRayTracerSnsTopicCCE2005E"
              }
            }
          ],
          "Version": "2012-10-17"
        },
        "PolicyName": "snspublishLambdaFunctionServiceRoleDefaultPolicyD927DA99",
        "Roles": [
          {
            "Ref": "snspublishLambdaFunctionServiceRoleBE8DA9C2"
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/LambdaFunction/ServiceRole/DefaultPolicy/Resource"
      }
    },
    "snspublishLambdaFunctionE7ECD8FF": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameters3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5S3BucketD2320349"
          },
          "S3Key": {
            "Fn::Join": [
              "",
              [
                {
                  "Fn::Select": [
                    0,
                    {
                      "Fn::Split": [
                        "||",
                        {
                          "Ref": "AssetParameters3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5S3VersionKey91D22072"
                        }
                      ]
                    }
                  ]
                },
                {
                  "Fn::Select": [
                    1,
                    {
                      "Fn::Split": [
                        "||",
                        {
                          "Ref": "AssetParameters3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5S3VersionKey91D22072"
                        }
                      ]
                    }
                  ]
                }
              ]
            ]
          }
        },
        "Role": {
          "Fn::GetAtt": [
            "snspublishLambdaFunctionServiceRoleBE8DA9C2",
            "Arn"
          ]
        },
        "Environment": {
          "Variables": {
            "TOPIC_ARN": {
              "Ref": "TheXRayTracerSnsTopicCCE2005E"
            }
          }
        },
        "Handler": "sns_publish.handler",
        "Runtime": "python3.8",
        "Timeout": 60,
        "TracingConfig": {
          "Mode": "Active"
        }
      },
      "DependsOn": [
        "snspublishLambdaFunctionServiceRoleDefaultPolicyD927DA99",
        "snspublishLambdaFunctionServiceRoleBE8DA9C2"
      ],
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/LambdaFunction/Resource",
        "aws:asset:path": "asset.3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Code"
      }
    },
    "snspublishLambdaFunctionAllowInvokeSnsFlowSNSTopicACE071C85E8FF116": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "snspublishLambdaFunctionE7ECD8FF",
            "Arn"
          ]
        },
        "Principal": "sns.amazonaws.com",
        "SourceArn": {
          "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
        }
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/LambdaFunction/AllowInvoke:SnsFlowSNSTopicACE071C8"
      }
    },
    "snspublishLambdaFunctionSNSTopic766E3B5D": {
      "Type": "AWS::SNS::Subscription",
      "Properties": {
        "Protocol": "lambda",
        "TopicArn": {
          "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
        },
        "Endpoint": {
          "Fn::GetAtt": [
            "snspublishLambdaFunctionE7ECD8FF",
            "Arn"
          ]
        },
        "Region": {
          "Fn::Select": [
            3,
            {
              "Fn::Split": [
                ":",
                {
                  "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
                }
              ]
            }
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/LambdaFunction/SNSTopic/Resource"
      }
    },
    "snspublishLambdainvocationErrors2194CE9F8": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "snspublishErrorTopic167BD513"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "e / invocations * 100",
            "Id": "expr_1",
            "Label": "% of invocations that errored, last 5 mins"
          },
          {
            "Id": "invocations",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "snspublishLambdaFunctionE7ECD8FF"
                    }
                  }
                ],
                "MetricName": "Invocations",
                "Namespace": "AWS/Lambda"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          },
          {
            "Id": "e",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "snspublishLambdaFunctionE7ECD8FF"
                    }
                  }
                ],
                "MetricName": "Errors",
                "Namespace": "AWS/Lambda"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          }
        ],
        "Threshold": 2,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/Lambda invocation Errors > 2%/Resource"
      }
    },
    "snspublishLambdap99LongDuration1s0547A3C8": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "snspublishErrorTopic167BD513"
          }
        ],
        "DatapointsToAlarm": 1,
        "Dimensions": [
          {
            "Name": "FunctionName",
            "Value": {
              "Ref": "snspublishLambdaFunctionE7ECD8FF"
            }
          }
        ],
        "ExtendedStatistic": "p99",
        "MetricName": "Duration",
        "Namespace": "AWS/Lambda",
        "Period": 300,
        "Threshold": 1000,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/Lambda p99 Long Duration (>1s)/Resource"
      }
    },
    "snspublishLambdaThrottledinvocations22BAA7401": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "snspublishErrorTopic167BD513"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "t / (invocations + t) * 100",
            "Id": "expr_1",
            "Label": "throttled requests % in last 30 mins"
          },
          {
            "Id": "invocations",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "snspublishLambdaFunctionE7ECD8FF"
                    }
                  }
                ],
                "MetricName": "Invocations",
                "Namespace": "AWS/Lambda"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          },
          {
            "Id": "t",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "snspublishLambdaFunctionE7ECD8FF"
                    }
                  }
                ],
                "MetricName": "Throttles",
                "Namespace": "AWS/Lambda"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          }
        ],
        "Threshold": 2,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/Lambda Throttled invocations >2%/Resource"
      }
    },
    "snspublishCloudWatchDashBoard5DA9CB77": {
      "Type": "AWS::CloudWatch::Dashboard",
      "Properties": {
        "DashboardBody": {
          "Fn::Join": [
            "",
            [
              "{\"widgets\":[{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Error %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"% of invocations that errored, last 5 mins\",\"expression\":\"e / invocations * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"e\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Duration\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"p50\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"p90\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"throttled requests % in last 30 mins\",\"expression\":\"t / (invocations + t) * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"t\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/CloudWatchDashBoard/Resource"
      }
    },
    "snssubscribeErrorTopicB1BEEA4E": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic",
        "TopicName": "ErrorTopic"
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/ErrorTopic/Resource"
      }
    },
    "snssubscribeLambdaFunctionServiceRole6068C33F": {
      "Type": "AWS::IAM::Role",
      "Properties": {
        "AssumeRolePolicyDocument": {
          "Statement": [
            {
              "Action": "sts:AssumeRole",
              "Effect": "Allow",
              "Principal": {
                "Service": "lambda.amazonaws.com"
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
                ":iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
              ]
            ]
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/LambdaFunction/ServiceRole/Resource"
      }
    },
    "snssubscribeLambdaFunctionServiceRoleDefaultPolicy7C3E54A8": {
      "Type": "AWS::IAM::Policy",
      "Properties": {
        "PolicyDocument": {
          "Statement": [
            {
              "Action": [
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords"
              ],
              "Effect": "Allow",
              "Resource": "*"
            }
          ],
          "Version": "2012-10-17"
        },
        "PolicyName": "snssubscribeLambdaFunctionServiceRoleDefaultPolicy7C3E54A8",
        "Roles": [
          {
            "Ref": "snssubscribeLambdaFunctionServiceRole6068C33F"
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/LambdaFunction/ServiceRole/DefaultPolicy/Resource"
      }
    },
    "snssubscribeLambdaFunctionE84E36B6": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameters3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5S3BucketD2320349"
          },
          "S3Key": {
            "Fn::Join": [
              "",
              [
                {
                  "Fn::Select": [
                    0,
                    {
                      "Fn::Split": [
                        "||",
                        {
                          "Ref": "AssetParameters3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5S3VersionKey91D22072"
                        }
                      ]
                    }
                  ]
                },
                {
                  "Fn::Select": [
                    1,
                    {
                      "Fn::Split": [
                        "||",
                        {
                          "Ref": "AssetParameters3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5S3VersionKey91D22072"
                        }
                      ]
                    }
                  ]
                }
              ]
            ]
          }
        },
        "Role": {
          "Fn::GetAtt": [
            "snssubscribeLambdaFunctionServiceRole6068C33F",
            "Arn"
          ]
        },
        "Handler": "sns_subscribe.handler",
        "Runtime": "python3.8",
        "Timeout": 60,
        "TracingConfig": {
          "Mode": "Active"
        }
      },
      "DependsOn": [
        "snssubscribeLambdaFunctionServiceRoleDefaultPolicy7C3E54A8",
        "snssubscribeLambdaFunctionServiceRole6068C33F"
      ],
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/LambdaFunction/Resource",
        "aws:asset:path": "asset.3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Code"
      }
    },
    "snssubscribeLambdaFunctionAllowInvokeSnsFlowTheXRayTracerSnsTopic2E3ECD150E3B6B47": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "snssubscribeLambdaFunctionE84E36B6",
            "Arn"
          ]
        },
        "Principal": "sns.amazonaws.com",
        "SourceArn": {
          "Ref": "TheXRayTracerSnsTopicCCE2005E"
        }
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/LambdaFunction/AllowInvoke:SnsFlowTheXRayTracerSnsTopic2E3ECD15"
      }
    },
    "snssubscribeLambdaFunctionTheXRayTracerSnsTopicC8EDB3DC": {
      "Type": "AWS::SNS::Subscription",
      "Properties": {
        "Protocol": "lambda",
        "TopicArn": {
          "Ref": "TheXRayTracerSnsTopicCCE2005E"
        },
        "Endpoint": {
          "Fn::GetAtt": [
            "snssubscribeLambdaFunctionE84E36B6",
            "Arn"
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/LambdaFunction/TheXRayTracerSnsTopic/Resource"
      }
    },
    "snssubscribeLambdainvocationErrors2AA7BE787": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "snssubscribeErrorTopicB1BEEA4E"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "e / invocations * 100",
            "Id": "expr_1",
            "Label": "% of invocations that errored, last 5 mins"
          },
          {
            "Id": "invocations",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "snssubscribeLambdaFunctionE84E36B6"
                    }
                  }
                ],
                "MetricName": "Invocations",
                "Namespace": "AWS/Lambda"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          },
          {
            "Id": "e",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "snssubscribeLambdaFunctionE84E36B6"
                    }
                  }
                ],
                "MetricName": "Errors",
                "Namespace": "AWS/Lambda"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          }
        ],
        "Threshold": 2,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/Lambda invocation Errors > 2%/Resource"
      }
    },
    "snssubscribeLambdap99LongDuration1s207F8DA0": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "snssubscribeErrorTopicB1BEEA4E"
          }
        ],
        "DatapointsToAlarm": 1,
        "Dimensions": [
          {
            "Name": "FunctionName",
            "Value": {
              "Ref": "snssubscribeLambdaFunctionE84E36B6"
            }
          }
        ],
        "ExtendedStatistic": "p99",
        "MetricName": "Duration",
        "Namespace": "AWS/Lambda",
        "Period": 300,
        "Threshold": 1000,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/Lambda p99 Long Duration (>1s)/Resource"
      }
    },
    "snssubscribeLambdaThrottledinvocations2104FA145": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "snssubscribeErrorTopicB1BEEA4E"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "t / (invocations + t) * 100",
            "Id": "expr_1",
            "Label": "throttled requests % in last 30 mins"
          },
          {
            "Id": "invocations",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "snssubscribeLambdaFunctionE84E36B6"
                    }
                  }
                ],
                "MetricName": "Invocations",
                "Namespace": "AWS/Lambda"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          },
          {
            "Id": "t",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "snssubscribeLambdaFunctionE84E36B6"
                    }
                  }
                ],
                "MetricName": "Throttles",
                "Namespace": "AWS/Lambda"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          }
        ],
        "Threshold": 2,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/Lambda Throttled invocations >2%/Resource"
      }
    },
    "snssubscribeCloudWatchDashBoard0367AF74": {
      "Type": "AWS::CloudWatch::Dashboard",
      "Properties": {
        "DashboardBody": {
          "Fn::Join": [
            "",
            [
              "{\"widgets\":[{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Error %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"% of invocations that errored, last 5 mins\",\"expression\":\"e / invocations * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"e\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Duration\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"p50\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"p90\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"throttled requests % in last 30 mins\",\"expression\":\"t / (invocations + t) * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"t\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/CloudWatchDashBoard/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/1WPwW7DIAyGn6V34jbKabe1nXaO0r2A47DGa4AKg6oK8e4LRJu2k7//57eNW2i7FzjsXvEhDU23fSLnNaRLQLqps7MSfKSgjiI6rOaV7VWdP22PHo0O2hcxaHHRky68tkwc2NmsysgkViB9uDtTed3gEkchz/cSK+4/XSMnFJ3VgmacENJ7tPST/cu99oZF6jJGA2lwS/1Erb1bmJ41Vykr6RosdwjUc1YNp0g3Hco6RYuL0wMDzZCOC3pTWjd4Q5lHh34q1q/IOav+GWZn9x20B2h3X8Lc+GgDGw3DVr8Bmdj8XGIBAAA="
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/CDKMetadata/Default"
      },
      "Condition": "CDKMetadataAvailable"
    }
  },
  "Parameters": {
    "AssetParameters3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5S3BucketD2320349": {
      "Type": "String",
      "Description": "S3 bucket for asset \"3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5\""
    },
    "AssetParameters3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5S3VersionKey91D22072": {
      "Type": "String",
      "Description": "S3 key for asset version \"3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5\""
    },
    "AssetParameters3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5ArtifactHash8698A4CE": {
      "Type": "String",
      "Description": "Artifact hash for asset \"3685b746731556d1122cc06e6f3359cf30955051fc855f65044eea29ab8780b5\""
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