import { useState } from "react";
import { chatRevise } from "../services/api";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

interface Props {
  runId: string;
  chatHistory: ChatMessage[];
  revisionCount: number;
  maxRevisions?: number;
  onRevised: () => void;
}

export default function ChatPanel({
  runId,
  chatHistory,
  revisionCount,
  maxRevisions = 5,
  onRevised,
}: Props) {
  const [message, setMessage] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const remaining = Math.max(0, maxRevisions - revisionCount);
  const limitReached = remaining <= 0;

  async function handleSend() {
    const trimmed = message.trim();
    if (!trimmed || sending || limitReached) return;

    setSending(true);
    setError(null);

    try {
      await chatRevise(runId, trimmed);
      setMessage("");
      onRevised();
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to apply your message.");
    } finally {
      setSending(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="bg-white rounded-xl p-6 shadow space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold">Refine with Chat</h2>
        <span className="text-xs text-gray-500">
          {remaining} of {maxRevisions} revisions left
        </span>
      </div>

      <p className="text-xs text-gray-500">
        Tell the AI what to change — e.g. "I've also used Kafka on a side
        project, add it," or "be more aggressive matching the JD skills." Each
        message regenerates the resume using your current draft as the base.
      </p>

      <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
        {chatHistory.length === 0 && (
          <p className="text-sm text-gray-400">
            No messages yet. Send one to refine this draft.
          </p>
        )}

        {chatHistory.map((m, i) => (
          <div
            key={i}
            className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`
                max-w-[85%] rounded-lg px-3 py-2 text-sm
                ${
                  // AFTER
                  m.role === "user"
                    ? "bg-brand-600 text-white"
                    : "bg-gray-100 text-gray-700"
                }
              `}
            >
              {m.content}
            </div>
          </div>
        ))}
      </div>

      {error && <p className="text-xs text-red-600">{error}</p>}

      <div className="flex gap-2 items-end">
        <textarea
          className="flex-1 border rounded-lg p-2 text-sm resize-none disabled:bg-gray-100 disabled:text-gray-400"
          rows={2}
          placeholder={
            limitReached
              ? "Revision limit reached for this run."
              : "Type a message and press Enter to send..."
          }
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={sending || limitReached}
        />

        <button
          onClick={handleSend}
          disabled={sending || limitReached || !message.trim()}
          // AFTER
          className="text-sm bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 rounded-lg disabled:opacity-50 shrink-0 transition"
        >
          {sending ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}
