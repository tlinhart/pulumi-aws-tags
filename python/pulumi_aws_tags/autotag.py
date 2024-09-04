from __future__ import annotations

from collections.abc import Mapping

import pulumi

from .taggable import is_taggable

# Taggable resources that do not support auto-tagging.
_UNSUPPORTED_RESOURCE_TYPES = {"aws:autoscaling/group:Group"}


def register_auto_tags(auto_tags: Mapping[str, str]) -> None:
    """Register a global auto-tagging stack transform.

    The transform merges a set of given tags with whatever was also explicitly
    added to the resource definition.
    """
    pulumi.runtime.register_resource_transform(
        lambda args: _auto_tag(args, auto_tags)
    )


def _auto_tag(
    args: pulumi.ResourceTransformArgs, auto_tags: Mapping[str, str]
) -> pulumi.ResourceTransformResult | None:
    """Apply the given tags to the resource properties if applicable."""
    if is_taggable(args.type_):
        if args.type_ in _UNSUPPORTED_RESOURCE_TYPES:
            pulumi.log.warn(
                f"resource of type {args.type_} does not support auto-tagging"
            )
            return None
        props = {**args.props}
        tags = pulumi.Output.from_input(props.get("tags") or {})
        props["tags"] = tags.apply(lambda tags: {**tags, **auto_tags})
        return pulumi.ResourceTransformResult(props, args.opts)
    return None
