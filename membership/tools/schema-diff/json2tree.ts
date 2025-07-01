export type JsonTree = Record<string, string>;

export function jsonToTree(obj: any, prefix = ""): JsonTree {
  const tree: JsonTree = {};
  const path = (key: string) => (prefix ? `${prefix}.${key}` : key);

  if (Array.isArray(obj)) {
    if (obj.length > 0) {
      Object.assign(tree, jsonToTree(obj[0], `${prefix}[]`));
    } else {
      tree[`${prefix}[]`] = "array";
    }
  } else if (obj !== null && typeof obj === "object") {
    for (const key in obj) {
      Object.assign(tree, jsonToTree(obj[key], path(key)));
    }
  } else {
    tree[prefix] = typeof obj;
  }
  return tree;
} 