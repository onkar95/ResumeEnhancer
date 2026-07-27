const STORAGE_KEY = "resume-enhancer-run";

export interface StoredResumeRun {
  runId: string;
}

export function saveRunId(runId: string) {
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      runId,
    }),
  );
}

export function getRunId(): string | null {
  const value = localStorage.getItem(STORAGE_KEY);

  if (!value) {
    return null;
  }

  try {
    const parsed: StoredResumeRun = JSON.parse(value);

    return parsed.runId;
  } catch {
    return null;
  }
}

export function clearRunId() {
  localStorage.removeItem(STORAGE_KEY);
}