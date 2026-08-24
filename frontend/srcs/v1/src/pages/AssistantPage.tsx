import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { fetchRun } from "../services/api";
import LoadingScreen from "../components/layout/LoadingScreen";
import SuggestionsList from "../components/assistant/SuggestionsList";
import ChatResumeThread from "../components/assistant/ChatResumeThread";

type Tab = "suggestions" | "chat";

export default function AssistantPage() {
  const { runId } = useParams();
  const navigate = useNavigate();
  const [run, setRun] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<Tab>("suggestions");

  async function load() {
    if (!runId) return;
    try { setLoading(true); setRun(await fetchRun(runId)); }
    finally { setLoading(false); }
  }
  useEffect(() => { load(); }, [runId]);

  if (loading) return <LoadingScreen />;
  if (!run) return <div className="flex min-h-full items-center justify-center text-sm text-gray-500">Resume run not found.</div>;

  const suggestions = run.candidate_suggestions?.suggestions || [];
  const pending = suggestions.filter((s: any) => s.status === "pending").length;
  const revisionCount = run.revision_count || 0;

  return (
    <div className="flex h-[calc(100vh-57px)] min-h-0 flex-col bg-gray-50 lg:h-screen">
      <header className="shrink-0 border-b border-gray-200 bg-white">
        <div className="flex h-16 items-center justify-between gap-4 px-4 sm:px-6">
          <button onClick={() => navigate(`/review/${runId}`)} className="flex shrink-0 items-center gap-2 text-sm text-gray-500 hover:text-gray-900">← <span className="hidden sm:inline">Back to resume</span></button>
          <div className="min-w-0 text-center"><h1 className="truncate text-base font-bold text-gray-950 sm:text-lg">AI Resume Assistant</h1><p className="truncate text-xs text-gray-500">{run.tailored_resume?.name || "Current draft"}</p></div>
          <span className="shrink-0 rounded-full border border-brand-200 bg-brand-50 px-2.5 py-1 text-[11px] font-semibold text-brand-700">Draft v{Math.max(1, revisionCount + 1)}</span>
        </div>
        <nav className="grid grid-cols-2 border-t border-gray-100">
          {(["suggestions", "chat"] as Tab[]).map((item) => <button key={item} onClick={() => setTab(item)} className={`relative h-12 text-sm font-semibold ${tab === item ? "text-brand-700" : "text-gray-500 hover:text-gray-800"}`}>{item === "suggestions" ? <span className="inline-flex items-center gap-2">Suggestions {pending > 0 && <span className="rounded-full bg-brand-100 px-2 py-0.5 text-[10px]">{pending}</span>}</span> : "Chat & Resume"}{tab === item && <span className="absolute inset-x-0 bottom-0 h-0.5 bg-brand-600" />}</button>)}
        </nav>
      </header>
      <main className="min-h-0 flex-1 overflow-hidden">
        {tab === "suggestions" ? <div className="h-full overflow-y-auto"><div className="mx-auto max-w-5xl px-4 py-6 sm:px-6 lg:px-8"><SuggestionsList runId={runId!} suggestions={suggestions} onChanged={load} /></div></div> : <ChatResumeThread runId={runId!} chatHistory={run.chat_history || []} resume={run.tailored_resume} revisionCount={revisionCount} onRevised={load} />}
      </main>
    </div>
  );
}
