import { useState } from "react";

import {
  approveSuggestions,
  rejectSuggestions,
  reviseResume,
} from "../../services/api";

interface Suggestion {
  suggestion_id: string;
  section: string;
  subsection?: string;
  current_content?: string;
  suggested_content: any;
  reason: string;
  confidence: number;
  status: string;
}

interface Props {
  runId: string;
  suggestions: Suggestion[];
  onChanged: () => void;
}

export default function SuggestionsPanel({
  runId,
  suggestions,
  onChanged,
}: Props) {
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [busy, setBusy] = useState(false);

  const pending = suggestions.filter((s) => s.status === "pending");
  const approved = suggestions.filter((s) => s.status === "approved");

  function toggle(id: string) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  }

  async function handleApprove() {
    if (selected.size === 0) return;
    setBusy(true);
    try {
      await approveSuggestions(runId, Array.from(selected));
      setSelected(new Set());
      onChanged();
    } finally {
      setBusy(false);
    }
  }

  async function handleReject() {
    if (selected.size === 0) return;
    setBusy(true);
    try {
      await rejectSuggestions(runId, Array.from(selected));
      setSelected(new Set());
      onChanged();
    } finally {
      setBusy(false);
    }
  }

  async function handleRegenerate() {
    setBusy(true);
    try {
      await reviseResume(runId);
      onChanged();
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Failed to regenerate resume");
    } finally {
      setBusy(false);
    }
  }

  function renderSuggestedContent(s: Suggestion) {
    if (typeof s.suggested_content === "string") {
      return <p className="text-sm text-gray-700">{s.suggested_content}</p>;
    }

    if (s.suggested_content?.title) {
      return (
        <>
          <div className="font-semibold text-sm">
            {s.suggested_content.title}
          </div>
          <ul className="list-disc ml-5 text-xs text-gray-600 mt-1">
            {s.suggested_content.bullet_points?.map((b: string, i: number) => (
              <li key={i}>{b}</li>
            ))}
          </ul>
        </>
      );
    }

    return (
      <p className="text-sm text-gray-700">
        {JSON.stringify(s.suggested_content)}
      </p>
    );
  }

  if (suggestions.length === 0) {
    return (
      <div className="bg-white rounded-xl p-6 shadow text-gray-500 text-sm">
        No suggestions for this draft.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl p-6 shadow space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <h2 className="text-xl font-bold">Suggestions</h2>

        <div className="flex gap-2">
          <button
            onClick={handleApprove}
            disabled={busy || selected.size === 0}
            // AFTER
            className="text-sm bg-brand-600 hover:bg-brand-700 text-white px-3 py-1.5 rounded-lg disabled:opacity-50 transition"
          >
            Approve Selected
          </button>
          <button
            onClick={handleReject}
            disabled={busy || selected.size === 0}
// AFTER
            className="text-sm bg-brand-600 hover:bg-brand-700 text-white px-3 py-1.5 rounded-lg disabled:opacity-50 transition"          >
            Reject Selected
          </button>
        </div>
      </div>

      {approved.length > 0 && (
        <div className="bg-green-50 border border-green-200 rounded p-3 flex items-center justify-between flex-wrap gap-2">
          <span className="text-sm text-green-800">
            {approved.length} suggestion{approved.length > 1 ? "s" : ""}{" "}
            approved, not yet applied.
          </span>
          <button
            onClick={handleRegenerate}
            disabled={busy}
            className="text-sm bg-blue-600 text-white px-3 py-1.5 rounded disabled:opacity-50"
          >
            {busy ? "Regenerating..." : "Regenerate Resume with Approved"}
          </button>
        </div>
      )}

      <div className="space-y-3">
        {pending.map((s) => (
          <label
            key={s.suggestion_id}
            className="flex gap-3 border rounded-lg p-3 cursor-pointer hover:bg-gray-50"
          >
            <input
              type="checkbox"
              checked={selected.has(s.suggestion_id)}
              onChange={() => toggle(s.suggestion_id)}
              className="mt-1"
            />
            <div className="flex-1 min-w-0">
              <div className="text-xs uppercase tracking-wide text-gray-400">
                {s.section}
                {s.subsection ? ` · ${s.subsection}` : ""}
              </div>
              <div className="mt-1">{renderSuggestedContent(s)}</div>
              <div className="text-xs text-gray-500 mt-1">{s.reason}</div>
            </div>
          </label>
        ))}

        {pending.length === 0 && (
          <p className="text-sm text-gray-400">
            No pending suggestions left to review.
          </p>
        )}
      </div>
    </div>
  );
}

