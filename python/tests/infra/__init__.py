import pulumi
import pulumi_aws as aws
from pulumi_aws_tags import register_auto_tags


register_auto_tags({
    'user:Project': pulumi.get_project(),
    'user:Stack': pulumi.get_stack()
})

server = aws.ec2.Instance(
    'server',
    instance_type='t2.micro',
    ami='ami-0bb75d95f668ff5a7',
    tags={
        'ServerGroup': 'webservers'
    }
)
