from aws_cdk import (
    aws_lambda,
    aws_apigateway as api_gateway,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    core as cdk
)
import lambda_function

class EventBridgeAtm(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.create_lambda_function_with_event_bridge_rule(
            handler_name="approved_transaction_handler",
            function_name="atm_consumer",
            event_bridge_rule=self.create_event_bridge_rule(
                rule_name="approved_transactions_rule",
                description='Approved Transaction',
                detail={
                    "result": ["approved"]
                }
            ),
        )

        self.create_lambda_function_with_event_bridge_rule(
            handler_name="ny_prefix_transaction_handler",
            function_name="atm_consumer",
            event_bridge_rule=self.create_event_bridge_rule(
                rule_name="ny_prefix_transactions_rule",
                detail={
                    "location": [{"prefix": "NY-"}]
                }
            ),
        )

        self.create_lambda_function_with_event_bridge_rule(
            handler_name="not_approved_transaction_handler",
            function_name="atm_consumer",
            event_bridge_rule=self.create_event_bridge_rule(
                rule_name="not_approved_transaction_rule",
                detail={
                    "result": [{"anything-but": "approved"}]
                }
            ),
        )

        atm_producer_lambda = self.create_lambda_function_with_event_bridge_rule(
            function_name="atm_producer"
        )

        atm_producer_lambda.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                resources=['*'],
                actions=['events:PutEvents']
            )
        )

        api_gateway.LambdaRestApi(
            self, 'Endpoint',
            handler=atm_producer_lambda
        )

    def create_event_bridge_rule(self, rule_name=None, description=None, detail=None):
        return events.Rule(
            self, rule_name,
            description=description,
            event_pattern=events.EventPattern(
                source=['custom.myATMapp'],
                detail_type=['transaction'],
                detail=detail
            )
        )

    def create_lambda_function_with_event_bridge_rule(
        self, handler_name=None, function_name=None,
        event_bridge_rule:events.Rule=None
    ):
        handler_name = 'handler' if not handler_name else handler_name
        function = aws_lambda.Function(
            self, handler_name,
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler=f"{function_name}.{handler_name}",
            code=aws_lambda.Code.from_asset(f"lambda_functions/{function_name}")
        )
        # function = lambda_function.create_python_lambda_function(
        #     self, construct_id=handler_name,
        #     handler_name=handler_name,
        #     function_name=function_name,
        # )
        if event_bridge_rule:
            event_bridge_rule.add_target(
                targets.LambdaFunction(
                    handler=function
                )
            )
        return function
