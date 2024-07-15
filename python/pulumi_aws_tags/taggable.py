import importlib
import inspect
import pkgutil

import pulumi
import pulumi_aws

# Known exceptions to the rules for identifying taggable resources.
_NOT_TAGGABLE_RESOURCE_TYPES = {
    "aws:devopsguru/resourceCollection:ResourceCollection"
}


def _snake_to_camel(s):
    """Convert a string from snake case to camel case."""
    return "".join(
        word.lower() if index == 0 else word.title()
        for index, word in enumerate(s.split("_"))
    )


def _get_resource_type(cls):
    """Return a type token for the AWS resource class."""
    path = "/".join(_snake_to_camel(p) for p in cls.__module__.split(".")[1:])
    name = cls.__name__
    return f"aws:{path}:{name}"


def _get_taggable_resource_types():
    """Return a generator of AWS type tokens that are taggable."""
    # Collect all resource classes from the pulumi_aws package.
    classes = set()
    for _, name, _ in pkgutil.walk_packages(
        path=pulumi_aws.__path__, prefix="pulumi_aws.", onerror=lambda _: None
    ):
        module = importlib.import_module(name)
        for _, cls in inspect.getmembers(
            module,
            predicate=lambda m: inspect.isclass(m)
            and issubclass(m, pulumi.CustomResource),
        ):
            classes.add(cls)

    # Yield type token for each resource class supporting the tags constructor
    # parameter (excluding known exceptions).
    for cls in classes:
        signature = inspect.signature(cls._internal_init)
        if "tags" in signature.parameters:
            type_ = _get_resource_type(cls)
            if type_ not in _NOT_TAGGABLE_RESOURCE_TYPES:
                yield type_


taggable_resource_types = sorted(_get_taggable_resource_types())


def is_taggable(t):
    """Return if the given resource type is a taggable AWS resource."""
    return t in taggable_resource_types


if __name__ == "__main__":
    for resource_type in taggable_resource_types:
        print(resource_type)
