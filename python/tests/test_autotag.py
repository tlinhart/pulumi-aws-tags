import pulumi


class PulumiMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        outputs = {**args.inputs}
        return [f"{args.name}_id", outputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}


pulumi.runtime.set_mocks(PulumiMocks())

from . import infra  # noqa: E402


@pulumi.runtime.test
def test_server_has_tags():
    def check_tags(args):
        urn, tags = args
        assert tags is not None, f"server {urn} must have tags"
        assert "user:Project" in tags, f"server {urn} must have auto-tags"
        assert (
            "ServerGroup" in tags
        ), f"server {urn} must have explicitly defined tags"

    return pulumi.Output.all(infra.server.urn, infra.server.tags).apply(
        check_tags
    )
