// import axios from "axios";

// const api = axios.create({
//     baseURL: "http://localhost:8000",
// });

// export async function runWorkflow(
//   resumeFile: File,
//   jdText: string
// ) {
//   const formData = new FormData();

//   formData.append("resume_file", resumeFile);
//   formData.append("jd_text", jdText);

//   const response = await api.post(
//     "/api/v1/resume-workflow",
//     formData
//   );

//   return response.data;
// }


import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});


// AFTER
export async function runWorkflow(
  resumeFile: File,
  jdText: string,
  userInstructions?: string
) {
  const formData = new FormData();

  formData.append("resume_file", resumeFile);
  formData.append("jd_text", jdText);

  if (userInstructions?.trim()) {
    formData.append("user_instructions", userInstructions);
  }

  const response = await api.post(
    "/api/v1/resume-workflow",
    formData
  );

  return response.data;
}

// ============================================================
// Human Review API
// ============================================================

export async function fetchRun(runId: string) {
  const response = await api.get(`/api/v1/review/${runId}`);
  return response.data;
}

export async function approveSuggestions(
  runId: string,
  suggestionIds: string[]
) {
  const response = await api.post("/api/v1/suggestions/approve", {
    run_id: runId,
    suggestion_ids: suggestionIds,
  });
  return response.data;
}

export async function rejectSuggestions(
  runId: string,
  suggestionIds: string[]
) {
  const response = await api.post("/api/v1/suggestions/reject", {
    run_id: runId,
    suggestion_ids: suggestionIds,
  });
  return response.data;
}

export async function reviseResume(runId: string) {
  const response = await api.post(`/api/v1/review/${runId}/revise`);
  return response.data;
}

export async function editSection(
  runId: string,
  path: string,
  value: unknown
) {
  const response = await api.post(`/api/v1/review/${runId}/section-edit`, {
    path,
    value,
  });
  return response.data;
}

export async function finalizeRun(runId: string) {
  const response = await api.post(`/api/v1/review/${runId}/finalize`);
  return response.data;
}


//
export async function fetchRunHistory() {
  const response = await api.get("/api/v1/review/runs");
  return response.data; // [{ run_id, created_at, resume_name, job_title, company, ats_before, ats_after, finalized }]
}

export async function deleteRun(runId: string) {
  const response = await api.delete(`/api/v1/review/${runId}`);
  return response.data;
}

export async function clearAllRuns() {
  const response = await api.delete("/api/v1/review/runs");
  return response.data;
}