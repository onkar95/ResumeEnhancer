import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { runWorkflow, fetchRun } from "../services/api";

import ResumeRenderer from "../components/resume/ResumeRenderer";
import LoadingScreen from "../components/layout/LoadingScreen";

import ATSCard from "../components/comparison/ATSCard";
import GapAnalysis from "../components/comparison/GapAnalysis";
import ValidationPanel from "../components/comparison/ValidationPanel";

import { setActiveRunId, getActiveRunId, saveRunId } from "../utils/storage";

export default function HomePage() {
  const navigate = useNavigate();

  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jdText, setJdText] = useState("");
  const [loading, setLoading] = useState(false);
  const [userInstructions, setUserInstructions] = useState("");
  const [result, setResult] = useState<any>(null);

  // Restore last-active run on refresh.
  useEffect(() => {
    const active = getActiveRunId();
    if (active) restoreRun(active);
  }, []);

  async function restoreRun(runId: string) {
    try {
      const data = await fetchRun(runId);
      setResult({
        run_id: data.run_id,
        parsed_resume: data.parsed_resume,
        tailored_resume: data.tailored_resume,
        gap_analysis: data.gap_analysis,
        comparison_data: data.comparison_data,
        validation_result: data.validation_result,
        candidate_suggestions: data.candidate_suggestions,
      });
    } catch (err) {
      console.error("Failed to restore run", err);
      setActiveRunId(null);
    }
  }

  async function handleSubmit() {
    if (!resumeFile) {
      alert("Please upload a resume");
      return;
    }
    if (!jdText.trim()) {
      alert("Please enter a job description");
      return;
    }

    try {
      setLoading(true);

      const response = await runWorkflow(resumeFile, jdText, userInstructions);

      setResult(response);

      if (response?.run_id) {
        setActiveRunId(response.run_id);
      }
    } catch (error) {
      console.error(error);
      alert("Resume workflow failed");
    } finally {
      setLoading(false);
    }
  }

  function handleSaveAndReview() {
    if (!result?.run_id) return;
    saveRunId(result.run_id);
    navigate(`/review/${result.run_id}`);
  }

  function handleClearCurrent() {
    setResult(null);
    setActiveRunId(null);
    setResumeFile(null);
    setUserInstructions("");
    setJdText("");
  }

  const comparison = result?.comparison_data || {};

  return (
    <div className="p-8 w-full">
      <div className="mb-8 flex items-start justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-4xl font-bold">Resume Enhancer</h1>
          <p className="text-gray-600 mt-2">
            Generate a tailored draft, compare side by side, then save it to
            review, edit, and export.
          </p>
        </div>

        <button
          onClick={() => navigate("/history")}
          className="text-sm text-blue-600 hover:text-blue-800 underline"
        >
          View History →
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-md p-6 mb-8">
        <div className="flex items-center justify-between mb-4">
          <label className="block font-semibold">Resume PDF</label>
          {(result || resumeFile || jdText) && (
            <button
              onClick={handleClearCurrent}
              className="text-xs text-gray-500 hover:text-gray-800 underline"
            >
              Clear current
            </button>
          )}
        </div>

        <input
          type="file"
          accept=".pdf"
          className="bg-amber-100 cursor-pointer p-2 rounded-sm"
          onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
        />

        {resumeFile && (
          <div className="mt-2 text-sm text-green-600">
            Selected: {resumeFile.name}
          </div>
        )}

        <div className="mt-4">
          <label className="block font-semibold mb-2">Job Description</label>
          <textarea
            className="w-full border rounded-lg p-4 h-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Paste Job Description"
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
          />
        </div>
        <div className="mt-4">
          <label className="block font-semibold mb-2">
            Additional Notes{" "}
            <span className="text-gray-400 font-normal">(optional)</span>
          </label>
          <p className="text-xs text-gray-500 mb-2">
            Mention skills you've worked with that aren't on your resume, how
            confident you are with them, or how aggressively you want the AI to
            tailor — e.g. "I've used Kafka briefly on a side project, add it if
            relevant" or "be strict, only use what's already on my resume."
          </p>
          <textarea
            className="w-full border rounded-lg p-4 h-28 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Optional — anything you want the AI to know before tailoring your resume"
            value={userInstructions}
            onChange={(e) => setUserInstructions(e.target.value)}
          />
        </div>

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="mt-6 px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium disabled:opacity-50"
        >
          {loading ? "Generating..." : "Generate Tailored Resume"}
        </button>
      </div>

      {loading && <LoadingScreen />}

      {result && (
        <>
          <div className="bg-yellow-50 border border-yellow-300 rounded-xl p-4 mb-6 flex items-center justify-between flex-wrap gap-3">
            <span className="text-sm text-yellow-800">
              This draft is saved. Click "Save & Review" to edit sections and
              export a final PDF.
            </span>
            <button
              onClick={handleSaveAndReview}
              className="px-5 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg font-medium"
            >
              Save &amp; Review
            </button>
          </div>

          <div className="grid grid-cols-1 2xl:grid-cols-3 gap-6 items-start">
            <ATSCard title="ATS Before" value={comparison.ats_before ?? "-"} />
            <ATSCard title="ATS After" value={comparison.ats_after ?? "-"} />
            <ATSCard
              title="Improvement"
              value={
                comparison.ats_before != null && comparison.ats_after != null
                  ? `${comparison.ats_after - comparison.ats_before}`
                  : "-"
              }
            />
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mt-8">
            <div>
              <h2 className="text-2xl font-bold mb-4">Original Resume</h2>
              <ResumeRenderer resume={result.parsed_resume} />
            </div>

            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold">Tailored Draft</h2>
                <div className="flex items-center gap-3 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <span className="inline-block w-3 h-3 rounded diff-added" />{" "}
                    Added/changed
                  </span>
                  <span className="flex items-center gap-1">
                    <span className="inline-block w-3 h-3 rounded diff-removed" />{" "}
                    Removed
                  </span>
                </div>
              </div>

              <ResumeRenderer
                resume={result.tailored_resume}
                originalResume={result.parsed_resume}
                diff
              />
            </div>
          </div>

          <div className="mt-10 space-y-8">
            <GapAnalysis gapAnalysis={result.gap_analysis} />
            <ValidationPanel validation={result.validation_result} />
          </div>
        </>
      )}
    </div>
  );
}
