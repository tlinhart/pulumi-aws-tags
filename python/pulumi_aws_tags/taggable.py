import inspect

import pulumi
import pulumi_aws


def _snake_to_camel(s):
    """Convert a string from snake case to camel case."""
    return "".join(
        word.lower() if index == 0 else word.title()
        for index, word in enumerate(s.split("_"))
    )


def _get_taggable_resource_types():
    """Return a generator of AWS type tokens that are taggable."""
    # Get all submodules of the pulumi_aws package.
    modules = set()

    def walk_modules(module):
        for name, submodule in inspect.getmembers(module, inspect.ismodule):
            if (
                submodule.__name__.startswith(module.__name__)
                and submodule not in modules
            ):
                modules.add(module)
                walk_modules(submodule)

    walk_modules(pulumi_aws)

    # Get all resource classes which support the tags constructor parameter.
    classes = set()
    for module in modules:
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, pulumi.CustomResource):
                signature = inspect.signature(cls._internal_init)
                if "tags" in signature.parameters:
                    classes.add(cls)

    # Yield AWS type tokens.
    for cls in classes:
        path = "/".join(
            _snake_to_camel(name) for name in cls.__module__.split(".")[1:]
        )
        name = cls.__name__
        yield f"aws:{path}:{name}"


taggable_resource_types = sorted(_get_taggable_resource_types())


def is_taggable(t):
    """Return if the given resource type is a taggable AWS resource."""
    return t in taggable_resource_types


if __name__ == "__main__":
    for resource_type in taggable_resource_types:
        print(resource_type)
