import constructs
import aws_cdk
import well_architected

class LambdaFunctionConstruct(well_architected.WellArchitectedConstruct):

    def __init__(self, scope: constructs.Construct, id: str,
        function_name=None, handler_name=None,
        environment_variables=None,
        error_topic:aws_cdk.aws_sns.Topic=None,
        layers:list[str]=None,
        concurrent_executions=None,
        duration=60, vpc=None,
        **kwargs
    ) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )
        handler_name = 'handler' if handler_name is None else handler_name
        self.lambda_function = aws_cdk.aws_lambda.Function(
            self, 'LambdaFunction', # can we use id as function_name
            runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_9,
            handler=f'{function_name}.{handler_name}',
            code=aws_cdk.aws_lambda.Code.from_asset(f"lambda_functions/{function_name}"),
            timeout=aws_cdk.Duration.seconds(duration),
            tracing=aws_cdk.aws_lambda.Tracing.ACTIVE,
            layers=self.create_layers(layers),
            vpc=vpc,
            reserved_concurrent_executions=concurrent_executions,
            environment=environment_variables,
        )
        self.create_invocations_error_greater_than_2_percent_alarm()
        self.create_invocation_longer_than_1_second_alarmration_alarm()
        self.create_throttled_invocations_greater_than_2_percent_alarm()
        self.create_cloudwatch_dashboard(
            self.create_cloudwatch_widgets()
        )

    def create_layer(self, layer):
        return aws_cdk.aws_lambda.LayerVersion(
            self, f'{layer}LambdaLayer',
            code=aws_cdk.aws_lambda.Code.from_asset(f"lambda_layers/{layer}"),
            description=f"{layer} Lambda Layer"
        )

    def create_layers(self, layers):
        result = [self.create_layer('aws-xray-sdk')]
        try:
            for layer in layers:
                result.append(self.create_layer(layer))
        except TypeError:
            'No additional layers specified'
        return result

    def get_lambda_function_metric(self, metric_name):
        return self.lambda_function.metric(metric_name=metric_name, statistic="sum")

    def create_lambda_error_percentage_metric(self):
        return self.create_cloudwatch_math_expression(
            label="invocations_errored_percentage_last_5_mins",
            expression="(errors / invocations) * 100",
            using_metrics={
                "invocations": self.get_lambda_function_metric('Invocations'),
                "errors": self.get_lambda_function_metric("Errors"),
            },
        )

    def create_lambda_throttled_percentage_metric(self):
        # NOTE: throttled requests are not counted in total number of invocations
        return self.create_cloudwatch_math_expression(
            label="throttled_requests_percentage_last_30_mins",
            expression="(throttles * 100) / (invocations + throttles)",
            using_metrics={
                "invocations": self.get_lambda_function_metric("Invocations"),
                "throttles": self.get_lambda_function_metric("Throttles"),
            },
        )

    def create_invocations_error_greater_than_2_percent_alarm(self):
        return self.create_cloudwatch_alarm(
            id="LambdaInvocationsErrorsGreaterThan2Percent",
            metric=self.create_lambda_error_percentage_metric(),
            threshold=2,
        )

    def create_invocation_longer_than_1_second_alarmration_alarm(self):
        return self.create_cloudwatch_alarm(
            id="LambdaP99LongDurationGreaterThan1s",
            metric=self.lambda_function.metric_duration(statistic="p99"),
            threshold=1000,
        )

    def create_throttled_invocations_greater_than_2_percent_alarm(self):
        return self.create_cloudwatch_alarm(
            id="LambdaThrottledInvocationsGreaterThan2Percent",
            metric=self.create_lambda_throttled_percentage_metric(),
            threshold=2,
        )

    def create_lambda_error_percentage_widget(self):
        return self.create_cloudwatch_widget(
            title="lambda_error_percentage",
            stacked=False,
            left=[self.create_lambda_error_percentage_metric()],
        )

    def create_lambda_duration_widget(self):
        return self.create_cloudwatch_widget(
            title="lambda_duration",
            left=[
                self.lambda_function.metric_duration(statistic=statistic)
                for statistic in ('p50', 'p90', 'p99')
            ],
        )

    def create_lambda_throttled_percentage_widget(self):
        return self.create_cloudwatch_widget(
            title="lambda_throttle_percentage",
            left=[self.create_lambda_throttled_percentage_metric()],
            stacked=False,
        )

    def create_cloudwatch_widgets(self):
        return (
            self.create_lambda_error_percentage_widget(),
            self.create_lambda_duration_widget(),
            self.create_lambda_throttled_percentage_widget(),
        )

class LambdaFunctionStack(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str,
        function_name=None, environment_variables=None, error_topic:aws_cdk.aws_sns.ITopic=None,
        handler_name=None,
        **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.lambda_function = create_python_lambda_function(
            self, function_name=function_name,
            environment_variables=environment_variables,
            error_topic=error_topic,
            handler_name=handler_name,
        )

def create_python_lambda_function(
        stack,
        function_name=None, handler_name=None,
        environment_variables=None,
        duration=60, error_topic=None, vpc=None,
        concurrent_executions=None,
    ):
    return LambdaFunctionConstruct(
        stack, function_name,
        function_name=function_name,
        handler_name=handler_name,
        environment_variables=environment_variables,
        duration=duration,
        error_topic=error_topic,
        vpc=vpc,
        concurrent_executions=concurrent_executions,
    ).lambda_function