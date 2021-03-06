import constructs
import regular_constructs.ecs_fargate_service
import well_architected


class NlbFargateService(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        regular_constructs.ecs_fargate_service.FargateService(
            self, 'EcsFargateService',
            container_image=container_image,
        )