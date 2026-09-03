import { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { fetchRun, finalizeRun } from "../services/api";
import LoadingScreen from "../components/layout/LoadingScreen";
import SuggestionsList from "../components/assistant/SuggestionsList";
import ChatResumeThread from "../components/assistant/ChatResumeThread";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { clearRunId, getRunId, saveRunId } from "../utils/storage";

type Tab = "suggestions" | "chat";

export default function AssistantPage() {
  const { runId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const resolved = runId || getRunId();
  const queryClient = useQueryClient();

  const tab: Tab = location.pathname.endsWith("/chat") ? "chat" : "suggestions";

  const {
    data: run,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["run", resolved],
    queryFn: () => fetchRun(resolved!),
    enabled: !!resolved,
  });

  useEffect(() => {
    if (isError) {
      clearRunId();
      navigate("/");
    }
  }, [isError]);

  useEffect(() => {
    if (resolved) saveRunId(resolved);
  }, [resolved]);

  async function refresh() {
    // used after edits/approvals/chat — force a real refetch, don't just rely on staleTime
    await queryClient.invalidateQueries({ queryKey: ["run", resolved] });
  }

  async function finalize() {
    if (!resolved) return;
    await finalizeRun(resolved);
    await refresh();
  }

  if (isLoading) return <LoadingScreen message="Loading AI assistant..." />;
  if (!run) {
    return (
      <div className="flex min-h-full items-center justify-center text-sm text-gray-500">
        Resume run not found.
      </div>
    );
  }

  const suggestions = run.candidate_suggestions?.suggestions || [];
  const pending = suggestions.filter((s: any) => s.status === "pending").length;
  const revisionCount = run.revision_count || 0;

  const goToTab = (next: Tab) => {
    navigate(`/review/${runId}/assistant/${next}`);
  };

  return (
    <div className="flex h-full min-h-0 flex-col bg-gray-50">
      <header className="shrink-0 border-b border-gray-200 bg-white">
        <div className="flex min-h-16 items-center justify-between gap-4 px-4 sm:px-6">
          <button
            onClick={() => navigate(`/review/${runId}`)}
            className="flex shrink-0 items-center gap-2 text-sm text-gray-500 hover:text-gray-900"
          >
            ← <span className="hidden sm:inline">Back to review</span>
          </button>
          <div className="min-w-0 text-center">
            <h1 className="truncate text-base font-bold text-gray-950 sm:text-lg">
              AI Resume Assistant
            </h1>
            <p className="truncate text-xs text-gray-500">
              {run.tailored_resume?.name || "Current draft"}
            </p>
          </div>
          <span className="shrink-0 rounded-full border border-brand-200 bg-brand-50 px-2.5 py-1 text-[11px] font-semibold text-brand-700">
            Draft v{Math.max(1, revisionCount + 1)}
          </span>
        </div>

        <nav className="grid grid-cols-2 border-t border-gray-100">
          <button
            onClick={() => goToTab("suggestions")}
            className={`relative h-12 text-sm font-semibold ${tab === "suggestions" ? "text-brand-700" : "text-gray-500 hover:text-gray-800"}`}
          >
            <span className="inline-flex items-center gap-2">
              Suggestions
              {pending > 0 && (
                <span className="rounded-full bg-brand-100 px-2 py-0.5 text-[10px]">
                  {pending}
                </span>
              )}
            </span>
            {tab === "suggestions" && (
              <span className="absolute inset-x-0 bottom-0 h-0.5 bg-brand-600" />
            )}
          </button>
          <button
            onClick={() => goToTab("chat")}
            className={`relative h-12 text-sm font-semibold ${tab === "chat" ? "text-brand-700" : "text-gray-500 hover:text-gray-800"}`}
          >
            Chat & Resume
            {tab === "chat" && (
              <span className="absolute inset-x-0 bottom-0 h-0.5 bg-brand-600" />
            )}
          </button>
        </nav>
      </header>

      <main className="min-h-0 flex-1 overflow-hidden">
        {tab === "suggestions" ? (
          <div className="h-full overflow-y-auto">
            <div className="mx-auto max-w-5xl px-4 py-6 sm:px-6 lg:px-8">
              <SuggestionsList
                runId={runId!}
                suggestions={suggestions}
                onChanged={refresh}
              />
            </div>
          </div>
        ) : (
          <ChatResumeThread
            runId={runId!}
            chatHistory={run.chat_history || []}
            resume={run.tailored_resume}
            revisionCount={revisionCount}
            onRevised={refresh}
          />
        )}
      </main>
    </div>
  );
}
