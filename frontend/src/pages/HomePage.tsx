// import { useState } from "react";
// import { useNavigate } from "react-router-dom";

// import { runWorkflow } from "../services/api";

// import ResumeRenderer from "../components/resume/ResumeRenderer";

// import LoadingScreen from "../components/layout/LoadingScreen";

// import ATSCard from "../components/comparison/ATSCard";
// import GapAnalysis from "../components/comparison/GapAnalysis";
// import ValidationPanel from "../components/comparison/ValidationPanel";

// import { saveRunId } from "../utils/storage";

// export default function HomePage() {
//   const navigate = useNavigate();

//   const [resumeFile, setResumeFile] = useState<File | null>(null);
//   const [jdText, setJdText] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [result, setResult] = useState<any>(null);

//   async function handleSubmit() {
//     if (!resumeFile) {
//       alert("Please upload a resume");
//       return;
//     }

//     if (!jdText.trim()) {
//       alert("Please enter a job description");
//       return;
//     }

//     try {
//       setLoading(true);

//       const response = await runWorkflow(resumeFile, jdText);

//       setResult(response);
//     } catch (error) {
//       console.error(error);

//       alert("Resume workflow failed");
//     } finally {
//       setLoading(false);
//     }
//   }

//   function handleSaveAndReview() {
//     if (!result?.run_id) return;

//     saveRunId(result.run_id);

//     navigate(`/review/${result.run_id}`);
//   }

//   const comparison = result?.comparison_data || {};

//   return (
//     <div className="min-h-screen min-w-screen bg-slate-100">
//       <div className="mx-2 p-8">
//         <div className="mb-8">
//           <h1 className="text-4xl font-bold">Resume Enhancer</h1>

//           <p className="text-gray-600 mt-2">
//             Generate a tailored draft, review and edit it, then export the final
//             PDF.
//           </p>
//         </div>
//         <div className="bg-white rounded-xl shadow-md p-6 mb-8">
//           <div className="mb-4">
//             <label className="block font-semibold mb-2">Resume PDF</label>

//             <input
//               type="file"
//               accept=".pdf"
//               className="bg-amber-100 cursor-pointer p-2 rounded-sm"
//               onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
//             />

//             {resumeFile && (
//               <div className="mt-2 text-sm text-green-600">
//                 Selected: {resumeFile.name}
//               </div>
//             )}
//           </div>

//           <div>
//             <label className="block font-semibold mb-2">Job Description</label>

//             <textarea
//               className="
//                 w-full
//                 border
//                 rounded-lg
//                 p-4
//                 h-64
//                 focus:outline-none
//                 focus:ring-2
//                 focus:ring-blue-500
//               "
//               placeholder="Paste Job Description"
//               value={jdText}
//               onChange={(e) => setJdText(e.target.value)}
//             />
//           </div>

//           <button
//             onClick={handleSubmit}
//             className="
//               mt-6
//               px-8
//               py-3
//               bg-blue-600
//               hover:bg-blue-700
//               text-white
//               rounded-lg
//               font-medium
//             "
//           >
//             Generate Tailored Resume
//           </button>
//         </div>

//         {loading && <LoadingScreen />}

//         {result && (
//           <>
//             <div className="bg-yellow-50 border border-yellow-300 rounded-xl p-4 mb-6 flex items-center justify-between flex-wrap gap-3">
//               <span className="text-sm text-yellow-800">
//                 This is a draft. Save it to review, edit sections, and export a
//                 final PDF.
//               </span>

//               <button
//                 onClick={handleSaveAndReview}
//                 className="px-5 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg font-medium"
//               >
//                 Save &amp; Review
//               </button>
//             </div>

//             <div className="grid grid-cols-1 2xl:grid-cols-2 gap-10 items-start">
//               <ATSCard
//                 title="ATS Before"
//                 value={comparison.ats_before ?? "-"}
//               />

//               <ATSCard title="ATS After" value={comparison.ats_after ?? "-"} />

//               <ATSCard
//                 title="Improvement"
//                 value={
//                   comparison.ats_before != null && comparison.ats_after != null
//                     ? `${comparison.ats_after - comparison.ats_before}`
//                     : "-"
//                 }
//               />
//             </div>

//             <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mt-8">
//               <div>
//                 <h2 className="text-2xl font-bold mb-4">Original Resume</h2>

//                 <ResumeRenderer resume={result.parsed_resume} />
//               </div>

//               <div>
//                 <h2 className="text-2xl font-bold mb-4">Tailored Draft</h2>

//                 {/* <ResumeRenderer resume={result.tailored_resume} /> */}
//                 <ResumeRenderer
//                   resume={result.tailored_resume}
//                   originalResume={result.parsed_resume}
//                 />
//               </div>
//             </div>

//             <div className="mt-10 space-y-8">
//               <GapAnalysis gapAnalysis={result.gap_analysis} />

//               <ValidationPanel validation={result.validation_result} />
//             </div>
//           </>
//         )}
//       </div>
//     </div>
//   );
// }

/**localstorage with history */

// import { useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";

// import { runWorkflow } from "../services/api";

// import ResumeRenderer from "../components/resume/ResumeRenderer";
// import DiffLegend from "../components/resume/DiffLegend";
// import LoadingScreen from "../components/layout/LoadingScreen";
// import HistoryPanel from "../components/history/HistoryPanel";

// import ATSCard from "../components/comparison/ATSCard";
// import GapAnalysis from "../components/comparison/GapAnalysis";
// import ValidationPanel from "../components/comparison/ValidationPanel";

// import {
//   saveRunId,
//   saveRunResult,
//   getRunResult,
//   getActiveRunId,
//   setActiveRunId,
//   getHistory,
//   deleteRun,
//   clearAllRuns,
//   type RunHistoryEntry,
// } from "../utils/storage";

// export default function HomePage() {
//   const navigate = useNavigate();

//   const [resumeFile, setResumeFile] = useState<File | null>(null);
//   const [jdText, setJdText] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [result, setResult] = useState<any>(null);
//   const [history, setHistory] = useState<RunHistoryEntry[]>([]);
//   const [activeRunId, setActiveRunIdState] = useState<string | null>(null);

//   // Restore last-active run (and history list) on mount / refresh.
//   useEffect(() => {
//     setHistory(getHistory());

//     const active = getActiveRunId();
//     if (active) {
//       const stored = getRunResult(active);
//       if (stored) {
//         setResult(stored);
//         setActiveRunIdState(active);
//       }
//     }
//   }, []);

//   async function handleSubmit() {
//     if (!resumeFile) {
//       alert("Please upload a resume");
//       return;
//     }

//     if (!jdText.trim()) {
//       alert("Please enter a job description");
//       return;
//     }

//     try {
//       setLoading(true);

//       const response = await runWorkflow(resumeFile, jdText);

//       setResult(response);

//       if (response?.run_id) {
//         saveRunResult(response.run_id, response);
//         setActiveRunIdState(response.run_id);
//         setHistory(getHistory());
//       }
//     } catch (error) {
//       console.error(error);
//       alert("Resume workflow failed");
//     } finally {
//       setLoading(false);
//     }
//   }

//   function handleSaveAndReview() {
//     if (!result?.run_id) return;
//     saveRunId(result.run_id);
//     navigate(`/review/${result.run_id}`);
//   }

//   function handleSelectHistory(runId: string) {
//     const stored = getRunResult(runId);
//     if (!stored) return;

//     setResult(stored);
//     setActiveRunId(runId);
//     setActiveRunIdState(runId);
//   }

//   function handleDeleteHistory(runId: string) {
//     deleteRun(runId);
//     setHistory(getHistory());

//     if (runId === activeRunId) {
//       setResult(null);
//       setActiveRunIdState(null);
//     }
//   }

//   function handleClearCurrent() {
//     setResult(null);
//     setActiveRunId(null);
//     setActiveRunIdState(null);
//     setResumeFile(null);
//     setJdText("");
//   }

//   function handleClearAllHistory() {
//     if (!confirm("Clear all saved drafts? This cannot be undone.")) return;

//     clearAllRuns();
//     setHistory([]);
//     setResult(null);
//     setActiveRunIdState(null);
//   }

//   const comparison = result?.comparison_data || {};

//   return (
//     <div className="min-h-screen min-w-screen bg-slate-100">
//       <div className="mx-2 p-8">
//         <div className="mb-8 flex items-start justify-between flex-wrap gap-4">
//           <div>
//             <h1 className="text-4xl font-bold">Resume Enhancer</h1>
//             <p className="text-gray-600 mt-2">
//               Generate a tailored draft, review and edit it, then export the
//               final PDF.
//             </p>
//           </div>

//           {history.length > 0 && (
//             <button
//               onClick={handleClearAllHistory}
//               className="text-sm text-red-500 hover:text-red-700 underline"
//             >
//               Clear all history
//             </button>
//           )}
//         </div>

//         <div className="grid grid-cols-1 xl:grid-cols-4 gap-8 items-start">
//           <div className="xl:col-span-3">
//             <div className="bg-white rounded-xl shadow-md p-6 mb-8">
//               <div className="flex items-center justify-between mb-4">
//                 <label className="block font-semibold">Resume PDF</label>
//                 {(result || resumeFile || jdText) && (
//                   <button
//                     onClick={handleClearCurrent}
//                     className="text-xs text-gray-500 hover:text-gray-800 underline"
//                   >
//                     Clear current
//                   </button>
//                 )}
//               </div>

//               <input
//                 type="file"
//                 accept=".pdf"
//                 className="bg-amber-100 cursor-pointer p-2 rounded-sm"
//                 onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
//               />

//               {resumeFile && (
//                 <div className="mt-2 text-sm text-green-600">
//                   Selected: {resumeFile.name}
//                 </div>
//               )}

//               <div className="mt-4">
//                 <label className="block font-semibold mb-2">
//                   Job Description
//                 </label>

//                 <textarea
//                   className="
//                     w-full border rounded-lg p-4 h-64
//                     focus:outline-none focus:ring-2 focus:ring-blue-500
//                   "
//                   placeholder="Paste Job Description"
//                   value={jdText}
//                   onChange={(e) => setJdText(e.target.value)}
//                 />
//               </div>

//               <button
//                 onClick={handleSubmit}
//                 disabled={loading}
//                 className="
//                   mt-6 px-8 py-3 bg-blue-600 hover:bg-blue-700
//                   text-white rounded-lg font-medium disabled:opacity-50
//                 "
//               >
//                 {loading ? "Generating..." : "Generate Tailored Resume"}
//               </button>
//             </div>

//             {loading && <LoadingScreen />}

//             {result && (
//               <>
//                 <div className="bg-yellow-50 border border-yellow-300 rounded-xl p-4 mb-6 flex items-center justify-between flex-wrap gap-3">
//                   <span className="text-sm text-yellow-800">
//                     This is a draft, saved locally. Click "Save & Review" to
//                     edit sections and export a final PDF.
//                   </span>

//                   <button
//                     onClick={handleSaveAndReview}
//                     className="px-5 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg font-medium"
//                   >
//                     Save &amp; Review
//                   </button>
//                 </div>

//                 <div className="grid grid-cols-1 2xl:grid-cols-2 gap-10 items-start">
//                   <ATSCard
//                     title="ATS Before"
//                     value={comparison.ats_before ?? "-"}
//                   />

//                   <ATSCard
//                     title="ATS After"
//                     value={comparison.ats_after ?? "-"}
//                   />

//                   <ATSCard
//                     title="Improvement"
//                     value={
//                       comparison.ats_before != null &&
//                       comparison.ats_after != null
//                         ? `${comparison.ats_after - comparison.ats_before}`
//                         : "-"
//                     }
//                   />
//                 </div>

//                 <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mt-8">
//                   <div>
//                     <h2 className="text-2xl font-bold mb-4">
//                       Original Resume
//                     </h2>
//                     <ResumeRenderer resume={result.parsed_resume} />
//                   </div>

//                   <div>
//                     <div className="flex items-center justify-between mb-4">
//                       <h2 className="text-2xl font-bold">Tailored Draft</h2>
//                     </div>
//                     <DiffLegend />
//                     <ResumeRenderer
//                       resume={result.tailored_resume}
//                       originalResume={result.parsed_resume}
//                     />
//                   </div>
//                 </div>

//                 <div className="mt-10 space-y-8">
//                   <GapAnalysis gapAnalysis={result.gap_analysis} />
//                   <ValidationPanel validation={result.validation_result} />
//                 </div>
//               </>
//             )}
//           </div>

//           <div className="xl:col-span-1">
//             <HistoryPanel
//               history={history}
//               activeRunId={activeRunId}
//               onSelect={handleSelectHistory}
//               onDelete={handleDeleteHistory}
//             />
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  runWorkflow,
  fetchRun,
  fetchRunHistory,
  deleteRun,
  clearAllRuns,
} from "../services/api";

import ResumeRenderer from "../components/resume/ResumeRenderer";
import DiffLegend from "../components/resume/DiffLegend";
import LoadingScreen from "../components/layout/LoadingScreen";
import HistoryPanel from "../components/history/HistoryPanel";

import ATSCard from "../components/comparison/ATSCard";
import GapAnalysis from "../components/comparison/GapAnalysis";
import ValidationPanel from "../components/comparison/ValidationPanel";

import { setActiveRunId, getActiveRunId, saveRunId } from "../utils/storage";

export default function HomePage() {
  const navigate = useNavigate();

  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jdText, setJdText] = useState("");
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [result, setResult] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [activeRunId, setActiveRunIdState] = useState<string | null>(null);

  useEffect(() => {
    loadHistory();

    const active = getActiveRunId();
    if (active) {
      restoreRun(active);
    }
  }, []);

  async function loadHistory() {
    try {
      setHistoryLoading(true);
      const data = await fetchRunHistory();
      setHistory(data);
    } catch (err) {
      console.error("Failed to load history", err);
    } finally {
      setHistoryLoading(false);
    }
  }

  async function restoreRun(runId: string) {
    try {
      const data = await fetchRun(runId);
      // /review/{run_id} returns the stored run shape; normalize field
      // names to match what runWorkflow() returns so the same renderers work.
      setResult({
        run_id: data.run_id,
        parsed_resume: data.parsed_resume,
        tailored_resume: data.tailored_resume,
        gap_analysis: data.gap_analysis,
        comparison_data: data.comparison_data,
        validation_result: data.validation_result,
        candidate_suggestions: data.candidate_suggestions,
      });
      setActiveRunIdState(runId);
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

      const response = await runWorkflow(resumeFile, jdText);

      setResult(response);

      if (response?.run_id) {
        setActiveRunId(response.run_id);
        setActiveRunIdState(response.run_id);
        loadHistory(); // backend already persisted this run
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

  async function handleSelectHistory(runId: string) {
    await restoreRun(runId);
  }

  async function handleDeleteHistory(runId: string) {
    try {
      await deleteRun(runId);
      setHistory((prev) => prev.filter((h) => h.run_id !== runId));

      if (runId === activeRunId) {
        setResult(null);
        setActiveRunId(null);
        setActiveRunIdState(null);
      }
    } catch (err) {
      console.error("Failed to delete run", err);
      alert("Failed to delete run");
    }
  }

  function handleClearCurrent() {
    setResult(null);
    setActiveRunId(null);
    setActiveRunIdState(null);
    setResumeFile(null);
    setJdText("");
  }

  async function handleClearAllHistory() {
    if (
      !confirm(
        "Clear all saved drafts from the database? This cannot be undone.",
      )
    )
      return;

    try {
      await clearAllRuns();
      setHistory([]);
      setResult(null);
      setActiveRunId(null);
      setActiveRunIdState(null);
    } catch (err) {
      console.error("Failed to clear history", err);
      alert("Failed to clear history");
    }
  }

  const comparison = result?.comparison_data || {};

  return (
    <div className="min-h-screen min-w-screen bg-slate-100">
      <div className="mx-2 p-8">
        <div className="mb-8 flex items-start justify-between flex-wrap gap-4">
          <div>
            <h1 className="text-4xl font-bold">Resume Enhancer</h1>
            <p className="text-gray-600 mt-2">
              Generate a tailored draft, review and edit it, then export the
              final PDF.
            </p>
          </div>

          {history.length > 0 && (
            <button
              onClick={handleClearAllHistory}
              className="text-sm text-red-500 hover:text-red-700 underline"
            >
              Clear all history
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-4 gap-8 items-start">
          <div className="xl:col-span-3">
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
                <label className="block font-semibold mb-2">
                  Job Description
                </label>
                <textarea
                  className="w-full border rounded-lg p-4 h-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Paste Job Description"
                  value={jdText}
                  onChange={(e) => setJdText(e.target.value)}
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
                    This draft is saved in the database. Click "Save & Review"
                    to edit sections and export a final PDF.
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
                  <ATSCard
                    title="ATS After"
                    value={comparison.ats_after ?? "-"}
                  />
                  <ATSCard
                    title="Improvement"
                    value={
                      comparison.ats_before != null &&
                      comparison.ats_after != null
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
                    <DiffLegend />
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

          <div className="xl:col-span-1">
            {historyLoading ? (
              <div className="bg-white rounded-xl shadow p-4 text-sm text-gray-400">
                Loading history…
              </div>
            ) : (
              <HistoryPanel
                history={history}
                activeRunId={activeRunId}
                onSelect={handleSelectHistory}
                onDelete={handleDeleteHistory}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
