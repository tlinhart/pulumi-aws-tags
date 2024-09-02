import pulumi
import pulumi_aws as aws
from pulumi_aws_tags import register_auto_tags

register_auto_tags(
    {"user:Project": pulumi.get_project(), "user:Stack": pulumi.get_stack()}
)

bucket = aws.s3.BucketV2("my-bucket", tags={"foo": "bar"})

pulumi.export("bucket_tags", bucket.tags)
