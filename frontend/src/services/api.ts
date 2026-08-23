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
    withCredentials: true,   // <-- required so the httpOnly cookie is sent
});

//login
export async function fetchMe() {
  const response = await api.get("/api/v1/auth/me");
  return response.data;
}

export function loginWithGoogle() {
  window.location.href = "http://localhost:8000/api/v1/auth/login";
}

export async function logout() {
  await api.post("/api/v1/auth/logout");
}

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
  user_id:string,
  value: unknown
) {
  const response = await api.post(`/api/v1/review/${runId}/section-edit`, {
    path,
    user_id,
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

export function getExportPdfUrl(runId: string) {
  return `${api.defaults.baseURL}/api/v1/review/${runId}/export/pdf`;
}

export function getExportDocxUrl(runId: string) {
  return `${api.defaults.baseURL}/api/v1/review/${runId}/export/docx`;
}

export async function chatRevise(runId: string, message: string) {
  const response = await api.post(`/api/v1/review/${runId}/chat`, { message });
  return response.data;
}