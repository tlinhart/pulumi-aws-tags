import * as pulumi from "@pulumi/pulumi";
import {isTaggable} from "./taggable";

/**
 * Register a global auto-tagging stack transformation.
 *
 * The transformation merges a set of given tags with whatever was also
 * explicitly added to the resource definition.
 */
export function registerAutoTags(autoTags: Record<string, string>): void {
  pulumi.runtime.registerStackTransformation((args) => {
    if (isTaggable(args.type)) {
      args.props["tags"] = {...args.props["tags"], ...autoTags};
      return {props: args.props, opts: args.opts};
    }
    return undefined;
  });
}
