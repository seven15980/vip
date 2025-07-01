import { zodSchemaToTree } from "./zod2tree";
import { jsonToTree } from "./json2tree";
import { compareTrees } from "./compare";
import { printDiffTable } from "./printTable";

// 1. 引入你的zod schema
import { z } from "zod";

// 示例schema，实际使用时请替换为你的真实schema
const userProfileSchema = z.object({
  id: z.string(),
  name: z.string(),
  age: z.number().optional(),
  email: z.string().email(),
  address: z.object({
    city: z.string(),
    street: z.string(),
  }),
});

// 2. 获取后端API返回（可用fetch、axios、curl等，或直接粘贴json）
const apiResponse = {
  "id": "123",
  "name": "张三",
  "email": "zhangsan@example.com",
  "address": {
    "city": "北京"
  },
  "extra_field": "should not be here"
};

// 3. 生成结构树
const expectedTree = zodSchemaToTree(userProfileSchema);
const actualTree = jsonToTree(apiResponse);

// 4. 对比
const diffs = compareTrees(expectedTree, actualTree);

// 5. 打印页面/接口名和结果
console.log("\n【用户信息页面 /api/profile】");
printDiffTable(diffs); 