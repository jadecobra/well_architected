from tests.utilities import TestTemplates, true, false


class TestSqsFlow(TestTemplates):

    def test_sqs_flow(self):
        self.assert_template_equal(
            'SqsFlow',
           {
  "Resources": {
    "RDSPublishQueue2BEA1A7F": {
      "Type": "AWS::SQS::Queue",
      "Properties": {
        "VisibilityTimeout": 300
      },
      "UpdateReplacePolicy": "Delete",
      "DeletionPolicy": "Delete",
      "Metadata": {
        "aws:cdk:path": "SqsFlow/RDSPublishQueue/Resource"
      }
    },
    "sqsErrorTopicC8E3DE0B": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic"
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs/ErrorTopic/Resource"
      }
    },
    "sqsLambdaFunctionServiceRole62789435": {
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
        "aws:cdk:path": "SqsFlow/sqs/LambdaFunction/ServiceRole/Resource"
      }
    },
    "sqsLambdaFunctionServiceRoleDefaultPolicyE4DD722B": {
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
              "Action": [
                "sqs:SendMessage",
                "sqs:GetQueueAttributes",
                "sqs:GetQueueUrl"
              ],
              "Effect": "Allow",
              "Resource": {
                "Fn::GetAtt": [
                  "RDSPublishQueue2BEA1A7F",
                  "Arn"
                ]
              }
            }
          ],
          "Version": "2012-10-17"
        },
        "PolicyName": "sqsLambdaFunctionServiceRoleDefaultPolicyE4DD722B",
        "Roles": [
          {
            "Ref": "sqsLambdaFunctionServiceRole62789435"
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs/LambdaFunction/ServiceRole/DefaultPolicy/Resource"
      }
    },
    "sqsLambdaFunctionDBCFBC0F": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameterscc629a1cbfb955ae6703ba4a9bf13234c83109279756439f1c139ce563d2667eS3BucketE9206EF0"
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
                          "Ref": "AssetParameterscc629a1cbfb955ae6703ba4a9bf13234c83109279756439f1c139ce563d2667eS3VersionKey8174EE0C"
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
                          "Ref": "AssetParameterscc629a1cbfb955ae6703ba4a9bf13234c83109279756439f1c139ce563d2667eS3VersionKey8174EE0C"
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
            "sqsLambdaFunctionServiceRole62789435",
            "Arn"
          ]
        },
        "Environment": {
          "Variables": {
            "SQS_URL": {
              "Ref": "RDSPublishQueue2BEA1A7F"
            }
          }
        },
        "Handler": "sqs.handler",
        "Runtime": "python3.8",
        "Timeout": 60,
        "TracingConfig": {
          "Mode": "Active"
        }
      },
      "DependsOn": [
        "sqsLambdaFunctionServiceRoleDefaultPolicyE4DD722B",
        "sqsLambdaFunctionServiceRole62789435"
      ],
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs/LambdaFunction/Resource",
        "aws:asset:path": "asset.cc629a1cbfb955ae6703ba4a9bf13234c83109279756439f1c139ce563d2667e",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Code"
      }
    },
    "sqsLambdaFunctionAllowInvokeXRayTracerSnsFanOutTopic4E706A091417C519": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "sqsLambdaFunctionDBCFBC0F",
            "Arn"
          ]
        },
        "Principal": "sns.amazonaws.com",
        "SourceArn": {
          "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
        }
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs/LambdaFunction/AllowInvoke:XRayTracerSnsFanOutTopic4E706A09"
      }
    },
    "sqsLambdaFunctionXRayTracerSnsFanOutTopic1D1F6839": {
      "Type": "AWS::SNS::Subscription",
      "Properties": {
        "Protocol": "lambda",
        "TopicArn": {
          "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
        },
        "Endpoint": {
          "Fn::GetAtt": [
            "sqsLambdaFunctionDBCFBC0F",
            "Arn"
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs/LambdaFunction/XRayTracerSnsFanOutTopic/Resource"
      }
    },
    "sqsLambdainvocationErrors2DA8BB648": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "sqsErrorTopicC8E3DE0B"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "errors / invocations * 100",
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
                      "Ref": "sqsLambdaFunctionDBCFBC0F"
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
            "Id": "errors",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "sqsLambdaFunctionDBCFBC0F"
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
        "aws:cdk:path": "SqsFlow/sqs/Lambda invocation Errors > 2%/Resource"
      }
    },
    "sqsLambdap99LongDuration1s7AB941BF": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "sqsErrorTopicC8E3DE0B"
          }
        ],
        "DatapointsToAlarm": 1,
        "Dimensions": [
          {
            "Name": "FunctionName",
            "Value": {
              "Ref": "sqsLambdaFunctionDBCFBC0F"
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
        "aws:cdk:path": "SqsFlow/sqs/Lambda p99 Long Duration (>1s)/Resource"
      }
    },
    "sqsLambdaThrottledinvocations2735F537D": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "sqsErrorTopicC8E3DE0B"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "throttles / (invocations + t) * 100",
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
                      "Ref": "sqsLambdaFunctionDBCFBC0F"
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
            "Id": "throttles",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "sqsLambdaFunctionDBCFBC0F"
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
        "aws:cdk:path": "SqsFlow/sqs/Lambda Throttled invocations >2%/Resource"
      }
    },
    "sqsCloudWatchDashBoardAC79C904": {
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
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"% of invocations that errored, last 5 mins\",\"expression\":\"errors / invocations * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "sqsLambdaFunctionDBCFBC0F"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Ref": "sqsLambdaFunctionDBCFBC0F"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"errors\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Duration\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "sqsLambdaFunctionDBCFBC0F"
              },
              "\",{\"stat\":\"p50\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "sqsLambdaFunctionDBCFBC0F"
              },
              "\",{\"stat\":\"p90\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "sqsLambdaFunctionDBCFBC0F"
              },
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"throttled requests % in last 30 mins\",\"expression\":\"throttles / (invocations + t) * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "sqsLambdaFunctionDBCFBC0F"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Ref": "sqsLambdaFunctionDBCFBC0F"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"throttles\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs/CloudWatchDashBoard/Resource"
      }
    },
    "sqssubscribeErrorTopicC4F29AB2": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic"
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs_subscribe/ErrorTopic/Resource"
      }
    },
    "sqssubscribeLambdaFunctionServiceRole7577D75B": {
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
        "aws:cdk:path": "SqsFlow/sqs_subscribe/LambdaFunction/ServiceRole/Resource"
      }
    },
    "sqssubscribeLambdaFunctionServiceRoleDefaultPolicy47D1F13D": {
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
              "Action": [
                "sqs:ReceiveMessage",
                "sqs:ChangeMessageVisibility",
                "sqs:GetQueueUrl",
                "sqs:DeleteMessage",
                "sqs:GetQueueAttributes"
              ],
              "Effect": "Allow",
              "Resource": {
                "Fn::GetAtt": [
                  "RDSPublishQueue2BEA1A7F",
                  "Arn"
                ]
              }
            }
          ],
          "Version": "2012-10-17"
        },
        "PolicyName": "sqssubscribeLambdaFunctionServiceRoleDefaultPolicy47D1F13D",
        "Roles": [
          {
            "Ref": "sqssubscribeLambdaFunctionServiceRole7577D75B"
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs_subscribe/LambdaFunction/ServiceRole/DefaultPolicy/Resource"
      }
    },
    "sqssubscribeLambdaFunction2B3EFD1F": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameters45a64ba94427aa8245e84b37bb9b08e693b04502538428e5ceab2adab6ff77c7S3BucketD999D6E8"
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
                          "Ref": "AssetParameters45a64ba94427aa8245e84b37bb9b08e693b04502538428e5ceab2adab6ff77c7S3VersionKey8DF23815"
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
                          "Ref": "AssetParameters45a64ba94427aa8245e84b37bb9b08e693b04502538428e5ceab2adab6ff77c7S3VersionKey8DF23815"
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
            "sqssubscribeLambdaFunctionServiceRole7577D75B",
            "Arn"
          ]
        },
        "Handler": "sqs_subscribe.handler",
        "Runtime": "python3.8",
        "Timeout": 60,
        "TracingConfig": {
          "Mode": "Active"
        }
      },
      "DependsOn": [
        "sqssubscribeLambdaFunctionServiceRoleDefaultPolicy47D1F13D",
        "sqssubscribeLambdaFunctionServiceRole7577D75B"
      ],
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs_subscribe/LambdaFunction/Resource",
        "aws:asset:path": "asset.45a64ba94427aa8245e84b37bb9b08e693b04502538428e5ceab2adab6ff77c7",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Code"
      }
    },
    "sqssubscribeLambdaFunctionSqsEventSourceSqsFlowRDSPublishQueueD1D2BBCF2F32E4E5": {
      "Type": "AWS::Lambda::EventSourceMapping",
      "Properties": {
        "FunctionName": {
          "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
        },
        "EventSourceArn": {
          "Fn::GetAtt": [
            "RDSPublishQueue2BEA1A7F",
            "Arn"
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs_subscribe/LambdaFunction/SqsEventSource:SqsFlowRDSPublishQueueD1D2BBCF/Resource"
      }
    },
    "sqssubscribeLambdainvocationErrors291E8D7B4": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "sqssubscribeErrorTopicC4F29AB2"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "errors / invocations * 100",
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
                      "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
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
            "Id": "errors",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
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
        "aws:cdk:path": "SqsFlow/sqs_subscribe/Lambda invocation Errors > 2%/Resource"
      }
    },
    "sqssubscribeLambdap99LongDuration1sD4FA6C78": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "sqssubscribeErrorTopicC4F29AB2"
          }
        ],
        "DatapointsToAlarm": 1,
        "Dimensions": [
          {
            "Name": "FunctionName",
            "Value": {
              "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
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
        "aws:cdk:path": "SqsFlow/sqs_subscribe/Lambda p99 Long Duration (>1s)/Resource"
      }
    },
    "sqssubscribeLambdaThrottledinvocations21C107A97": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "sqssubscribeErrorTopicC4F29AB2"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "throttles / (invocations + t) * 100",
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
                      "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
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
            "Id": "throttles",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
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
        "aws:cdk:path": "SqsFlow/sqs_subscribe/Lambda Throttled invocations >2%/Resource"
      }
    },
    "sqssubscribeCloudWatchDashBoard2D9A2251": {
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
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"% of invocations that errored, last 5 mins\",\"expression\":\"errors / invocations * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"errors\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Duration\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
              },
              "\",{\"stat\":\"p50\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
              },
              "\",{\"stat\":\"p90\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
              },
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"throttled requests % in last 30 mins\",\"expression\":\"throttles / (invocations + t) * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Ref": "sqssubscribeLambdaFunction2B3EFD1F"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"throttles\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs_subscribe/CloudWatchDashBoard/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/2WQwU7DMBBEv6V3Z9soJ260BW5IIeEHNs7Sukns4LWpKsv/TuwAqsRpZ549q7FLKKsH2G0e8cqF7IdtkMYShNahHMTRaHbWSyf2zOQWeFL6JI4fukaLEzmyyTTExltJSS+RXjlldBRpZeBPhvDmyefTLKJgvcB3MyuZ4Cpa37G0ak7ZRO99FCNOXY8QXryWvzfudU12UszJPX+Rdm0u9Irz/FP4P41C4QShMWOulmdtRiVveWFWS9WqwPR2hvwFi4eDlwO5AzIJORrfX9HJM4T9iHZK0VU8IZ87g7ZP6M/EGEV9c2ejtxWUOyg3F1aqsF47NRE06/wGpg+TAZYBAAA="
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/CDKMetadata/Default"
      },
      "Condition": "CDKMetadataAvailable"
    }
  },
  "Parameters": {
    "AssetParameterscc629a1cbfb955ae6703ba4a9bf13234c83109279756439f1c139ce563d2667eS3BucketE9206EF0": {
      "Type": "String",
      "Description": "S3 bucket for asset \"cc629a1cbfb955ae6703ba4a9bf13234c83109279756439f1c139ce563d2667e\""
    },
    "AssetParameterscc629a1cbfb955ae6703ba4a9bf13234c83109279756439f1c139ce563d2667eS3VersionKey8174EE0C": {
      "Type": "String",
      "Description": "S3 key for asset version \"cc629a1cbfb955ae6703ba4a9bf13234c83109279756439f1c139ce563d2667e\""
    },
    "AssetParameterscc629a1cbfb955ae6703ba4a9bf13234c83109279756439f1c139ce563d2667eArtifactHash68AAC9E4": {
      "Type": "String",
      "Description": "Artifact hash for asset \"cc629a1cbfb955ae6703ba4a9bf13234c83109279756439f1c139ce563d2667e\""
    },
    "AssetParameters45a64ba94427aa8245e84b37bb9b08e693b04502538428e5ceab2adab6ff77c7S3BucketD999D6E8": {
      "Type": "String",
      "Description": "S3 bucket for asset \"45a64ba94427aa8245e84b37bb9b08e693b04502538428e5ceab2adab6ff77c7\""
    },
    "AssetParameters45a64ba94427aa8245e84b37bb9b08e693b04502538428e5ceab2adab6ff77c7S3VersionKey8DF23815": {
      "Type": "String",
      "Description": "S3 key for asset version \"45a64ba94427aa8245e84b37bb9b08e693b04502538428e5ceab2adab6ff77c7\""
    },
    "AssetParameters45a64ba94427aa8245e84b37bb9b08e693b04502538428e5ceab2adab6ff77c7ArtifactHashBA433240": {
      "Type": "String",
      "Description": "Artifact hash for asset \"45a64ba94427aa8245e84b37bb9b08e693b04502538428e5ceab2adab6ff77c7\""
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