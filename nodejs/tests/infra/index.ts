import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import {registerAutoTags} from "pulumi-aws-tags";

registerAutoTags({
  "example:project": pulumi.getProject(),
  "example:stack": pulumi.getStack(),
});

const bucket = new aws.s3.BucketV2("my-bucket", {tags: {"example:foo": "bar"}});

export const bucketTags = bucket.tags;
