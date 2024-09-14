import * as aws from "@pulumi/aws";
import {registerAutoTags} from "pulumi-aws-tags";

registerAutoTags({tag1: "foo", tag2: "auto"});
registerAutoTags({tag3: "auto"}, {override: false});

const bucket = new aws.s3.BucketV2("my-bucket", {
  tags: {tag2: "explicit", tag3: "explicit", tag4: "bar"},
});

export const bucketTags = bucket.tags;
