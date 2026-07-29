// const STORAGE_KEY = "resume-enhancer-run";

// export interface StoredResumeRun {
//   runId: string;
// }

// export function saveRunId(runId: string) {
//   localStorage.setItem(
//     STORAGE_KEY,
//     JSON.stringify({
//       runId,
//     }),
//   );
// }

// export function getRunId(): string | null {
//   const value = localStorage.getItem(STORAGE_KEY);

//   if (!value) {
//     return null;
//   }

//   try {
//     const parsed: StoredResumeRun = JSON.parse(value);

//     return parsed.runId;
//   } catch {
//     return null;
//   }
// }

// export function clearRunId() {
//   localStorage.removeItem(STORAGE_KEY);
// }

const HISTORY_KEY = "resume-enhancer-history";
const ACTIVE_KEY = "resume-enhancer-active-run";
const RUN_DATA_PREFIX = "resume-enhancer-run-";
const LEGACY_STORAGE_KEY = "resume-enhancer-run";

const MAX_HISTORY = 15; // evict oldest beyond this to avoid quota issues

export interface RunHistoryEntry {
  runId: string;
  createdAt: string;
  resumeName?: string;
  jobTitle?: string;
  company?: string;
  atsBefore?: number;
  atsAfter?: number;
}

interface StoredRunData {
  runId: string;
  createdAt: string;
  result: any;
}

function safeParse<T>(value: string | null, fallback: T): T {
  if (!value) return fallback;
  try {
    return JSON.parse(value) as T;
  } catch {
    return fallback;
  }
}

// ---------------------------------------------------------------
// History index
// ---------------------------------------------------------------

export function getHistory(): RunHistoryEntry[] {
  return safeParse<RunHistoryEntry[]>(localStorage.getItem(HISTORY_KEY), []);
}

function saveHistory(history: RunHistoryEntry[]) {
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
}

// ---------------------------------------------------------------
// Full run persistence
// ---------------------------------------------------------------

export function saveRunResult(runId: string, result: any): void {
  const createdAt = new Date().toISOString();
  const stored: StoredRunData = { runId, createdAt, result };

  const entry: RunHistoryEntry = {
    runId,
    createdAt,
    resumeName: result?.parsed_resume?.name,
    jobTitle: result?.parsed_jd?.job_details?.title,
    company: result?.parsed_jd?.job_details?.company,
    atsBefore: result?.comparison_data?.ats_before,
    atsAfter: result?.comparison_data?.ats_after,
  };

  let history = getHistory().filter((h) => h.runId !== runId);
  history.unshift(entry);

  const persist = () => {
    localStorage.setItem(RUN_DATA_PREFIX + runId, JSON.stringify(stored));
    saveHistory(history);
  };

  try {
    persist();
  } catch (err) {
    // Quota exceeded: drop oldest runs and retry once.
    console.warn("localStorage quota hit, trimming history", err);
    while (history.length > 1) {
      const evicted = history.pop();
      if (evicted) {
        localStorage.removeItem(RUN_DATA_PREFIX + evicted.runId);
      }
      try {
        persist();
        break;
      } catch {
        continue;
      }
    }
  }

  if (history.length > MAX_HISTORY) {
    const overflow = history.splice(MAX_HISTORY);
    overflow.forEach((h) => localStorage.removeItem(RUN_DATA_PREFIX + h.runId));
    saveHistory(history);
  }

  setActiveRunId(runId);
}

export function getRunResult(runId: string): any | null {
  const stored = safeParse<StoredRunData | null>(
    localStorage.getItem(RUN_DATA_PREFIX + runId),
    null,
  );
  return stored?.result ?? null;
}

export function deleteRun(runId: string): void {
  localStorage.removeItem(RUN_DATA_PREFIX + runId);
  saveHistory(getHistory().filter((h) => h.runId !== runId));
  if (getActiveRunId() === runId) {
    setActiveRunId(null);
  }
}

export function clearAllRuns(): void {
  getHistory().forEach((h) => localStorage.removeItem(RUN_DATA_PREFIX + h.runId));
  localStorage.removeItem(HISTORY_KEY);
  localStorage.removeItem(ACTIVE_KEY);
  localStorage.removeItem(LEGACY_STORAGE_KEY);
}

// ---------------------------------------------------------------
// "Which run is currently shown on the homepage" pointer
// ---------------------------------------------------------------

export function setActiveRunId(runId: string | null): void {
  if (runId) {
    localStorage.setItem(ACTIVE_KEY, runId);
  } else {
    localStorage.removeItem(ACTIVE_KEY);
  }
}

export function getActiveRunId(): string | null {
  return localStorage.getItem(ACTIVE_KEY);
}

// ---------------------------------------------------------------
// Legacy API (kept so ReviewPage's existing calls keep working)
// ---------------------------------------------------------------

export function saveRunId(runId: string) {
  setActiveRunId(runId);
  localStorage.setItem(LEGACY_STORAGE_KEY, JSON.stringify({ runId }));
}

export function getRunId(): string | null {
  const active = getActiveRunId();
  if (active) return active;

  const value = localStorage.getItem(LEGACY_STORAGE_KEY);
  if (!value) return null;

  try {
    const parsed = JSON.parse(value);
    return parsed.runId ?? null;
  } catch {
    return null;
  }
}

export function clearRunId() {
  localStorage.removeItem(LEGACY_STORAGE_KEY);
  setActiveRunId(null);
}