import pulumi

from .taggable import is_taggable

# Taggable resources that do not support auto-tagging.
_UNSUPPORTED_RESOURCE_TYPES = {"aws:autoscaling/group:Group"}


def register_auto_tags(auto_tags):
    """Register a global auto-tagging stack transform.

    The transform merges a set of given tags with whatever was also explicitly
    added to the resource definition.
    """
    pulumi.runtime.register_resource_transform(
        lambda args: _auto_tag(args, auto_tags)
    )


def _auto_tag(args, auto_tags):
    """Apply the given tags to the resource properties if applicable."""
    if is_taggable(args.type_):
        if args.type_ in _UNSUPPORTED_RESOURCE_TYPES:
            pulumi.log.warn(
                f"resource of type {args.type_} does not support auto-tagging"
            )
            return
        tags = pulumi.Output.from_input(args.props.get("tags") or {})
        args.props["tags"] = tags.apply(lambda tags: {**tags, **auto_tags})
        return pulumi.ResourceTransformResult(args.props, args.opts)
