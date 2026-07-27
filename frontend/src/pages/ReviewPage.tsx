import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useReactToPrint } from "react-to-print";

import { fetchRun, finalizeRun } from "../services/api";

import EditableResumeRenderer from "../components/review/EditableResumeRenderer";
import SuggestionPanel from "../components/review/SuggestionPanel";
import LoadingScreen from "../components/layout/LoadingScreen";

import { getRunId, saveRunId, clearRunId } from "../utils/storage";

export default function ReviewPage() {
  const { runId } = useParams();

  const navigate = useNavigate();

  const resumeRef = useRef<HTMLDivElement>(null);

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const [run, setRun] = useState<any>(null);

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

  const handleDownloadPdf = useReactToPrint({
    contentRef: resumeRef,
    documentTitle: `${run?.tailored_resume?.name || "resume"}`,
  });

  if (loading) {
    return <LoadingScreen />;
  }

  if (!run) {
    return null;
  }

  return (
    <div className="min-h-screen min-w-screen bg-slate-100">
      <div className="mx-2 p-8">
        <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
          <button
            onClick={() => navigate("/")}
            className="text-sm text-gray-500 hover:text-gray-800"
          >
            ← Back to Home
          </button>

          <div className="flex gap-3 items-center">
            {refreshing && (
              <span className="text-sm text-gray-400">Refreshing…</span>
            )}

            {!run.finalized ? (
              <button
                onClick={handleFinalize}
                className="px-5 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium"
              >
                Finalize Resume
              </button>
            ) : (
              <span className="px-4 py-2 bg-green-100 text-green-800 rounded-lg text-sm">
                Finalized
              </span>
            )}

            <button
              onClick={handleDownloadPdf}
              className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium"
            >
              Download PDF
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8 items-start">
          <div className="xl:col-span-2">
            <h2 className="text-2xl font-bold mb-4">
              Tailored Resume{" "}
              {run.finalized ? "(Final)" : "(Draft — click any text to edit)"}
            </h2>

            <EditableResumeRenderer
              ref={resumeRef}
              runId={resolvedRunId!}
              resume={run.tailored_resume}
              onEdited={refreshRun}
            />
          </div>

          <div className="space-y-6">
            <SuggestionPanel
              runId={resolvedRunId!}
              suggestions={run.candidate_suggestions?.suggestions || []}
              onChanged={refreshRun}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
