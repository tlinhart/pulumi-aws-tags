import {LocalWorkspace, Stack, OutputMap} from "@pulumi/pulumi/automation";
import * as path from "path";
import "mocha";

describe("infra", function () {
  this.timeout(300000);

  let stack: Stack;
  let outputs: OutputMap;

  before(async function () {
    stack = await LocalWorkspace.createOrSelectStack(
      {
        stackName: "dev",
        workDir: path.join(__dirname, "infra"),
      },
      {
        envVars: {
          PULUMI_BACKEND_URL: "file://~",
          PULUMI_CONFIG_PASSPHRASE: "test",
        },
      }
    );
    await stack.setAllConfig(
      {
        "aws:region": {value: "us-east-1"},
        "aws:accessKey": {value: "test"},
        "aws:secretKey": {value: "test"},
        "aws:skipCredentialsValidation": {value: "true"},
        "aws:skipRequestingAccountId": {value: "true"},
        "aws:s3UsePathStyle": {value: "true"},
        'aws:endpoints[0]["s3"]': {value: "http://localhost:4566"},
      },
      true
    );
    await stack.up({onOutput: console.log});
    outputs = await stack.outputs();
  });

  after(async function () {
    await stack.destroy({onOutput: console.log, remove: true});
  });

  it("bucket must have auto-tags", async function () {
    if (!Object.hasOwn(outputs.bucketTags.value, "user:Project")) {
      throw new Error("assertion failed");
    }
  });

  it("bucket must have explicitly defined tags", async function () {
    if (!Object.hasOwn(outputs.bucketTags.value, "foo")) {
      throw new Error("assertion failed");
    }
  });
});
