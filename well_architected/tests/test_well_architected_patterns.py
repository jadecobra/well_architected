from tests.utilities import TestTemplates, true, false

class TestWellArchitectedPatterns(TestTemplates):

    @staticmethod
    def patterns():
        return (
            # 'DynamoDBFlow',
            # 'DynamoDBTable',
            # 'EventBridgeCircuitBreaker',
            'EventBridgeEtl',
            # 'LambdaHttpApiGateway',
            # 'HttpFlow',
            # 'LambdaFunction',
            # 'LambdaRestAPIGateway',
            # 'SnsFlow',
            # 'SnsRestApi',
            # 'SNSTopic',
            # 'SqsFlow',
            # 'WebApplicationFirewall',
        )

    def test_well_architected_cdk_patterns(self):
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_template_equal(pattern)