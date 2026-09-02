
import { useEffect, useState, type JSX } from "react";
import { editSection } from "../../services/api";
import HighlightText from "../resume/HighlightText";
import { useAuth } from "../../context/AuthContext";

interface Props {
  runId: string;
  path: string;
  value: string;
  originalValue?: string;
  onSaved: () => void;
  showChanges?: boolean;
  multiline?: boolean;
  className?: string;
  as?: "span" | "p" | "div";
  serialize?: (text: string) => unknown;
}

export default function InlineEditableText({
  runId,
  path,
  value,
  showChanges = false,
  onSaved,
  multiline,
  originalValue,
  className,
  as = "span",
  serialize,
}: Props) {
  const { user } = useAuth();
  console.log("originalValue", originalValue.length);
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(value);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setDraft(value);
  }, [value]);

  async function save() {
    setSaving(true);

    try {
      const payload = serialize ? serialize(draft) : draft;

      await editSection(runId, path, user.user_id, payload);

      onSaved();

      setEditing(false);
    } catch (err) {
      console.error(err);
      alert("Failed to save edit");
    } finally {
      setSaving(false);
    }
  }

  if (editing) {
    return (
      <span className="inline-flex flex-col gap-2 w-full">
        {multiline ? (
          <textarea
            className="border rounded p-2 w-full text-sm"
            rows={5}
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            autoFocus
          />
        ) : (
          <input
            className="border rounded p-2 w-full text-sm"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            autoFocus
          />
        )}

        <span className="flex gap-2">
          <button
            onClick={save}
            disabled={saving}
            className="text-xs bg-blue-600 text-white px-3 py-1 rounded disabled:opacity-50"
          >
            {saving ? "Saving..." : "Save"}
          </button>

          <button
            onClick={() => {
              setDraft(value);
              setEditing(false);
            }}
            className="text-xs bg-gray-200 px-3 py-1 rounded"
          >
            Cancel
          </button>
        </span>
      </span>
    );
  }

  const Tag = as as keyof JSX.IntrinsicElements;

  return (
    <Tag
      className={`${className ?? ""} cursor-pointer hover:bg-yellow-50 rounded group inline`}
      onClick={() => setEditing(true)}
      title="Click to edit"
    >
      {showChanges && originalValue !== undefined ? (
        <HighlightText
          diff={showChanges && originalValue !== undefined}
          original={originalValue}
          current={value}
        />
      ) : (
        value
      )}

      <span className="opacity-0 group-hover:opacity-100 text-xs text-blue-500 ml-1">
        ✎
      </span>
    </Tag>
  );
}
