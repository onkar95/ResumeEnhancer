// export type DiffStatus =
//   | "same"
//   | "added"
//   | "removed"
//   | "modified";

// export interface DiffResult {
//   status: DiffStatus;
// }

// export function normalize(value: any): string {
//   if (value === null || value === undefined) {
//     return "";
//   }

//   return String(value)
//     .replace(/\s+/g, " ")
//     .trim()
//     .toLowerCase();
// }

// // export function compareText(
// //   original?: string,
// //   current?: string,
// // ): DiffResult {
// //   const oldValue = normalize(original);
// //   const newValue = normalize(current);

// //   if (!oldValue && newValue) {
// //     return {
// //       status: "added",
// //     };
// //   }

// //   if (oldValue && !newValue) {
// //     return {
// //       status: "removed",
// //     };
// //   }

// //   if (oldValue !== newValue) {
// //     return {
// //       status: "modified",
// //     };
// //   }

// //   return {
// //     status: "same",
// //   };
// // }

// export function compareText(
//   original?: string,
//   current?: string,
// ): DiffStatus {
//   const oldValue = normalize(original);
//   const newValue = normalize(current);

//   if (!oldValue && newValue) {
//     return "added";
//   }

//   if (oldValue && !newValue) {
//     return "removed";
//   }

//   if (oldValue !== newValue) {
//     return "modified";
//   }

//   return "same";
// }

// export function isAdded(
//   value: string,
//   originalValues: string[],
// ): boolean {
//   return !originalValues
//     .map(normalize)
//     .includes(normalize(value));
// }

// export function isRemoved(
//   value: string,
//   newValues: string[],
// ): boolean {
//   return !newValues
//     .map(normalize)
//     .includes(normalize(value));
// }

// export function findMatchingExperience(
//   originalExperiences: any[],
//   experience: any,
// ) {
//   return (
//     originalExperiences.find((exp) => {
//       return (
//         normalize(exp.company) ===
//           normalize(experience.company) &&
//         normalize(exp.role) ===
//           normalize(experience.role)
//       );
//     }) || null
//   );
// }

// export function findMatchingProject(
//   originalProjects: any[],
//   project: any,
// ) {
//   return (
//     originalProjects.find((p) => {
//       return (
//         normalize(p.title) ===
//         normalize(project.title)
//       );
//     }) || null
//   );
// }

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