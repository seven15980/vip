export type DiffType = "missing" | "type-mismatch" | "extra";
export interface DiffItem {
  field: string;
  path: string;
  expectedType?: string;
  actualType?: string;
  diffType: DiffType;
  required?: boolean;
}

export function compareTrees(
  expected: Record<string, { type: string; required: boolean }>,
  actual: Record<string, string>
): DiffItem[] {
  const diffs: DiffItem[] = [];
  for (const path in expected) {
    if (!(path in actual)) {
      diffs.push({
        field: path.split('.').pop()!,
        path,
        expectedType: expected[path].type,
        diffType: "missing",
        required: expected[path].required,
      });
    } else if (expected[path].type !== actual[path]) {
      diffs.push({
        field: path.split('.').pop()!,
        path,
        expectedType: expected[path].type,
        actualType: actual[path],
        diffType: "type-mismatch",
        required: expected[path].required,
      });
    }
  }
  for (const path in actual) {
    if (!(path in expected)) {
      diffs.push({
        field: path.split('.').pop()!,
        path,
        actualType: actual[path],
        diffType: "extra",
        required: undefined,
      });
    }
  }
  return diffs;
} 