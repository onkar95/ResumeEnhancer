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
            {s.suggested_content.bullet_points?.map(
              (b: string, i: number) => (
                <li key={i}>{b}</li>
              ),
            )}
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
            className="text-sm bg-green-600 text-white px-3 py-1.5 rounded disabled:opacity-50"
          >
            Approve Selected
          </button>
          <button
            onClick={handleReject}
            disabled={busy || selected.size === 0}
            className="text-sm bg-red-100 text-red-700 px-3 py-1.5 rounded disabled:opacity-50"
          >
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

// import { useMemo, useState } from "react";

// import { approveSuggestions, rejectSuggestions } from "../../services/api";

// interface Suggestion {
//   id: string;
//   title: string;
//   description?: string;
//   reason?: string;
//   section?: string;
//   status?: string;
// }

// interface Props {
//   runId: string;
//   suggestions: Suggestion[];
//   refresh: () => Promise<void>;
// }

// export default function SuggestionPanel({
//   runId,
//   suggestions,
//   refresh,
// }: Props) {
//   const [selected, setSelected] = useState<string[]>([]);
//   const [loading, setLoading] = useState(false);

//   const allSelected = useMemo(() => {
//     return suggestions.length > 0 && selected.length === suggestions.length;
//   }, [selected, suggestions]);

//   function toggle(id: string) {
//     if (selected.includes(id)) {
//       setSelected(selected.filter((x) => x !== id));
//     } else {
//       setSelected([...selected, id]);
//     }
//   }

//   function toggleAll() {
//     if (allSelected) {
//       setSelected([]);
//     } else {
//       setSelected(suggestions.map((s) => s.id));
//     }
//   }

//   async function approve() {
//     if (!selected.length) return;

//     try {
//       setLoading(true);

//       await approveSuggestions(runId, selected);

//       setSelected([]);

//       await refresh();
//     } catch (err) {
//       console.error(err);

//       alert("Unable to approve suggestions.");
//     } finally {
//       setLoading(false);
//     }
//   }

//   async function reject() {
//     if (!selected.length) return;

//     try {
//       setLoading(true);

//       await rejectSuggestions(runId, selected);

//       setSelected([]);

//       await refresh();
//     } catch (err) {
//       console.error(err);

//       alert("Unable to reject suggestions.");
//     } finally {
//       setLoading(false);
//     }
//   }

//   if (!suggestions.length) {
//     return (
//       <div className="bg-white rounded-xl shadow p-6 mb-8">
//         <h2 className="text-2xl font-bold mb-2">AI Suggestions</h2>

//         <p className="text-gray-500">No pending suggestions.</p>
//       </div>
//     );
//   }

//   return (
//     <div className="bg-white rounded-xl shadow p-6 mb-8">
//       <div className="flex justify-between items-center mb-5">
//         <h2 className="text-2xl font-bold">AI Suggestions</h2>

//         <div className="flex gap-2">
//           <button
//             onClick={approve}
//             disabled={loading}
//             className="
//               px-4
//               py-2
//               bg-green-600
//               text-white
//               rounded-lg
//             "
//           >
//             Approve
//           </button>

//           <button
//             onClick={reject}
//             disabled={loading}
//             className="
//               px-4
//               py-2
//               bg-red-600
//               text-white
//               rounded-lg
//             "
//           >
//             Reject
//           </button>
//         </div>
//       </div>

//       <table className="w-full">
//         <thead>
//           <tr className="border-b">
//             <th className="py-3">
//               <input
//                 type="checkbox"
//                 checked={allSelected}
//                 onChange={toggleAll}
//               />
//             </th>

//             <th className="text-left py-3">Suggestion</th>

//             <th className="text-left py-3">Section</th>

//             <th className="text-left py-3">Reason</th>
//           </tr>
//         </thead>

//         <tbody>
//           {suggestions.map((suggestion) => (
//             <tr key={suggestion.id} className="border-b">
//               <td className="py-4">
//                 <input
//                   type="checkbox"
//                   checked={selected.includes(suggestion.id)}
//                   onChange={() => toggle(suggestion.id)}
//                 />
//               </td>

//               <td className="py-4">
//                 <div className="font-semibold">{suggestion.title}</div>

//                 {suggestion.description && (
//                   <div className="text-sm text-gray-500 mt-1">
//                     {suggestion.description}
//                   </div>
//                 )}
//               </td>

//               <td>{suggestion.section}</td>

//               <td>{suggestion.reason}</td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   );
// }
