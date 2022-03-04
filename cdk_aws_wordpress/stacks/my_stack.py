import os
from aws_cdk import Stack, RemovalPolicy
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_route53 import PublicHostedZone
from constructs import Construct
from cloudcomponents.cdk_wordpress import Wordpress


class MyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read WP_DOMAIN and WP_IMAGE from environment variables
        WP_DOMAIN = account = os.environ.get("WP_DOMAIN")
        WP_IMAGE = account = os.environ.get("WP_IMAGE")
        if not WP_DOMAIN or not WP_IMAGE:
            raise Exception(
                "Required environment variables 'WP_DOMAIN' or 'WP_IMAGE' are missing or undefined"
            )

        wp_domain_zone = PublicHostedZone.from_lookup(
            self,
            "WpDomainZone",
            domain_name=WP_DOMAIN,
        )

        Wordpress(
            self,
            "Wordpress",
            domain_name=f"blog.{WP_DOMAIN}",
            domain_zone=wp_domain_zone,
            image=ContainerImage.from_registry(WP_IMAGE),
            removal_policy=RemovalPolicy.DESTROY,
            offload_static_content=True,  # Support for plugin e.g. `WP Offload Media for Amazon S3`
        )
