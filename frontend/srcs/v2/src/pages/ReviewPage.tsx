import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { fetchRun, finalizeRun, getExportPdfUrl, getExportDocxUrl } from "../services/api";
import EditableResumeRenderer from "../components/review/EditableResumeRenderer";
import LoadingScreen from "../components/layout/LoadingScreen";
import ATSCard from "../components/comparison/ATSCard";
import GapAnalysis from "../components/comparison/GapAnalysis";
import ValidationPanel from "../components/comparison/ValidationPanel";
import { getRunId, saveRunId, clearRunId } from "../utils/storage";

export default function ReviewPage() {
  const { runId } = useParams();
  const navigate = useNavigate();
  const resolved = runId || getRunId();
  const [run, setRun] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [view, setView] = useState<"compare" | "tailored" | "original">("compare");
  const [showChanges, setShowChanges] = useState(true);

  async function load() {
    if (!resolved) return;
    try { setLoading(true); const data = await fetchRun(resolved); saveRunId(resolved); setRun(data); }
    catch (e) { console.error(e); clearRunId(); navigate("/"); }
    finally { setLoading(false); }
  }
  useEffect(() => { load(); }, [resolved]);
  async function refresh() { if (!resolved) return; setRefreshing(true); try { setRun(await fetchRun(resolved)); } finally { setRefreshing(false); } }
  async function finalize() { if (!resolved) return; await finalizeRun(resolved); await refresh(); }

  if (loading) return <LoadingScreen message="Loading resume review..." />;
  if (!run) return null;
  const comparison = run.comparison_data || {};

  const ResumePanel = ({ resume, original }: { resume: any; original?: any }) => (
    <div className="overflow-x-auto">
      <div className="min-w-[640px] lg:min-w-0">
        <EditableResumeRenderer
          runId={resolved!}
          resume={resume}
          originalResume={original}
          onEdited={refresh}
        />
      </div>
    </div>
  );

  return <div className="min-h-full bg-gray-50">
    <div className="sticky top-0 z-30 border-b border-gray-200 bg-white">
      <div className="mx-auto flex max-w-[1500px] items-center justify-between gap-3 px-4 py-3 sm:px-6 lg:px-8">
        <button onClick={() => navigate("/")} className="text-sm text-gray-500 hover:text-gray-900">← <span className="hidden sm:inline">Dashboard</span></button>
        <div className="min-w-0 text-center"><h1 className="truncate text-base font-bold text-gray-950 sm:text-lg">Review & Compare</h1><p className="truncate text-xs text-gray-500">{run.tailored_resume?.name || "Resume"}</p></div>
        <div className="flex shrink-0 items-center gap-2">
          <span className="hidden rounded-full bg-brand-50 px-2.5 py-1 text-[10px] font-semibold text-brand-700 sm:inline-flex">{run.finalized ? "Finalized" : "Draft"}</span>
          <button onClick={() => navigate(`/review/${resolved}/assistant/suggestions`)} className="btn-primary px-3 py-2 text-xs">AI Assistant</button>
        </div>
      </div>
      <div className="mx-auto max-w-[1500px] border-t border-gray-100 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-3">{(["compare", "tailored", "original"] as const).map((v) => <button key={v} onClick={() => setView(v)} className={`relative h-11 text-xs font-semibold sm:text-sm ${view === v ? "text-brand-700" : "text-gray-500"}`}>{v === "compare" ? "Compare" : v === "tailored" ? "Tailored resume" : "Original resume"}{view === v && <span className="absolute inset-x-0 bottom-0 h-0.5 bg-brand-600" />}</button>)}</div>
      </div>
    </div>

    <div className="mx-auto max-w-[1500px] px-4 py-5 sm:px-6 lg:px-8">
      <div className="grid gap-3 sm:grid-cols-3"><ATSCard title="ATS Before" value={comparison.ats_before ?? "-"} /><ATSCard title="ATS After" value={comparison.ats_after ?? "-"} /><ATSCard title="Improvement" value={comparison.ats_before != null && comparison.ats_after != null ? `+${comparison.ats_after - comparison.ats_before}` : "-"} /></div>

      <div className="mt-5 flex flex-col gap-2 rounded-xl border border-brand-100 bg-brand-50 px-4 py-3 text-sm sm:flex-row sm:items-center sm:justify-between"><span className="text-brand-900">Review the AI changes, make inline edits, then finalize when ready.</span><div className="flex gap-2"><a href={getExportPdfUrl(resolved!)} className="btn-secondary px-3 py-2 text-xs">PDF</a><a href={getExportDocxUrl(resolved!)} className="btn-secondary px-3 py-2 text-xs">Word</a>{run.finalized ? <span className="rounded-lg bg-brand-600 px-3 py-2 text-xs font-semibold text-white">Finalized</span> : <button onClick={finalize} className="btn-primary px-3 py-2 text-xs">Finalize</button>}</div></div>

      {view === "compare" && (
        <>
          <div className="mt-6 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-gray-200 bg-white px-4 py-3 shadow-sm">
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => setShowChanges((value) => !value)}
                aria-pressed={showChanges}
                title={showChanges ? "Hide changes" : "Show changes"}
                className={`inline-flex h-9 items-center gap-2 rounded-lg border px-3 text-xs font-semibold transition ${showChanges ? "border-brand-200 bg-brand-50 text-brand-700" : "border-gray-200 bg-white text-gray-600 hover:bg-gray-50"}`}
              >
                <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                  <path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z" />
                  <circle cx="12" cy="12" r="2.5" />
                </svg>
                {showChanges ? "Changes on" : "Changes off"}
              </button>
              <span className="text-xs text-gray-500">{showChanges ? "Added text is green and removed text is red." : "Showing the tailored resume normally."}</span>
            </div>
            {showChanges && (
              <div className="flex items-center gap-4 text-[11px] font-medium text-gray-500">
                <span className="inline-flex items-center gap-1.5"><span className="h-2.5 w-2.5 rounded bg-green-200" /> Added / changed</span>
                <span className="inline-flex items-center gap-1.5"><span className="h-2.5 w-2.5 rounded bg-red-200" /> Removed</span>
              </div>
            )}
          </div>

          <div className="mt-5 grid gap-6 xl:grid-cols-2">
            <section className="min-w-0">
              <div className="mb-3 flex items-center justify-between">
                <h2 className="font-bold text-gray-950">Original resume</h2>
                <span className="text-[10px] text-gray-400">Original</span>
              </div>
              <ResumePanel resume={run.parsed_resume} />
            </section>
            <section className="min-w-0">
              <div className="mb-3 flex items-center justify-between">
                <h2 className="font-bold text-gray-950">Tailored resume</h2>
                <span className="text-[10px] text-brand-700">Current draft</span>
              </div>
              <ResumePanel resume={run.tailored_resume} original={showChanges ? run.parsed_resume : undefined} />
            </section>
          </div>
        </>
      )}
      {view === "tailored" && <div className="mx-auto mt-6 max-w-4xl"><ResumePanel resume={run.tailored_resume} /></div>}
      {view === "original" && <div className="mx-auto mt-6 max-w-4xl"><ResumePanel resume={run.parsed_resume} /></div>}

      <div className="mt-8 grid gap-6 xl:grid-cols-2"><GapAnalysis gapAnalysis={run.gap_analysis} /><ValidationPanel validation={run.validation_result} /></div>
    </div>
  </div>;
}
