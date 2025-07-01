import { ZodTypeAny, ZodObject, ZodArray, ZodOptional, ZodNullable, ZodUnion, ZodDiscriminatedUnion, ZodEnum, ZodLiteral, ZodString, ZodNumber, ZodBoolean, ZodDate } from "zod";

export type SchemaTree = Record<string, { type: string; required: boolean }>;

function zodTypeToJsType(schema: ZodTypeAny): string {
  if (schema instanceof ZodString) return "string";
  if (schema instanceof ZodNumber) return "number";
  if (schema instanceof ZodBoolean) return "boolean";
  if (schema instanceof ZodDate) return "string"; // Date一般序列化为字符串
  if (schema instanceof ZodArray) return "array";
  if (schema instanceof ZodObject) return "object";
  if (schema instanceof ZodEnum) return "string";
  if (schema instanceof ZodLiteral) return typeof schema.value;
  if (schema instanceof ZodUnion || schema instanceof ZodDiscriminatedUnion) return "union";
  return "any";
}

export function zodSchemaToTree(schema: ZodTypeAny, prefix = "", required = true): SchemaTree {
  const tree: SchemaTree = {};
  const path = (key: string) => (prefix ? `${prefix}.${key}` : key);

  if (schema instanceof ZodOptional) {
    Object.assign(tree, zodSchemaToTree(schema.unwrap(), prefix, false));
  } else if (schema instanceof ZodNullable) {
    Object.assign(tree, zodSchemaToTree(schema.unwrap(), prefix, required));
  } else if (schema instanceof ZodObject) {
    const shape = schema.shape;
    for (const key in shape) {
      Object.assign(tree, zodSchemaToTree(shape[key], path(key), required));
    }
  } else if (schema instanceof ZodArray) {
    Object.assign(tree, zodSchemaToTree(schema.element, `${prefix}[]`, required));
  } else {
    tree[prefix] = { type: zodTypeToJsType(schema), required };
  }
  return tree;
} 