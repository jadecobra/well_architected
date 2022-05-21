import aws_cdk
import constructs
import well_architected_lambda
import well_architected_dynamodb_table
import well_architected_rest_api

from aws_cdk import (
    aws_apigateway as api_gateway,
    aws_dynamodb as dynamodb,
    aws_events,
    aws_events_targets as targets,
    aws_iam as iam,
    aws_sns as sns,
)

class EventBridgeCircuitBreaker(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        error_topic = sns.Topic(
            self, id,
            display_name='ErrorTopic'
        )

        expiration_time_sort_key = dynamodb.Attribute(
            name="ExpirationTime",
            type=dynamodb.AttributeType.NUMBER
        )

        error_records = well_architected_dynamodb_table.DynamoDBTableConstruct(
            self, 'CircuitBreaker',
            error_topic=error_topic,
            partition_key=dynamodb.Attribute(
                name="RequestID",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=expiration_time_sort_key,
            time_to_live_attribute='ExpirationTime',
        ).dynamodb_table

        error_records.add_global_secondary_index(
            index_name='UrlIndex',
            partition_key=dynamodb.Attribute(
                name="SiteUrl",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=expiration_time_sort_key
        )

        environment_variables = dict(ERROR_RECORDS=error_records.table_name)

        webservice = well_architected_lambda.create_python_lambda_function(
            self, function_name='webservice',
            error_topic=error_topic,
            environment_variables=environment_variables,
            duration=20,
        )

        error_lambda = well_architected_lambda.create_python_lambda_function(
            self, function_name='error',
            error_topic=error_topic,
            environment_variables=environment_variables,
            duration=3,
        )

        error_records.grant_read_data(webservice)
        error_records.grant_write_data(error_lambda)

        webservice.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                resources=['*'],
                actions=['events:PutEvents']
            )
        )

        error_rule = aws_events.Rule(
            self, 'webserviceErrorRule',
            description='Failed Webservice Call',
            event_pattern=aws_events.EventPattern(
                source=['cdkpatterns.eventbridge.circuitbreaker'],
                detail_type=['httpcall'],
                detail={
                    "status": ["fail"]
                }
            )
        )

        error_rule.add_target(targets.LambdaFunction(handler=error_lambda))

        well_architected_rest_api.LambdaRestAPIGatewayConstruct(
            self, 'CircuitBreakerGateway',
            lambda_function=webservice,
            error_topic=error_topic,
        )