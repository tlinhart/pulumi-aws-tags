import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import {registerAutoTags} from "pulumi-aws-tags";

registerAutoTags({
  "user:Project": pulumi.getProject(),
  "user:Stack": pulumi.getStack(),
});

export const server = new aws.ec2.Instance("server", {
  instanceType: "t2.micro",
  ami: "ami-0bb75d95f668ff5a7",
  tags: {ServerGroup: "webservers"},
});
