import aws_cdk
import constructs



class NlbAutoscalingEcs(aws_cdk.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, *kwargs)

        vpc = self.create_vpc()
        ecs_cluster = self.create_ecs_cluster(vpc)
        ecs_cluster.add_asg_capacity_provider(
            self.create_autoscaling_group_provider(vpc)
        )

        ecs_service = self.create_ecs_service(
            ecs_cluster=ecs_cluster,
            container_image=container_image,
        )

        aws_cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value=ecs_service.load_balancer.load_balancer_dns_name
        )

    def create_vpc(self):
        return aws_cdk.aws_ec2.Vpc(
            self, "Vpc",
            max_azs=2
        )

    def create_ecs_cluster(self, vpc):
        return aws_cdk.aws_ecs.Cluster(
            self, 'EcsCluster',
            vpc=vpc
        )

    def create_autoscaling_group(self, vpc):
        return aws_cdk.aws_autoscaling.AutoScalingGroup(
            self, "AutoScalingGroup",
            instance_type=aws_cdk.aws_ec2.InstanceType("t2.micro"),
            machine_image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(),
            vpc=vpc,
        )

    def create_autoscaling_group_provider(self, vpc):
        return aws_cdk.aws_ecs.AsgCapacityProvider(
            self, "AsgCapacityProvider",
            auto_scaling_group=self.create_autoscaling_group(vpc)
        )

    def create_ecs_service(self, ecs_cluster=None, container_image=None):
        return aws_cdk.aws_ecs_patterns.NetworkLoadBalancedEc2Service(
            self, "Ec2Service",
            cluster=ecs_cluster,
            memory_limit_mib=512,
            task_image_options=aws_cdk.aws_ecs_patterns.NetworkLoadBalancedTaskImageOptions(
                image=aws_cdk.aws_ecs.ContainerImage.from_registry(
                    container_image
                )
            )
        )
