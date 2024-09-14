import pulumi
import pulumi_aws as aws
from pulumi_aws_tags import register_auto_tags

# Automatically inject tags to created AWS resources.
register_auto_tags(
    {
        "example:project": pulumi.get_project(),
        "example:stack": pulumi.get_stack(),
    }
)

# Create a bunch of AWS resources.
bucket = aws.s3.Bucket("my-bucket")

group = aws.ec2.SecurityGroup(
    "web-secgrp",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": ["0.0.0.0/0"],
        },
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"],
        },
    ],
)

server = aws.ec2.Instance(
    "web-server",
    instance_type="t2.micro",
    ami="ami-0bb75d95f668ff5a7",
    vpc_security_group_ids=[group.id],
)

pulumi.export("bucket_name", bucket.id)
pulumi.export("server_dns", server.public_dns)
