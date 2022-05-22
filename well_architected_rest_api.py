import aws_cdk
import constructs
import json
import well_architected
import well_architected_api

class WellArchitectedRestApiSns(well_architected.WellArchitectedStack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

    @staticmethod
    def create_schema(title=None, properties=None):
        return aws_cdk.aws_apigateway.JsonSchema(
            schema=aws_cdk.aws_apigateway.JsonSchemaVersion.DRAFT4,
            title=title,
            type=aws_cdk.aws_apigateway.JsonSchemaType.OBJECT,
            properties=properties
        )

    @staticmethod
    def string_schema_type():
        return aws_cdk.aws_apigateway.JsonSchema(
            type=aws_cdk.aws_apigateway.JsonSchemaType.STRING
        )

    def create_response_model(
        self, rest_api=None, model_name=None, properties=None
    ):
        property_keys = ['message']
        property_keys.append(properties) if properties else None
        return rest_api.add_model(
            model_name,
            content_type='application/json',
            model_name=model_name,
            schema=self.create_schema(
                title=model_name,
                properties={key: self.string_schema_type() for key in property_keys},
            )
        )

    @staticmethod
    def create_json_template(template):
        return {'application/json': template}

    @staticmethod
    def create_response_parameters(content_type=True, allow_origin=True, allow_credentials=True):
        return {
            'method.response.header.Content-Type': content_type,
            'method.response.header.Access-Control-Allow-Origin': allow_origin,
            'method.response.header.Access-Control-Allow-Credentials': allow_credentials,
        }

    def create_method_response(self, status_code=None, response_model=None):
        return aws_cdk.aws_apigateway.MethodResponse(
            status_code=str(status_code),
            response_parameters=self.create_response_parameters(),
            response_models=self.create_json_template(response_model)
        )

    def create_method_responses(self, rest_api):
        return [
            self.create_method_response(
                status_code=200,
                response_model=self.create_response_model(
                    rest_api=rest_api,
                    model_name='pollResponse',
                )
            ),
            self.create_method_response(
                status_code=400,
                response_model=self.create_response_model(
                    rest_api=rest_api,
                    model_name='errorResponse',
                    properties='state',
                )
            )
        ]

    @staticmethod
    def get_stage_options():
        return aws_cdk.aws_apigateway.StageOptions(
            metrics_enabled=True,
            logging_level=aws_cdk.aws_apigateway.MethodLoggingLevel.INFO,
            data_trace_enabled=True,
            stage_name='prod'
        )

    def create_rest_api(self, error_topic=None):
        return well_architected_api.WellArchitectedApi(
            self, 'RestApi',
            error_topic=error_topic,
            api=aws_cdk.aws_apigateway.RestApi(
                self, 'RestApiSns',
                    deploy_options=self.get_stage_options()
                )
        ).api

    def create_rest_api_method(self, method=None, rest_api=None, integration=None):
        rest_api.root.add_resource(
            'SendEvent'
        ).add_method(
            method,
            integration,
            method_responses=self.create_method_responses(rest_api)
        )

    def create_iam_service_role_for(self, sns_topic):
        role = aws_cdk.aws_iam.Role(
            self, 'IamRole',
            assumed_by=aws_cdk.aws_iam.ServicePrincipal(
                'apigateway.amazonaws.com'
            )
        )
        sns_topic.grant_publish(role)
        return role

    def get_request_templates(self, sns_topic_arn):
        raise NotImplementedError

    def get_integration_options(self, iam_role=None, request_templates=None):
        return aws_cdk.aws_apigateway.IntegrationOptions(
            credentials_role=iam_role,
            request_parameters={
                'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"
            },
            request_templates=request_templates,
            passthrough_behavior=aws_cdk.aws_apigateway.PassthroughBehavior.NEVER,
            integration_responses=self.get_integration_responses(),
        )

    def create_api_sns_integration(self, sns_topic):
        return aws_cdk.aws_apigateway.Integration(
            type=aws_cdk.aws_apigateway.IntegrationType.AWS,
            integration_http_method='POST',
            uri='arn:aws:apigateway:us-east-1:sns:path//',
            options=self.get_integration_options(
                iam_role=self.create_iam_service_role_for(sns_topic),
                request_templates=self.get_request_templates(sns_topic.topic_arn)
            ),
        )

    def create_integration_response(
        self, status_code=None, response_templates=None, response_parameters=None,
        selection_pattern=None, separators=None
    ):
        return aws_cdk.aws_apigateway.IntegrationResponse(
            status_code=str(status_code),
            selection_pattern=selection_pattern,
            response_templates=self.create_json_template(
                json.dumps(response_templates, separators=separators)
            ),
            response_parameters=response_parameters,
        )

    def get_integration_responses(self):
        return [
            self.create_integration_response(
                status_code=200,
                response_templates={"message": 'Message added to SNS topic'}
            ),
            self.create_integration_response(
                status_code=400,
                response_templates={
                    "message": "$util.escapeJavaScript($input.path('$.errorMessage'))",
                    "state": 'error',
                },
                selection_pattern="^\[Error\].*",
                separators=(',', ':'),
                response_parameters=self.create_response_parameters(
                    content_type="'application/json'",
                    allow_origin="'*'",
                    allow_credentials="'true'",
                )
            )
        ]


class RestApiLambdaConstruct(well_architected.WellArchitectedConstruct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        lambda_function: aws_cdk.aws_lambda.Function,
        error_topic:aws_cdk.aws_sns.Topic=None,
        **kwargs
        ) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )

        self.api = self.create_rest_api()
        self.error_topic = error_topic
        self.api_id = self.api.rest_api_id
        self.connect_api_to_lambda_function(
            resource=self.create_api_resource(self.api),
            lambda_function=lambda_function,
        )

        # fix resource_arn
        # self.resource_arn = f"arn:aws:apigateway:{self.region}::/restapis/{self.api_id}/stages/{self.rest_api.deployment_stage.stage_name}"
        self.resource_arn = "arn:aws:apigateway:{self.region}::/restapis/{self.api_id}/stages/{self.rest_api.deployment_stage.stage_name}"

        well_architected_api.WellArchitectedApi(
            self, 'ApiGatewayCloudWatch',
            api=self.api,
            error_topic=self.error_topic,
        )

    def method_origin(self):
        return 'method.response.header.Access-Control-Allow-Origin'

    def status_code(self):
        return '200'

    def create_method_responses(self):
        return [
            aws_cdk.aws_apigateway.MethodResponse(
                status_code=self.status_code(),
                response_parameters={
                    self.method_origin(): True
                }
            )
        ]

    def connect_api_to_lambda_function(self, resource=None, lambda_function=None):
        return resource.add_method(
            'GET', self.create_lambda_integration(lambda_function),
            method_responses=self.create_method_responses()
        )

    def create_integration_responses(self):
        return [
            aws_cdk.aws_apigateway.IntegrationResponse(
                status_code=self.status_code(),
                response_parameters={
                    self.method_origin(): "'*'"
                }
            )
        ]

    def create_lambda_integration(self, lambda_function):
        return aws_cdk.aws_apigateway.LambdaIntegration(
            lambda_function,
            proxy=False,
            integration_responses=self.create_integration_responses()
        )

    def create_api_resource(self, api):
        return api.root.add_resource('hello')

    def create_log_group(self):
        return aws_cdk.aws_logs.LogGroup(self, "helloAPILogs")

    def method_deployment_options(self):
        return {
            # This special path applies to all resource paths and all HTTP methods
            "/*/*": aws_cdk.aws_apigateway.MethodDeploymentOptions(
                throttling_rate_limit=100,
                throttling_burst_limit=200
            )
        }

    def deploy_options(self):
        return aws_cdk.aws_apigateway.StageOptions(
            method_options=self.method_deployment_options(),
            access_log_format=aws_cdk.aws_apigateway.AccessLogFormat.clf(),
            access_log_destination=aws_cdk.aws_apigateway.LogGroupLogDestination(
                self.create_log_group()
            ),
        )

    def create_rest_api(self):
        return aws_cdk.aws_apigateway.RestApi(
            self, 'LambdaAPIGateway',
            rest_api_name='hello',
            endpoint_types=[aws_cdk.aws_apigateway.EndpointType.REGIONAL],
            deploy_options=self.deploy_options(),
        )


class LambdaRestAPIGatewayStack(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, lambda_function: aws_cdk.aws_lambda.Function, error_topic:aws_cdk.aws_sns.Topic=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.rest_api = LambdaRestAPIGatewayConstruct(
            self, id,
            lambda_function=lambda_function,
            error_topic=error_topic,
            **kwargs
        )