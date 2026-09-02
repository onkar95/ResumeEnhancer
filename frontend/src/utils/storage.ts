

const ACTIVE_KEY = "resume-enhancer-active-run";

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

// Legacy aliases kept so ReviewPage.tsx needs no changes.
export const saveRunId = setActiveRunId;
export const getRunId = getActiveRunId;
export const clearRunId = () => setActiveRunId(null);