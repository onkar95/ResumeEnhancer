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
  const [userInstructions, setUserInstructions] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

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
    if (!resumeFile) return alert("Please upload a resume");
    if (!jdText.trim()) return alert("Please enter a job description");

    try {
      setLoading(true);
      const response = await runWorkflow(resumeFile, jdText, userInstructions);
      setResult(response);
      if (response?.run_id) setActiveRunId(response.run_id);
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
    setJdText("");
    setUserInstructions("");
  }

  const comparison = result?.comparison_data || {};

  return (
    <div className="w-full min-w-0 px-4 sm:px-6 lg:px-8 py-6 max-w-[1600px] mx-auto">
      <div className="mb-8 flex items-start justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900">Resume Enhancer</h1>
          <p className="text-gray-600 mt-2 max-w-xl">
            Generate a tailored draft, compare side by side, then save it to review, edit, and export.
          </p>
        </div>

        <button
          onClick={() => navigate("/history")}
          className="text-sm text-brand-700 hover:text-brand-800 underline"
        >
          View History →
        </button>
      </div>

      <div className="card p-6 mb-8 min-w-0">
        <div className="flex items-center justify-between mb-4">
          <label className="block font-semibold text-gray-900">Resume PDF</label>
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
          accept=".pdf , .docx"
          className="block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-brand-50 file:text-brand-700 file:font-medium hover:file:bg-brand-100 cursor-pointer"
          onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
        />

        {resumeFile && (
          <div className="mt-2 text-sm text-brand-700">Selected: {resumeFile.name}</div>
        )}

        <div className="mt-5">
          <label className="block font-semibold mb-2 text-gray-900">Job Description</label>
          <textarea
            className="w-full border border-gray-300 rounded-lg p-4 h-56 sm:h-64 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent resize-y"
            placeholder="Paste Job Description"
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
          />
        </div>

        <div className="mt-5">
          <label className="block font-semibold mb-2 text-gray-900">
            Additional Notes <span className="text-gray-400 font-normal">(optional)</span>
          </label>
          <p className="text-xs text-gray-500 mb-2">
            Mention skills you've worked with that aren't on your resume, how confident you are,
            or how aggressively to tailor — e.g. "used Kafka briefly, add it if relevant."
          </p>
          <textarea
            className="w-full border border-gray-300 rounded-lg p-4 h-24 sm:h-28 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent resize-y"
            placeholder="Optional — anything you want the AI to know"
            value={userInstructions}
            onChange={(e) => setUserInstructions(e.target.value)}
          />
        </div>

        <button onClick={handleSubmit} disabled={loading} className="btn-primary mt-6 w-full sm:w-auto">
          {loading ? "Generating..." : "Generate Tailored Resume"}
        </button>
      </div>

      {loading && <LoadingScreen />}

      {result && (
        <>
          <div className="bg-brand-50 border border-brand-200 rounded-xl p-4 mb-6 flex items-center justify-between flex-wrap gap-3 min-w-0">
            <span className="text-sm text-brand-900">
              This draft is saved. Click "Save & Review" to edit sections and export a final PDF.
            </span>
            <button onClick={handleSaveAndReview} className="btn-primary">
              Save &amp; Review
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 min-w-0">
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

          <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 lg:gap-8 mt-8 min-w-0">
            <div className="min-w-0">
              <h2 className="text-xl sm:text-2xl font-bold mb-4 text-gray-900">Original Resume</h2>
              <div className="overflow-x-auto">
                <div className="min-w-[560px] xl:min-w-0">
                  <ResumeRenderer resume={result.parsed_resume} />
                </div>
              </div>
            </div>

            <div className="min-w-0">
              <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
                <h2 className="text-xl sm:text-2xl font-bold text-gray-900">Tailored Draft</h2>
                <div className="flex items-center gap-3 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <span className="inline-block w-3 h-3 rounded diff-added" /> Added/changed
                  </span>
                  <span className="flex items-center gap-1">
                    <span className="inline-block w-3 h-3 rounded diff-removed" /> Removed
                  </span>
                </div>
              </div>
              <div className="overflow-x-auto">
                <div className="min-w-[560px] xl:min-w-0">
                  <ResumeRenderer resume={result.tailored_resume} originalResume={result.parsed_resume} diff />
                </div>
              </div>
            </div>
          </div>

          <div className="mt-10 space-y-6">
            <GapAnalysis gapAnalysis={result.gap_analysis} />
            <ValidationPanel validation={result.validation_result} />
          </div>
        </>
      )}
    </div>
  );
}