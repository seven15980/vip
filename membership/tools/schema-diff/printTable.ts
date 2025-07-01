import type { DiffItem } from "./compare";

export function printDiffTable(diffs: DiffItem[]) {
  const pad = (str: string, len: number) => str.padEnd(len, " ");
  const headers = ["字段名", "路径", "期望类型", "实际类型", "差异类型", "是否必填"];
  const colWidths = [10, 30, 12, 12, 10, 8];

  const color = (type: string, str: string) => {
    if (type === "missing") return `\x1b[41m${str}\x1b[0m`; // 红底
    if (type === "type-mismatch") return `\x1b[43m${str}\x1b[0m`; // 黄底
    if (type === "extra") return `\x1b[42m${str}\x1b[0m`; // 绿底
    return str;
  };

  console.log(
    headers.map((h, i) => pad(h, colWidths[i])).join(" | ")
  );
  console.log("-".repeat(colWidths.reduce((a, b) => a + b + 3, 0)));

  for (const d of diffs) {
    const row = [
      d.field,
      d.path,
      d.expectedType || "-",
      d.actualType || "-",
      d.diffType,
      d.required === undefined ? "-" : d.required ? "是" : "否",
    ].map((v, i) => pad(v, colWidths[i]));
    console.log(color(d.diffType, row.join(" | ")));
  }
} 