import { useEffect } from "react";
import { zodSchemaToTree } from "./zod2tree";
import { jsonToTree } from "./json2tree";
import { compareTrees } from "./compare";
import type { ZodTypeAny } from "zod";

export function useApiDiff(schema: ZodTypeAny, data: any, apiName: string) {
  useEffect(() => {
    if (!data) return;
    // zod 校验
    try {
      schema.parse(data);
    } catch (e) {
      console.error(`${apiName} zod校验失败:`, e);
    }
    // diff
    const expectedTree = zodSchemaToTree(schema);
    const actualTree = jsonToTree(data);
    const diffs = compareTrees(expectedTree, actualTree);
    console.log(`【自动化diff】${apiName}`);
    console.table(diffs);
  }, [data, schema, apiName]);
} 