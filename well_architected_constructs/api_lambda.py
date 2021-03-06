import aws_cdk
import aws_cdk.aws_apigatewayv2_alpha
import aws_cdk.aws_apigatewayv2_integrations_alpha
from .api import Api

def create_http_api_lambda(
    stack, error_topic=None, lambda_function=None
):
    return Api(
        stack, 'HttpApiGateway',
        error_topic=error_topic,
        api_gateway_service_role=False,
        api=aws_cdk.aws_apigatewayv2_alpha.HttpApi(
            stack, 'HttpApi',
            default_integration=aws_cdk.aws_apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                'HttpApiLambdaFunction',
                handler=lambda_function
            ),
        )
    )

def create_rest_api_lambda(
    stack, lambda_function=None, error_topic=None,
    proxy=True
):
    return Api(
        stack, 'RestApiGateway',
        error_topic=error_topic,
        api_gateway_service_role=False,
        api=aws_cdk.aws_apigateway.LambdaRestApi(
            stack, 'RestApiLambdaFunction',
            handler=lambda_function,
            proxy=proxy,
        )
    )
