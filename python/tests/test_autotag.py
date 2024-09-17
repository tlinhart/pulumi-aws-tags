from __future__ import annotations

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
        stack.up(on_output=print, suppress_progress=True)
        yield stack
        stack.destroy(remove=True, on_output=print, suppress_progress=True)

    def test_bucket_auto_tags(self, stack: Stack) -> None:
        """Check bucket has auto-tags."""
        outputs = stack.outputs()
        bucket_tags = outputs.get("bucket_tags")
        assert bucket_tags is not None
        assert all(
            key in bucket_tags.value for key in ["tag1", "tag2", "tag3"]
        )

    def test_bucket_explicit_tags(self, stack: Stack) -> None:
        """Check bucket has explicitly defined tags."""
        outputs = stack.outputs()
        bucket_tags = outputs.get("bucket_tags")
        assert bucket_tags is not None
        assert all(
            key in bucket_tags.value for key in ["tag2", "tag3", "tag4"]
        )

    def test_bucket_tags_precedence(self, stack: Stack) -> None:
        """Check bucket tag values conform to merge strategy."""
        outputs = stack.outputs()
        bucket_tags = outputs.get("bucket_tags")
        assert bucket_tags is not None
        assert all(key in bucket_tags.value for key in ["tag2", "tag3"])
        assert bucket_tags.value["tag2"] == "auto"
        assert bucket_tags.value["tag3"] == "explicit"
