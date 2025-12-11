import {LocalWorkspace, Stack, OutputMap} from "@pulumi/pulumi/automation";
import * as path from "path";
import {strict as assert} from "assert";
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
        "aws:s3UsePathStyle": {value: "true"},
        'aws:endpoints[0]["sts"]': {value: "http://localhost:4566"},
        'aws:endpoints[0]["s3"]': {value: "http://localhost:4566"},
        'aws:endpoints[0]["s3control"]': {value: "http://localhost:4566"},
      },
      true
    );
    await stack.up({onOutput: console.log, suppressProgress: true});
    outputs = await stack.outputs();
  });

  after(async function () {
    await stack.destroy({
      remove: true,
      onOutput: console.log,
      suppressProgress: true,
    });
  });

  it("bucket must have auto-tags", async function () {
    ["tag1", "tag2", "tag3"].forEach((key) => {
      assert(Object.hasOwn(outputs.bucketTags.value, key));
    });
  });

  it("bucket must have explicitly defined tags", async function () {
    ["tag2", "tag3", "tag4"].forEach((key) => {
      assert(Object.hasOwn(outputs.bucketTags.value, key));
    });
  });

  it("bucket tag values must conform to merge strategy", async function () {
    ["tag2", "tag3"].forEach((key) => {
      assert(Object.hasOwn(outputs.bucketTags.value, key));
    });
    assert.strictEqual(outputs.bucketTags.value.tag2, "auto");
    assert.strictEqual(outputs.bucketTags.value.tag3, "explicit");
  });
});
