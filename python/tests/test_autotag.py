import os
from collections.abc import Iterator

import pytest
from pulumi import automation
from pulumi.automation import ConfigValue, LocalWorkspaceOptions, Stack
from pytest import FixtureRequest


class TestAutoTags:
    @pytest.fixture(scope="class")
    def stack(self, request: FixtureRequest) -> Iterator[Stack]:
        stack = automation.create_or_select_stack(
            "dev",
            work_dir=os.path.join(os.path.dirname(__file__), "infra"),
            opts=LocalWorkspaceOptions(
                env_vars={
                    "PULUMI_BACKEND_URL": "file://~",
                    "PULUMI_CONFIG_PASSPHRASE": "test",
                }
            ),
        )
        stack.set_all_config(
            {
                "aws:region": ConfigValue("us-east-1"),
                "aws:accessKey": ConfigValue("test"),
                "aws:secretKey": ConfigValue("test"),
                "aws:skipCredentialsValidation": ConfigValue("true"),
                "aws:skipRequestingAccountId": ConfigValue("true"),
                "aws:s3UsePathStyle": ConfigValue("true"),
                'aws:endpoints[0]["s3"]': ConfigValue("http://localhost:4566"),
            },
            path=True,
        )
        stack.up(on_output=print)
        yield stack
        stack.destroy(on_output=print, remove=True)

    def test_bucket_has_auto_tags(self, stack: Stack) -> None:
        """Check bucket has auto-tags."""
        outputs = stack.outputs()
        bucket_tags = outputs.get("bucket_tags")
        assert bucket_tags is not None
        assert "example:project" in bucket_tags.value

    def test_bucket_has_explicit_tags(self, stack: Stack) -> None:
        """Check bucket has explicitly defined tags."""
        outputs = stack.outputs()
        bucket_tags = outputs.get("bucket_tags")
        assert bucket_tags is not None
        assert "example:foo" in bucket_tags.value
