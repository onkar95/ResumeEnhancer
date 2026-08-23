import { useReactToPrint } from "react-to-print";
import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { fetchRun, finalizeRun, getExportPdfUrl, getExportDocxUrl } from "../services/api";

import EditableResumeRenderer from "../components/review/EditableResumeRenderer";
import SuggestionPanel from "../components/review/SuggestionPanel";
import ChatPanel from "../components/review/ChatPanel";
import LoadingScreen from "../components/layout/LoadingScreen";

import { getRunId, saveRunId, clearRunId } from "../utils/storage";

export default function ReviewPage() {
  const { runId } = useParams();
  const navigate = useNavigate();
  const resumeRef = useRef<HTMLDivElement>(null);

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [run, setRun] = useState<any>(null);
  const [tab, setTab] = useState<"resume" | "assist">("resume");

  const resolvedRunId = runId || getRunId();

  useEffect(() => {
    if (!resolvedRunId) {
      navigate("/");
      return;
    }
    loadRun();
  }, []);

  async function loadRun() {
    if (!resolvedRunId) return;
    try {
      setLoading(true);
      const data = await fetchRun(resolvedRunId);
      saveRunId(resolvedRunId);
      setRun(data);
    } catch (err) {
      console.error(err);
      clearRunId();
      navigate("/");
    } finally {
      setLoading(false);
    }
  }

  async function refreshRun() {
    if (!resolvedRunId) return;
    try {
      setRefreshing(true);
      const data = await fetchRun(resolvedRunId);
      setRun(data);
    } finally {
      setRefreshing(false);
    }
  }

  async function handleFinalize() {
    if (!resolvedRunId) return;
    await finalizeRun(resolvedRunId);
    await refreshRun();
  }

  if (loading) return <LoadingScreen />;
  if (!run) return null;

//  const handleDownloadPdf = useReactToPrint({
//     contentRef: resumeRef,
//     documentTitle: `${run?.tailored_resume?.name || "resume"}`,
//   });

//   const handleDownloadWord = () => {
//     console.log("--", run?.tailored_resume);
//     // downloadResumeWord(run?.tailored_resume);
//   };
   {/* <button
              onClick={handleDownloadPdf}
              className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium"
            >
              Download PDF
            </button>
            <button
              onClick={handleDownloadWord}
              className="px-5 py-2 bg-blue-700 hover:bg-blue-800 text-white rounded-lg font-medium"
            >
              Download Word
            </button> */}

  return (
    <div className="w-full min-w-0 px-4 sm:px-6 lg:px-8 py-6 max-w-[1600px] mx-auto">
      {/* Header / actions */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
        <button
          onClick={() => navigate("/")}
          className="text-sm text-gray-500 hover:text-brand-700 self-start"
        >
          ← Back to Home
        </button>

        <div className="flex flex-wrap gap-2">
          {refreshing && (
            <span className="text-sm text-gray-400 self-center">Refreshing…</span>
          )}

          {!run.finalized ? (
            <button onClick={handleFinalize} className="btn-primary">
              Finalize Resume
            </button>
          ) : (
            <span className="px-4 py-2 bg-brand-100 text-brand-800 rounded-lg text-sm font-medium self-center">
              Finalized
            </span>
          )}

          <a href={getExportPdfUrl(resolvedRunId!)} className="btn-secondary">
            Download PDF
          </a>
          <a href={getExportDocxUrl(resolvedRunId!)} className="btn-secondary">
            Download Word
          </a>
        </div>
      </div>

      {run.user_instructions && (
        <div className="mb-4 text-xs bg-brand-50 border border-brand-200 rounded-lg p-3 text-brand-900 min-w-0">
          <span className="font-semibold">Your notes: </span>
          {run.user_instructions}
        </div>
      )}

      {/* Mobile tab switcher */}
      <div className="lg:hidden flex gap-2 mb-4">
        <button
          onClick={() => setTab("resume")}
          className={`flex-1 py-2 rounded-lg text-sm font-medium ${
            tab === "resume" ? "bg-brand-600 text-white" : "bg-white border border-gray-200 text-gray-600"
          }`}
        >
          Resume
        </button>
        <button
          onClick={() => setTab("assist")}
          className={`flex-1 py-2 rounded-lg text-sm font-medium ${
            tab === "assist" ? "bg-brand-600 text-white" : "bg-white border border-gray-200 text-gray-600"
          }`}
        >
          Assist
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8 items-start min-w-0">
        <div className={`lg:col-span-2 min-w-0 ${tab === "resume" ? "block" : "hidden lg:block"}`}>
          <h2 className="text-xl sm:text-2xl font-bold mb-4 text-gray-900">
            Tailored Resume{" "}
            <span className="text-sm font-normal text-gray-500">
              {run.finalized ? "(Final)" : "(Draft — click any text to edit)"}
            </span>
          </h2>

          {/* The resume itself may be wider than small screens; scope the
              horizontal scroll to this box only, never the page. */}
          <div className="overflow-x-auto">
            <div className="min-w-[640px] lg:min-w-0">
              <EditableResumeRenderer
                ref={resumeRef}
                runId={resolvedRunId!}
                resume={run.tailored_resume}
                onEdited={refreshRun}
                originalResume={run.parsed_resume}
              />
            </div>
          </div>
        </div>

        <div className={`space-y-6 min-w-0 ${tab === "assist" ? "block" : "hidden lg:block"}`}>
          <ChatPanel
            runId={resolvedRunId!}
            chatHistory={run.chat_history || []}
            revisionCount={run.revision_count || 0}
            onRevised={refreshRun}
          />

          <SuggestionPanel
            runId={resolvedRunId!}
            suggestions={run.candidate_suggestions?.suggestions || []}
            onChanged={refreshRun}
          />
        </div>
      </div>
    </div>
  );
}
