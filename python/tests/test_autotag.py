import os

from pulumi import automation
from pulumi.automation import ConfigValue, LocalWorkspaceOptions


class TestAutoTags:
    @classmethod
    def setup_class(cls) -> None:
        """Provision test infrastructure."""
        cls.stack = automation.create_or_select_stack(
            "dev",
            work_dir=os.path.join(os.path.dirname(__file__), "infra"),
            opts=LocalWorkspaceOptions(
                env_vars={
                    "PULUMI_BACKEND_URL": "file://~",
                    "PULUMI_CONFIG_PASSPHRASE": "test",
                }
            ),
        )
        cls.stack.set_all_config(
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
        cls.stack.up(on_output=print)
        cls.outputs = cls.stack.outputs()

    @classmethod
    def teardown_class(cls) -> None:
        """Destroy test infrastructure."""
        cls.stack.destroy(on_output=print, remove=True)

    def test_bucket_has_auto_tags(self) -> None:
        """Check bucket has auto-tags."""
        bucket_tags = self.outputs.get("bucket_tags")
        assert bucket_tags is not None
        assert "user:Project" in bucket_tags.value

    def test_bucket_has_explicit_tags(self) -> None:
        """Check bucket has explicitly defined tags."""
        bucket_tags = self.outputs.get("bucket_tags")
        assert bucket_tags is not None
        assert "foo" in bucket_tags.value
