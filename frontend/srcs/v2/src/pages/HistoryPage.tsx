import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { clearAllRuns, deleteRun, fetchRunHistory } from "../services/api";
import LoadingScreen from "../components/layout/LoadingScreen";

interface Props {
  mode?: "history" | "versions";
}

export default function HistoryPage({ mode = "history" }: Props) {
  const navigate = useNavigate();
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const isVersions = mode === "versions";

  const load = async () => {
    try {
      setLoading(true);
      setHistory(await fetchRunHistory());
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  async function remove(id: string) {
    if (!confirm("Delete this draft?")) return;
    await deleteRun(id);
    setHistory((h) => h.filter((x) => x.run_id !== id));
  }

  async function clear() {
    if (!confirm("Clear all saved drafts? This cannot be undone.")) return;
    await clearAllRuns();
    setHistory([]);
  }

  if (loading) {
    return <LoadingScreen message={isVersions ? "Loading resume versions..." : "Loading history..."} />;
  }

  return (
    <div className="min-h-full bg-gray-50">
      <div className="mx-auto max-w-6xl px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-brand-700">
              Workspace
            </p>
            <h1 className="mt-1 text-3xl font-bold text-gray-950">
              {isVersions ? "Resume Versions" : "History"}
            </h1>
            <p className="mt-2 text-sm text-gray-500">
              {isVersions
                ? "Open any generated draft and continue editing, reviewing, or exporting it."
                : "Keep track of your resume drafts and versions."}
            </p>
          </div>
          {history.length > 0 && (
            <button onClick={clear} className="text-xs font-semibold text-red-500 hover:text-red-700">
              Clear all history
            </button>
          )}
        </div>

        <div className="mt-7 overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
          {history.length === 0 ? (
            <div className="px-5 py-16 text-center">
              <div className="text-3xl">🗂️</div>
              <h2 className="mt-3 font-semibold text-gray-900">No resume versions yet</h2>
              <p className="mx-auto mt-1 max-w-md text-sm text-gray-500">
                Create a tailored resume to start building your version history.
              </p>
              <button onClick={() => navigate("/generate")} className="btn-primary mt-5">
                Create a resume
              </button>
            </div>
          ) : (
            <div className="divide-y divide-gray-100">
              {history.map((item) => (
                <div key={item.run_id} className="group flex items-center gap-4 px-4 py-4 sm:px-6">
                  <button
                    onClick={() => navigate(`/review/${item.run_id}`)}
                    className="flex min-w-0 flex-1 items-center gap-4 text-left"
                  >
                    <div className="hidden h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-700 sm:flex">
                      ▣
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="truncate text-sm font-semibold text-gray-900">
                        {item.job_title || "Untitled role"}
                      </div>
                      <div className="mt-1 truncate text-xs text-gray-500">
                        {item.resume_name || "Resume"}
                        {item.company ? ` · ${item.company}` : ""}
                      </div>
                      <div className="mt-1 text-[11px] text-gray-400">
                        {new Date(item.created_at).toLocaleString()}
                      </div>
                    </div>
                    <div className="hidden text-right sm:block">
                      <div className="text-sm font-bold text-gray-900">
                        ATS {item.ats_after ?? "—"}
                      </div>
                      <span className={`text-[10px] ${item.finalized ? "text-brand-700" : "text-gray-400"}`}>
                        {item.finalized ? "Finalized" : "Draft"}
                      </span>
                    </div>
                    <span className="text-gray-300">›</span>
                  </button>
                  <button
                    onClick={() => remove(item.run_id)}
                    className="rounded-lg px-2 py-1 text-xs text-gray-300 opacity-100 hover:bg-red-50 hover:text-red-500 sm:opacity-0 sm:group-hover:opacity-100"
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
