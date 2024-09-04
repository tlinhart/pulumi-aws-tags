from __future__ import annotations

import importlib
import inspect
from collections.abc import Iterator

import pulumi_aws  # noqa: F401
from pulumi.runtime.rpc import _RESOURCE_MODULES

# Known exceptions to the rules for identifying taggable resources.
_NOT_TAGGABLE_RESOURCE_TYPES = {
    "aws:devopsguru/resourceCollection:ResourceCollection"
}


def _get_resources() -> dict[str, dict[str, str]]:
    """Return all resources provided by registered Pulumi packages."""
    resources: dict[str, dict[str, str]] = {}
    for modules in _RESOURCE_MODULES.values():
        for module in modules:
            mod_info = module.mod_info  # type: ignore[attr-defined]
            module_name = mod_info["fqn"]
            resource_classes = mod_info["classes"]
            classes = resources.setdefault(module_name, {})
            classes.update(
                {name: type_ for type_, name in resource_classes.items()}
            )
    return resources


def _get_taggable_resource_types() -> Iterator[str]:
    """Return a generator of AWS type tokens that are taggable."""
    resources = _get_resources()
    for module_name, classes in resources.items():
        if not module_name.startswith("pulumi_aws."):
            continue
        module = importlib.import_module(module_name)
        for class_name, type_ in classes.items():
            cls = getattr(module, class_name)
            signature = inspect.signature(cls._internal_init)
            if (
                "tags" in signature.parameters
                and type_ not in _NOT_TAGGABLE_RESOURCE_TYPES
            ):
                yield type_


taggable_resource_types = sorted(_get_taggable_resource_types())


def is_taggable(t: str) -> bool:
    """Return if the given resource type is a taggable AWS resource."""
    return t in taggable_resource_types


if __name__ == "__main__":
    for resource_type in taggable_resource_types:
        print(resource_type)
