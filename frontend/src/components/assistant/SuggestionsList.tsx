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

export default function SuggestionsList({
  runId,
  suggestions,
  onChanged,
}: Props) {
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const [busy, setBusy] = useState(false);

  const [error, setError] = useState<string | null>(null);

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

  function selectAll() {
    if (selected.size === pending.length) {
      setSelected(new Set());
      return;
    }

    setSelected(new Set(pending.map((s) => s.suggestion_id)));
  }

  async function handleApprove() {
    if (selected.size === 0) {
      return;
    }

    setBusy(true);
    setError(null);

    try {
      await approveSuggestions(runId, Array.from(selected));

      setSelected(new Set());

      onChanged();
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to approve suggestions.");
    } finally {
      setBusy(false);
    }
  }

  async function handleReject() {
    if (selected.size === 0) {
      return;
    }

    setBusy(true);
    setError(null);

    try {
      await rejectSuggestions(runId, Array.from(selected));

      setSelected(new Set());

      onChanged();
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to reject suggestions.");
    } finally {
      setBusy(false);
    }
  }

  async function handleRegenerate() {
    setBusy(true);
    setError(null);

    try {
      await reviseResume(runId);

      onChanged();
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to regenerate resume.");
    } finally {
      setBusy(false);
    }
  }

  function renderSuggestedContent(suggestion: Suggestion) {
    const content = suggestion.suggested_content;

    if (typeof content === "string") {
      return (
        <p
          className="
          text-sm
          text-gray-700
          leading-6
        "
        >
          {content}
        </p>
      );
    }

    if (content?.title) {
      return (
        <div>
          <div
            className="
            font-semibold
            text-sm
            text-gray-900
          "
          >
            {content.title}
          </div>

          {content.bullet_points?.length > 0 && (
            <ul
              className="
              list-disc
              ml-5
              text-sm
              text-gray-600
              mt-2
              space-y-1
            "
            >
              {content.bullet_points.map((bullet: string, index: number) => (
                <li key={index}>{bullet}</li>
              ))}
            </ul>
          )}
        </div>
      );
    }

    return (
      <p
        className="
        text-sm
        text-gray-700
        break-words
      "
      >
        {JSON.stringify(content, null, 2)}
      </p>
    );
  }

  if (suggestions.length === 0) {
    return (
      <div
        className="
        max-w-3xl
        mx-auto
      "
      >
        <div
          className="
          bg-white
          border
          border-gray-200
          rounded-2xl
          p-8
          text-center
        "
        >
          <div
            className="
            text-3xl
            mb-3
          "
          >
            ✨
          </div>

          <h2
            className="
            font-bold
            text-gray-900
          "
          >
            Your resume looks good
          </h2>

          <p
            className="
            text-sm
            text-gray-500
            mt-1
          "
          >
            No AI suggestions were generated for this draft.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div
      className="
      max-w-4xl
      mx-auto
      space-y-5
    "
    >
      {/* ======================================================
          HEADER
      ====================================================== */}

      <div
        className="
        bg-white
        border
        border-gray-200
        rounded-2xl
        p-5
      "
      >
        <div
          className="
          flex
          flex-col
          sm:flex-row
          sm:items-center
          justify-between
          gap-4
        "
        >
          <div>
            <h2
              className="
              text-lg
              font-bold
              text-gray-900
            "
            >
              AI Suggestions
            </h2>

            <p
              className="
              text-sm
              text-gray-500
              mt-1
            "
            >
              Review the improvements before applying them to your resume.
            </p>
          </div>

          <button
            onClick={selectAll}
            disabled={pending.length === 0}
            className="
              text-xs
              font-medium
              text-brand-700
              hover:text-brand-800
              disabled:text-gray-400
            "
          >
            {selected.size === pending.length && pending.length > 0
              ? "Clear selection"
              : "Select all"}
          </button>
        </div>

        {/* Actions */}

        {pending.length > 0 && (
          <div
            className="
            flex
            flex-wrap
            gap-2
            mt-5
            pt-4
            border-t
            border-gray-100
          "
          >
            <button
              onClick={handleApprove}
              disabled={busy || selected.size === 0}
              className="
                text-sm
                bg-brand-600
                hover:bg-brand-700
                text-white
                px-4
                py-2
                rounded-lg
                disabled:opacity-40
                transition
              "
            >
              Approve selected
            </button>

            <button
              onClick={handleReject}
              disabled={busy || selected.size === 0}
              className="
                text-sm
                bg-white
                border
                border-gray-300
                hover:bg-gray-50
                text-gray-700
                px-4
                py-2
                rounded-lg
                disabled:opacity-40
                transition
              "
            >
              Reject selected
            </button>

            {selected.size > 0 && (
              <span
                className="
                text-xs
                text-gray-500
                self-center
              "
              >
                {selected.size} selected
              </span>
            )}
          </div>
        )}
      </div>

      {/* Error */}

      {error && (
        <div
          className="
          rounded-lg
          bg-red-50
          border
          border-red-200
          px-4
          py-3
          text-sm
          text-red-700
        "
        >
          {error}
        </div>
      )}

      {/* ======================================================
          APPROVED
      ====================================================== */}

      {approved.length > 0 && (
        <div
          className="
          bg-green-50
          border
          border-green-200
          rounded-xl
          p-4
        "
        >
          <div
            className="
            flex
            flex-col
            sm:flex-row
            sm:items-center
            justify-between
            gap-3
          "
          >
            <div>
              <div
                className="
                font-semibold
                text-sm
                text-green-900
              "
              >
                {approved.length} suggestion
                {approved.length !== 1 ? "s" : ""} approved
              </div>

              <div
                className="
                text-xs
                text-green-700
                mt-0.5
              "
              >
                Regenerate the resume to apply the approved changes.
              </div>
            </div>

            <button
              onClick={handleRegenerate}
              disabled={busy}
              className="
                shrink-0
                text-sm
                bg-green-600
                hover:bg-green-700
                text-white
                px-4
                py-2
                rounded-lg
                disabled:opacity-40
              "
            >
              {busy ? "Regenerating..." : "Regenerate resume"}
            </button>
          </div>
        </div>
      )}

      {/* ======================================================
          SUGGESTIONS
      ====================================================== */}

      <div className="space-y-3">
        {pending.map((suggestion) => (
          <label
            key={suggestion.suggestion_id}
            className={`
                block
                bg-white
                border
                rounded-xl
                p-4
                cursor-pointer
                transition
                ${
                  selected.has(suggestion.suggestion_id)
                    ? "border-brand-400 ring-2 ring-brand-50"
                    : "border-gray-200 hover:border-gray-300"
                }
              `}
          >
            <div
              className="
                flex
                gap-3
              "
            >
              <input
                type="checkbox"
                checked={selected.has(suggestion.suggestion_id)}
                onChange={() => toggle(suggestion.suggestion_id)}
                className="
                    mt-1
                    accent-brand-600
                  "
              />

              <div
                className="
                  flex-1
                  min-w-0
                "
              >
                <div
                  className="
                    flex
                    flex-wrap
                    items-center
                    gap-2
                  "
                >
                  <span
                    className="
                      text-[10px]
                      uppercase
                      tracking-wide
                      font-semibold
                      text-brand-700
                    "
                  >
                    {suggestion.section}
                  </span>

                  {suggestion.subsection && (
                    <span
                      className="
                        text-[10px]
                        text-gray-400
                      "
                    >
                      · {suggestion.subsection}
                    </span>
                  )}

                  <span
                    className="
                      ml-auto
                      text-[10px]
                      text-gray-400
                    "
                  >
                    {Math.round(suggestion.confidence * 100)}% confidence
                  </span>
                </div>

                <div className="mt-3">{renderSuggestedContent(suggestion)}</div>

                {suggestion.reason && (
                  <div
                    className="
                      mt-3
                      pt-3
                      border-t
                      border-gray-100
                    "
                  >
                    <div
                      className="
                        text-[10px]
                        uppercase
                        tracking-wide
                        text-gray-400
                        mb-1
                      "
                    >
                      Why
                    </div>

                    <p
                      className="
                        text-xs
                        text-gray-500
                        leading-5
                      "
                    >
                      {suggestion.reason}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </label>
        ))}

        {pending.length === 0 && (
          <div
            className="
            bg-white
            border
            border-gray-200
            rounded-xl
            p-8
            text-center
            text-sm
            text-gray-400
          "
          >
            No pending suggestions left.
          </div>
        )}
      </div>
    </div>
  );
}
