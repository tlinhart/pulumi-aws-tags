import * as taggableResourceTypes from "./taggable_resource_types.json";

/**
 * Return if the given resource type is a taggable AWS resource.
 */
export function isTaggable(t: string): boolean {
  return taggableResourceTypes.indexOf(t) !== -1;
}
