import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { runWorkflow } from "../services/api";

import ResumeRenderer from "../components/resume/ResumeRenderer";

import LoadingScreen from "../components/layout/LoadingScreen";

import ATSCard from "../components/comparison/ATSCard";
import GapAnalysis from "../components/comparison/GapAnalysis";
import ValidationPanel from "../components/comparison/ValidationPanel";

import { saveRunId } from "../utils/storage";

export default function HomePage() {
  const navigate = useNavigate();

  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jdText, setJdText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

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

      const response = await runWorkflow(resumeFile, jdText);

      setResult(response);
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

  const comparison = result?.comparison_data || {};

  return (
    <div className="min-h-screen min-w-screen bg-slate-100">
      <div className="mx-2 p-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold">Resume Enhancer</h1>

          <p className="text-gray-600 mt-2">
            Generate a tailored draft, review and edit it, then export the final
            PDF.
          </p>
        </div>
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <div className="mb-4">
            <label className="block font-semibold mb-2">Resume PDF</label>

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
          </div>

          <div>
            <label className="block font-semibold mb-2">Job Description</label>

            <textarea
              className="
                w-full
                border
                rounded-lg
                p-4
                h-64
                focus:outline-none
                focus:ring-2
                focus:ring-blue-500
              "
              placeholder="Paste Job Description"
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
            />
          </div>

          <button
            onClick={handleSubmit}
            className="
              mt-6
              px-8
              py-3
              bg-blue-600
              hover:bg-blue-700
              text-white
              rounded-lg
              font-medium
            "
          >
            Generate Tailored Resume
          </button>
        </div>

        {loading && <LoadingScreen />}

        {result && (
          <>
            <div className="bg-yellow-50 border border-yellow-300 rounded-xl p-4 mb-6 flex items-center justify-between flex-wrap gap-3">
              <span className="text-sm text-yellow-800">
                This is a draft. Save it to review, edit sections, and export a
                final PDF.
              </span>

              <button
                onClick={handleSaveAndReview}
                className="px-5 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg font-medium"
              >
                Save &amp; Review
              </button>
            </div>

            <div className="grid grid-cols-1 2xl:grid-cols-2 gap-10 items-start">
              <ATSCard
                title="ATS Before"
                value={comparison.ats_before ?? "-"}
              />

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
                <h2 className="text-2xl font-bold mb-4">Tailored Draft</h2>

                {/* <ResumeRenderer resume={result.tailored_resume} /> */}
                <ResumeRenderer
                  resume={result.tailored_resume}
                  originalResume={result.parsed_resume}
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
    </div>
  );
}
