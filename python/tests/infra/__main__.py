import pulumi
import pulumi_aws as aws
from pulumi_aws_tags import register_auto_tags

register_auto_tags(
    {
        "example:project": pulumi.get_project(),
        "example:stack": pulumi.get_stack(),
    }
)

bucket = aws.s3.BucketV2("my-bucket", tags={"example:foo": "bar"})

pulumi.export("bucket_tags", bucket.tags)
