import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000",
});

export async function runWorkflow(
  resumeFile: File,
  jdText: string
) {
  const formData = new FormData();

  formData.append("resume_file", resumeFile);
  formData.append("jd_text", jdText);

  const response = await api.post(
    "/api/v1/resume-workflow",
    formData
  );

  return response.data;
}
