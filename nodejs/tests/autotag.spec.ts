import * as pulumi from "@pulumi/pulumi";
import "mocha";

pulumi.runtime.setMocks({
  newResource: function (
    args: pulumi.runtime.MockResourceArgs
  ): pulumi.runtime.MockResourceResult {
    const outputs = {...args.inputs};
    return {
      id: `${args.name}_id`,
      state: outputs,
    };
  },
  call: function (): pulumi.runtime.MockCallResult {
    return {};
  },
});

describe("infra", function () {
  let infra: typeof import("./infra/index");

  before(function () {
    // https://github.com/pulumi/pulumi/issues/4669
    pulumi.runtime.runInPulumiStack(async function () {
      infra = await import("./infra/index");
    });
  });

  it("server must have tags", function (done) {
    infra.server.tags.apply((tags) =>
      tags ? done() : done(new Error("assertion failed"))
    );
  });

  it("server must have auto-tags", function (done) {
    infra.server.tags.apply((tags) =>
      Object.prototype.hasOwnProperty.call(tags, "user:Project")
        ? done()
        : done(new Error("assertion failed"))
    );
  });

  it("server must have explicitly defined tags", function (done) {
    infra.server.tags.apply((tags) =>
      Object.prototype.hasOwnProperty.call(tags, "ServerGroup")
        ? done()
        : done(new Error("assertion failed"))
    );
  });
});
