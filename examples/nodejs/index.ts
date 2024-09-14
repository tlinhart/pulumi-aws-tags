import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import {registerAutoTags} from "pulumi-aws-tags";

// Automatically inject tags to created AWS resources.
registerAutoTags({
  "example:project": pulumi.getProject(),
  "example:stack": pulumi.getStack(),
});

// Create a bunch of AWS resources.
const bucket = new aws.s3.Bucket("my-bucket");

const group = new aws.ec2.SecurityGroup("web-secgrp", {
  ingress: [
    {
      protocol: "tcp",
      fromPort: 22,
      toPort: 22,
      cidrBlocks: ["0.0.0.0/0"],
    },
    {
      protocol: "tcp",
      fromPort: 80,
      toPort: 80,
      cidrBlocks: ["0.0.0.0/0"],
    },
  ],
});

const server = new aws.ec2.Instance("web-server", {
  instanceType: "t2.micro",
  ami: "ami-0bb75d95f668ff5a7",
  vpcSecurityGroupIds: [group.id],
});

export const bucketName = bucket.id;
export const serverDns = server.publicDns;
