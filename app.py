import aws_cdk.core as cdk
import aws_cdk.aws_dynamodb as aws_dynamodb

import big_fan
import destined_lambda
import dynamodb_table
import event_bridge_atm
import event_bridge_circuit_breaker
import event_bridge_etl
import http_api
import lambda_circuit_breaker
import lambda_trilogy.lambda_lith
import lambda_trilogy.fat_lambda
import lambda_trilogy.single_purpose_lambda
import lambda_function
import rds_proxy
import rest_api
import saga_step_function
import scalable_webhook
import sns_topic
import xray_tracer
import web_application_firewall


class WellArchitected(cdk.App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_webservice()
        self.create_xray_tracer()

        big_fan.BigFan(self, "BigFan")

        destined_lambda.DestinedLambda(self, "DestinedLambda")

        event_bridge_atm.EventBridgeAtm(self, "EventBridgeAtm")
        event_bridge_circuit_breaker.EventBridgeCircuitBreaker(
            self, 'EventBridgeCircuitBreaker'
        )
        event_bridge_etl.EventbridgeEtl(self, 'EventBridgeEtl')

        lambda_trilogy.lambda_lith.LambdaLith(self, "LambdaLith")
        lambda_trilogy.fat_lambda.TheFatLambdaStack(self, "FatLambda")
        lambda_trilogy.single_purpose_lambda.TheSinglePurposeFunctionStack(self, "SinglePurposeLambda")
        lambda_circuit_breaker.LambdaCircuitBreaker(self, "LambdaCircuitBreaker")

        rds_proxy.RdsProxy(self, "RdsProxy")
        saga_step_function.SagaStepFunction(self, "SagaStepFunction")
        scalable_webhook.ScalableWebhook(self, "ScalableWebhook")

    def create_webservice(self):
        error_sns_topic = sns_topic.SnsTopic(self, 'SnsTopic').topic
        hits_record = dynamodb_table.DynamoDBTableStack(
            self, 'DynamoDBTable',
            error_topic=error_sns_topic,
            partition_key=aws_dynamodb.Attribute(
                name="path",
                type=aws_dynamodb.AttributeType.STRING,
            )
        ).dynamodb_table
        hits_counter = lambda_function.LambdaFunctionStack(
            self, 'HitCounter',
            function_name='hit_counter',
            error_topic=error_sns_topic,
            environment_variables={
                'HITS_TABLE_NAME': hits_record.table_name
            },
        )
        hits_record.grant_read_write_data(hits_counter.lambda_function)
        http_api.LambdaHttpApiGateway(
            self, 'LambdaHttpApiGateway',
            lambda_function=hits_counter.lambda_function,
            error_topic=error_sns_topic,
        )
        self.rest_api = rest_api.LambdaRestAPIGatewayStack(
            self, 'LambdaRestAPIGateway',
            lambda_function=hits_counter.lambda_function,
            error_topic=error_sns_topic,
        ).rest_api
        web_application_firewall.WebApplicationFirewall(
            self, 'WebApplicationFirewall',
            target_arn=self.rest_api.resource_arn
        )

    def create_xray_tracer(self):
        xray_tracer_sns_topic = sns_topic.SnsTopic(
            self, 'XRayTracerSnsFanOutTopic', display_name='The XRay Tracer Fan Out Topic'
        ).topic
        xray_tracer.sns_rest_api.SnsRestApi(
            self, 'SnsRestApi', sns_topic=xray_tracer_sns_topic
        )
        xray_tracer.sns_flow.SnsFlow(self, 'SnsFlow', sns_topic=xray_tracer_sns_topic)
        xray_tracer.sqs_flow.SqsFlow(self, 'SqsFlow', sns_topic=xray_tracer_sns_topic)
        xray_tracer.http_flow.HttpFlow(self, 'HttpFlow', sns_topic=xray_tracer_sns_topic)
        xray_tracer.dynamodb_flow.DynamoDBFlow(
            self, 'DynamoDBFlow', sns_topic=xray_tracer_sns_topic
        )

WellArchitected().synth()