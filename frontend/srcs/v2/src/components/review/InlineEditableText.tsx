// import { useState, type JSX } from "react";

// import { editSection } from "../../services/api";

// interface Props {
//   runId: string;
//   path: string;
//   value: string;
//   onSaved: () => void;
//   multiline?: boolean;
//   className?: string;
//   as?: "span" | "p" | "div";
//   /** Transform the raw text draft before sending to the backend, e.g.
//    * turning a comma-separated skills string back into a string[]. */
//   serialize?: (text: string) => unknown;
// }

// export default function InlineEditableText({
//   runId,
//   path,
//   value,
//   onSaved,
//   multiline,
//   className,
//   as = "span",
//   serialize,
// }: Props) {
//   const [editing, setEditing] = useState(false);
//   const [draft, setDraft] = useState(value);
//   const [saving, setSaving] = useState(false);

//   async function save() {
//     setSaving(true);
//     try {
//       const payload = serialize ? serialize(draft) : draft;
//       await editSection(runId, path, payload);
//       onSaved();
//       setEditing(false);
//     } catch (err) {
//       console.error(err);
//       alert("Failed to save edit");
//     } finally {
//       setSaving(false);
//     }
//   }

//   if (editing) {
//     return (
//       <span className="inline-flex flex-col gap-1 w-full">
//         {multiline ? (
//           <textarea
//             className="border rounded p-2 w-full text-sm"
//             rows={4}
//             value={draft}
//             onChange={(e) => setDraft(e.target.value)}
//             autoFocus
//           />
//         ) : (
//           <input
//             className="border rounded p-1 w-full text-sm"
//             value={draft}
//             onChange={(e) => setDraft(e.target.value)}
//             autoFocus
//           />
//         )}
//         <span className="flex gap-2">
//           <button
//             onClick={save}
//             disabled={saving}
//             className="text-xs bg-blue-600 text-white px-2 py-1 rounded disabled:opacity-50"
//           >
//             {saving ? "Saving..." : "Save"}
//           </button>
//           <button
//             onClick={() => {
//               setDraft(value);
//               setEditing(false);
//             }}
//             className="text-xs bg-gray-200 px-2 py-1 rounded"
//           >
//             Cancel
//           </button>
//         </span>
//       </span>
//     );
//   }

//   const Tag = as as keyof JSX.IntrinsicElements;

//   return (
//     <Tag
//       className={`${className || ""} cursor-pointer hover:bg-yellow-50 rounded group inline`}
//       onClick={() => setEditing(true)}
//       title="Click to edit"
//     >
//       {value}
//       <span className="opacity-0 group-hover:opacity-100 text-xs text-blue-500 ml-1">
//         ✎
//       </span>
//     </Tag>
//   );
// }

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
  multiline?: boolean;
  className?: string;
  as?: "span" | "p" | "div";
  serialize?: (text: string) => unknown;
}

export default function InlineEditableText({
  runId,
  path,
  value,
  onSaved,
  multiline,
  className,
  as = "span",
  serialize,
}: Props) {

   const { user } = useAuth();

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

      await editSection(runId, path,user.user_id, payload);

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
      <HighlightText
        diff={originalValue !== undefined}
        original={originalValue ?? ""}
        current={value}
      />

      <span className="opacity-0 group-hover:opacity-100 text-xs text-blue-500 ml-1">
        ✎
      </span>
    </Tag>
  );
}