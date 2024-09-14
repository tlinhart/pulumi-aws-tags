import pulumi
import pulumi_aws as aws
from pulumi_aws_tags import register_auto_tags

register_auto_tags({"tag1": "foo", "tag2": "auto"})
register_auto_tags({"tag3": "auto"}, override=False)

bucket = aws.s3.BucketV2(
    "my-bucket", tags={"tag2": "explicit", "tag3": "explicit", "tag4": "bar"}
)

pulumi.export("bucket_tags", bucket.tags)
