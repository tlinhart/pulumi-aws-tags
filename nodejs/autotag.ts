import * as pulumi from "@pulumi/pulumi";
import {isTaggable} from "./taggable";

// Taggable resources that do not support auto-tagging.
const UNSUPPORTED_RESOURCE_TYPES: string[] = ["aws:autoscaling/group:Group"];

export interface RegisterAutoTagsOptions {
  /**
   * Override any explicitly provided tags with matching keys.
   */
  override?: boolean;
}

/**
 * Register a global auto-tagging stack transform.
 *
 * The transform merges a set of given tags with whatever was also explicitly
 * added to the resource definition. The default merge strategy is to override
 * any explicitly provided tags with matching keys. To reverse this behavior
 * set `override` to `false`.
 */
export function registerAutoTags(
  autoTags: Record<string, string>,
  {override = true}: RegisterAutoTagsOptions = {}
): void {
  pulumi.runtime.registerResourceTransform((args) => {
    if (isTaggable(args.type)) {
      if (UNSUPPORTED_RESOURCE_TYPES.includes(args.type)) {
        pulumi.log.warn(`${args.type} does not support auto-tagging`);
        return undefined;
      }
      const tags = pulumi.output(args.props.tags || {});
      args.props.tags = tags.apply((tags) =>
        override ? {...tags, ...autoTags} : {...autoTags, ...tags}
      );
      return {props: args.props, opts: args.opts};
    }
    return undefined;
  });
}
