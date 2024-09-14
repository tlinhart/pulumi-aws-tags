from __future__ import annotations

from collections.abc import Mapping

import pulumi

from .taggable import is_taggable

# Taggable resources that do not support auto-tagging.
_UNSUPPORTED_RESOURCE_TYPES = {"aws:autoscaling/group:Group"}


def register_auto_tags(
    auto_tags: Mapping[str, str], *, override: bool = True
) -> None:
    """Register a global auto-tagging stack transform.

    The transform merges a set of given tags with whatever was also explicitly
    added to the resource definition. The default merge strategy is to override
    any explicitly provided tags with matching keys. To reverse this behavior
    set `override` to `False`.
    """

    def auto_tag(
        args: pulumi.ResourceTransformArgs,
    ) -> pulumi.ResourceTransformResult | None:
        if is_taggable(args.type_):
            if args.type_ in _UNSUPPORTED_RESOURCE_TYPES:
                pulumi.log.warn(f"{args.type_} does not support auto-tagging")
                return None
            props = {**args.props}
            tags = pulumi.Output.from_input(props.get("tags") or {})
            props["tags"] = tags.apply(
                lambda tags: {**tags, **auto_tags}
                if override
                else {**auto_tags, **tags}
            )
            return pulumi.ResourceTransformResult(props, args.opts)
        return None

    pulumi.runtime.register_resource_transform(auto_tag)
