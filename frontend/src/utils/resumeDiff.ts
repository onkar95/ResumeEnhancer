

export type DiffType = "normal" | "added" | "removed";

export interface DiffToken {
  text: string;
  type: DiffType;
}

function normalize(word: string) {
  return word.toLowerCase().trim();
}

function tokenize(text: string): string[] {
  if (!text) return [];
  return text.split(/\s+/).filter(Boolean);
}

export function diffWords(
  original = "",
  current = "",
): DiffToken[] {
  const a = tokenize(original);
  const b = tokenize(current);

  const m = a.length;
  const n = b.length;

  const dp = Array.from({ length: m + 1 }, () =>
    Array(n + 1).fill(0),
  );

  for (let i = m - 1; i >= 0; i--) {
    for (let j = n - 1; j >= 0; j--) {
      if (normalize(a[i]) === normalize(b[j])) {
        dp[i][j] = dp[i + 1][j + 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i + 1][j], dp[i][j + 1]);
      }
    }
  }

  const result: DiffToken[] = [];

  let i = 0;
  let j = 0;

  while (i < m && j < n) {
    if (normalize(a[i]) === normalize(b[j])) {
      result.push({
        text: b[j],
        type: "normal",
      });

      i++;
      j++;
    } else if (dp[i + 1][j] >= dp[i][j + 1]) {
      result.push({
        text: a[i],
        type: "removed",
      });

      i++;
    } else {
      result.push({
        text: b[j],
        type: "added",
      });

      j++;
    }
  }

  while (i < m) {
    result.push({
      text: a[i],
      type: "removed",
    });

    i++;
  }

  while (j < n) {
    result.push({
      text: b[j],
      type: "added",
    });

    j++;
  }

  return result;
}