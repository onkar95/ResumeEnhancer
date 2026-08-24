// import { useEffect, useState } from "react";
// import { useNavigate, useParams } from "react-router-dom";

// import { fetchRun } from "../services/api";

// import LoadingScreen from "../components/layout/LoadingScreen";
// import ChatThread from "../components/assistant/ChatThread";
// import SuggestionsList from "../components/assistant/SuggestionsList";
// import ResumePreviewMini from "../components/assistant/ResumePreviewMini";

// export default function AssistantPage() {
//   const { runId } = useParams();
//   const navigate = useNavigate();

//   const [run, setRun] = useState<any>(null);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     if (!runId) return;

//     load();
//   }, [runId]);

//   async function load() {
//     if (!runId) return;

//     setLoading(true);

//     try {
//       const data = await fetchRun(runId);
//       setRun(data);
//     } finally {
//       setLoading(false);
//     }
//   }

//   if (loading) {
//     return <LoadingScreen />;
//   }

//   if (!run) {
//     return null;
//   }

//   return (
//     <div className="w-full h-screen min-w-0 flex flex-col overflow-hidden bg-white">

//       {/* Header */}
//       <header className="flex-shrink-0 flex items-center justify-between px-4 sm:px-6 py-4 border-b border-gray-200 bg-white">
//         <button
//           onClick={() => navigate(`/review/${runId}`)}
//           className="text-sm text-gray-500 hover:text-brand-700 transition-colors"
//         >
//           ← Back to Resume
//         </button>

//         <h1 className="text-lg font-bold text-gray-900 truncate px-4">
//           AI Assistant — {run.tailored_resume?.name}
//         </h1>

//         <div className="w-24 flex-shrink-0" />
//       </header>

//       {/* Main */}
//       <main className="flex-1 min-h-0 min-w-0 grid grid-cols-1 lg:grid-cols-[320px_minmax(0,1fr)]">

//         {/* Resume preview */}
//         <aside className="hidden lg:block min-h-0 overflow-y-auto border-r border-gray-200 bg-gray-50">
//           <ResumePreviewMini
//             resume={run.tailored_resume}
//           />
//         </aside>

//         {/* Right side */}
//         <section className="min-w-0 min-h-0 flex flex-col overflow-hidden">

//           {/* Suggestions area */}
//           <div className="flex-shrink-0 max-h-[45%] overflow-y-auto border-b border-gray-200">
//             <SuggestionsList
//               runId={runId!}
//               suggestions={
//                 run.candidate_suggestions?.suggestions || []
//               }
//               onChanged={load}
//             />
//           </div>

//           {/* Chat area */}
//           <div className="flex-1 min-h-0 min-w-0 overflow-hidden">
//             <ChatThread
//               runId={runId!}
//               chatHistory={run.chat_history || []}
//               revisionCount={run.revision_count || 0}
//               onRevised={load}
//             />
//           </div>

//         </section>
//       </main>
//     </div>
//   );
// }

import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { fetchRun } from "../services/api";
import LoadingScreen from "../components/layout/LoadingScreen";
import SuggestionsList from "../components/assistant/SuggestionsList";
import ChatResumeThread from "../components/assistant/ChatThread";

type AssistantTab = "suggestions" | "chat";

export default function AssistantPage() {
  const { runId } = useParams();
  const navigate = useNavigate();

  const [run, setRun] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] =
    useState<AssistantTab>("suggestions");

  useEffect(() => {
    if (!runId) return;

    load();
  }, [runId]);

  async function load() {
    if (!runId) return;

    setLoading(true);

    try {
      const data = await fetchRun(runId);
      setRun(data);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <LoadingScreen />;
  }

  if (!run) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-sm text-gray-500">
          Resume run not found.
        </div>
      </div>
    );
  }

  const suggestions =
    run.candidate_suggestions?.suggestions || [];

  const pendingSuggestions = suggestions.filter(
    (s: any) => s.status === "pending"
  );

  const revisionCount = run.revision_count || 0;
  const maxRevisions = 5;

  return (
    <div className="h-screen w-full min-w-0 overflow-hidden bg-gray-50 flex flex-col">

      {/* =========================================================
          HEADER
      ========================================================= */}

      <header className="shrink-0 bg-white border-b border-gray-200">

        <div className="h-16 px-4 sm:px-6 flex items-center justify-between gap-4">

          {/* Back */}
          <button
            onClick={() => navigate(`/review/${runId}`)}
            className="
              flex items-center gap-2
              text-sm text-gray-500
              hover:text-gray-900
              transition
              shrink-0
            "
          >
            <span className="text-lg">←</span>

            <span className="hidden sm:inline">
              Back to Resume
            </span>
          </button>

          {/* Title */}
          <div className="min-w-0 text-center">

            <h1 className="text-base sm:text-lg font-bold text-gray-900 truncate">
              AI Resume Assistant
            </h1>

            {run.tailored_resume?.name && (
              <p className="hidden sm:block text-xs text-gray-500 truncate max-w-[300px]">
                {run.tailored_resume.name}
              </p>
            )}

          </div>

          {/* Draft status */}
          <div className="shrink-0">

            <span className="
              inline-flex
              items-center
              gap-1.5
              rounded-full
              bg-green-50
              border border-green-200
              px-2.5
              py-1
              text-xs
              font-medium
              text-green-700
            ">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500" />

              Draft v{Math.max(1, revisionCount + 1)}
            </span>

          </div>

        </div>

        {/* =======================================================
            TABS
        ======================================================= */}

        <nav className="grid grid-cols-2 border-t border-gray-100">

          <button
            onClick={() => setActiveTab("suggestions")}
            className={`
              relative
              h-12
              text-sm
              font-medium
              transition
              ${
                activeTab === "suggestions"
                  ? "text-brand-700"
                  : "text-gray-500 hover:text-gray-800"
              }
            `}
          >

            <span className="inline-flex items-center gap-2">

              Suggestions

              {pendingSuggestions.length > 0 && (
                <span className="
                  min-w-[20px]
                  h-5
                  px-1.5
                  rounded-full
                  bg-brand-100
                  text-brand-700
                  text-[11px]
                  font-bold
                  inline-flex
                  items-center
                  justify-center
                ">
                  {pendingSuggestions.length}
                </span>
              )}

            </span>

            {activeTab === "suggestions" && (
              <span className="
                absolute
                bottom-0
                left-0
                right-0
                h-0.5
                bg-brand-600"
              />
            )}

          </button>

          <button
            onClick={() => setActiveTab("chat")}
            className={`
              relative
              h-12
              text-sm
              font-medium
              transition
              ${
                activeTab === "chat"
                  ? "text-brand-700"
                  : "text-gray-500 hover:text-gray-800"
              }
            `}
          >

            <span className="inline-flex items-center gap-2">
              Chat & Resume
            </span>

            {activeTab === "chat" && (
              <span className="
                absolute
                bottom-0
                left-0
                right-0
                h-0.5
                bg-brand-600"
              />
            )}

          </button>

        </nav>

      </header>

      {/* =========================================================
          MAIN WORKSPACE
      ========================================================= */}

      <main className="flex-1 min-h-0 overflow-hidden">

        {activeTab === "suggestions" ? (

          <div className="h-full overflow-y-auto">

            <div className="
              w-full
              max-w-5xl
              mx-auto
              px-4
              sm:px-6
              lg:px-8
              py-6
              pb-12
            ">

              <SuggestionsList
                runId={runId!}
                suggestions={suggestions}
                onChanged={load}
              />

            </div>

          </div>

        ) : (

          <ChatResumeThread
            runId={runId!}
            chatHistory={run.chat_history || []}
            resume={run.tailored_resume}
            revisionCount={revisionCount}
            maxRevisions={maxRevisions}
            onRevised={load}
          />

        )}

      </main>

    </div>
  );
}