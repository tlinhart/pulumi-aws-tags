import * as pulumi from "@pulumi/pulumi";
import {isTaggable} from "./taggable";

// Taggable resources that do not support auto-tagging.
const UNSUPPORTED_RESOURCE_TYPES: string[] = ["aws:autoscaling/group:Group"];

/**
 * Register a global auto-tagging stack transformation.
 *
 * The transformation merges a set of given tags with whatever was also
 * explicitly added to the resource definition.
 */
export function registerAutoTags(autoTags: Record<string, string>): void {
  pulumi.runtime.registerStackTransformation((args) => {
    if (isTaggable(args.type)) {
      if (UNSUPPORTED_RESOURCE_TYPES.includes(args.type)) {
        // See https://github.com/pulumi/pulumi/issues/16654 for why we cannot
        // associate the message with the resource.
        pulumi.log.warn(
          `resource of type ${args.type} does not support auto-tagging`
        );
        return undefined;
      }
      args.props["tags"] = {...args.props["tags"], ...autoTags};
      return {props: args.props, opts: args.opts};
    }
    return undefined;
  });
}
