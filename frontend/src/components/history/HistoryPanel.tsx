import type { RunHistoryEntry } from "../../utils/storage";

interface Props {
  history: RunHistoryEntry[];
  activeRunId: string | null;
  onSelect: (runId: string) => void;
  onDelete: (runId: string) => void;
}

export default function HistoryPanel({
  history,
  activeRunId,
  onSelect,
  onDelete,
}: Props) {
  if (history.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow p-4 text-sm text-gray-400">
        No previous drafts yet. Generate a resume to start your history.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow p-4">
      <h3 className="font-semibold mb-3 text-sm text-gray-500 uppercase tracking-wide">
        History
      </h3>

      <div className="space-y-2 max-h-[420px] overflow-y-auto">
        {history.map((entry) => {
          const isActive = entry.runId === activeRunId;

          return (
            <div
              key={entry.runId}
              onClick={() => onSelect(entry.runId)}
              className={`
                border rounded-lg p-3 cursor-pointer transition
                ${isActive ? "border-blue-500 bg-blue-50" : "border-gray-200 hover:bg-gray-50"}
              `}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="min-w-0">
                  <div className="font-medium text-sm truncate">
                    {entry.jobTitle || "Untitled role"}
                    {entry.company ? ` · ${entry.company}` : ""}
                  </div>

                  <div className="text-xs text-gray-500 truncate">
                    {entry.resumeName || "Resume"}
                  </div>

                  <div className="text-xs text-gray-400 mt-1">
                    {new Date(entry.createdAt).toLocaleString()}
                  </div>
                </div>

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete(entry.runId);
                  }}
                  className="text-xs text-red-400 hover:text-red-600 shrink-0"
                  title="Delete from history"
                >
                  ✕
                </button>
              </div>

              {(entry.atsBefore != null || entry.atsAfter != null) && (
                <div className="flex gap-3 mt-2 text-xs">
                  <span className="text-gray-500">
                    ATS: {entry.atsBefore ?? "-"} → {entry.atsAfter ?? "-"}
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}