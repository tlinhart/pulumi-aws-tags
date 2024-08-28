import * as pulumi from "@pulumi/pulumi";
import {isTaggable} from "./taggable";

// Taggable resources that do not support auto-tagging.
const UNSUPPORTED_RESOURCE_TYPES: string[] = ["aws:autoscaling/group:Group"];

/**
 * Register a global auto-tagging stack transform.
 *
 * The transform merges a set of given tags with whatever was also explicitly
 * added to the resource definition.
 */
export function registerAutoTags(autoTags: Record<string, string>): void {
  pulumi.runtime.registerResourceTransform((args) => {
    if (isTaggable(args.type)) {
      if (UNSUPPORTED_RESOURCE_TYPES.includes(args.type)) {
        pulumi.log.warn(
          `resource of type ${args.type} does not support auto-tagging`
        );
        return undefined;
      }
      const tags = pulumi.output(args.props.tags || {});
      args.props.tags = tags.apply((tags) => ({...tags, ...autoTags}));
      return {props: args.props, opts: args.opts};
    }
    return undefined;
  });
}
