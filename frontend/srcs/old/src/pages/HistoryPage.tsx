import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { fetchRunHistory, deleteRun, clearAllRuns } from "../services/api";
import { saveRunId, setActiveRunId } from "../utils/storage";
import HistoryPanel from "../components/history/HistoryPanel";

export default function HistoryPage() {
  const navigate = useNavigate();
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      setLoading(true);
      const data = await fetchRunHistory();
      setHistory(data);
    } catch (err) {
      console.error("Failed to load history", err);
    } finally {
      setLoading(false);
    }
  }

  function handleSelect(runId: string) {
    saveRunId(runId);
    navigate(`/review/${runId}`);
  }

  async function handleDelete(runId: string) {
    try {
      await deleteRun(runId);
      setHistory((prev) => prev.filter((h) => h.run_id !== runId));
    } catch (err) {
      console.error("Failed to delete run", err);
      alert("Failed to delete run");
    }
  }

  async function handleClearAll() {
    if (!confirm("Clear all saved drafts? This cannot be undone.")) return;
    try {
      await clearAllRuns();
      setHistory([]);
      setActiveRunId(null);
    } catch (err) {
      console.error("Failed to clear history", err);
      alert("Failed to clear history");
    }
  }

  return (
    <div className="w-full min-w-0 px-4 sm:px-6 lg:px-8 py-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">History</h1>
          <p className="text-gray-600 mt-1 text-sm sm:text-base">
            All previously generated resume drafts. Click one to open it in Review.
          </p>
        </div>

        {history.length > 0 && (
          <button onClick={handleClearAll} className="text-sm text-red-500 hover:text-red-700 underline">
            Clear all history
          </button>
        )}
      </div>

      {loading ? (
        <div className="text-gray-400 text-sm">Loading…</div>
      ) : (
        <HistoryPanel
          history={history}
          activeRunId={null}
          onSelect={handleSelect}
          onDelete={handleDelete}
          expanded
        />
      )}
    </div>
  );
}