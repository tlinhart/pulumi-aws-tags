import pulumi

from .taggable import is_taggable


def register_auto_tags(auto_tags):
    """Register a global auto-tagging stack transformation.

    The transformation merges a set of given tags with whatever was also
    explicitly added to the resource definition.
    """
    pulumi.runtime.register_stack_transformation(
        lambda args: _auto_tag(args, auto_tags)
    )


def _auto_tag(args, auto_tags):
    """Apply the given tags to the resource properties if applicable."""
    if is_taggable(args.type_):
        args.props["tags"] = {**(args.props["tags"] or {}), **auto_tags}
        return pulumi.ResourceTransformationResult(args.props, args.opts)
