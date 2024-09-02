import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import {registerAutoTags} from "pulumi-aws-tags";

registerAutoTags({
  "user:Project": pulumi.getProject(),
  "user:Stack": pulumi.getStack(),
});

const bucket = new aws.s3.BucketV2("my-bucket", {tags: {foo: "bar"}});

export const bucketTags = bucket.tags;
