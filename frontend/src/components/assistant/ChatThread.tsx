// import { useState, useRef, useEffect } from "react";
// import { chatRevise } from "../../services/api";

// interface ChatMessage {
//   role: "user" | "assistant";
//   content: string;
//   created_at: string;
// }

// interface Props {
//   runId: string;
//   chatHistory: ChatMessage[];
//   revisionCount: number;
//   maxRevisions?: number;
//   onRevised: () => void;
// }

// export default function ChatThread({
//   runId,
//   chatHistory,
//   revisionCount,
//   maxRevisions = 5,
//   onRevised,
// }: Props) {
//   const [message, setMessage] = useState("");
//   const [sending, setSending] = useState(false);
//   const [error, setError] = useState<string | null>(null);

//   const bottomRef = useRef<HTMLDivElement>(null);

//   const remaining = Math.max(
//     0,
//     maxRevisions - revisionCount
//   );

//   const limitReached = remaining <= 0;

//   useEffect(() => {
//     bottomRef.current?.scrollIntoView({
//       behavior: "smooth",
//     });
//   }, [chatHistory.length]);

//   async function handleSend() {
//     const trimmed = message.trim();

//     if (!trimmed || sending || limitReached) {
//       return;
//     }

//     setSending(true);
//     setError(null);

//     try {
//       await chatRevise(runId, trimmed);

//       setMessage("");

//       onRevised();
//     } catch (err: any) {
//       setError(
//         err?.response?.data?.detail ||
//           "Failed to apply your message."
//       );
//     } finally {
//       setSending(false);
//     }
//   }

//   function handleKeyDown(
//     e: React.KeyboardEvent<HTMLTextAreaElement>
//   ) {
//     if (e.key === "Enter" && !e.shiftKey) {
//       e.preventDefault();
//       handleSend();
//     }
//   }

//   return (
//     <div className="h-full min-h-0 w-full flex flex-col bg-white">

//       {/* Chat header */}
//       <div className="flex-shrink-0 px-4 sm:px-6 py-3 border-b border-gray-100 bg-white flex items-center justify-between">

//         <div className="min-w-0">
//           <h2 className="font-bold text-gray-900">
//             Chat with AI
//           </h2>

//           <p className="text-xs text-gray-500 mt-0.5 truncate">
//             Describe a change and the AI regenerates your resume using this
//             draft as the base.
//           </p>
//         </div>

//         <span
//           className={`flex-shrink-0 text-xs px-2 py-1 rounded-full ml-3 ${
//             limitReached
//               ? "bg-red-100 text-red-700"
//               : "bg-gray-100 text-gray-600"
//           }`}
//         >
//           {remaining} of {maxRevisions} left
//         </span>
//       </div>

//       {/* Messages */}
//       <div className="flex-1 min-h-0 overflow-y-auto px-4 sm:px-6 py-4 space-y-4 bg-gray-50">

//         {chatHistory.length === 0 && (
//           <div className="text-center text-sm text-gray-400 mt-10">
//             <p>
//               No messages yet. Try something like:
//             </p>

//             <p className="mt-2 text-gray-500 italic">
//               "I've also used Kafka on a side project, add it"
//             </p>
//           </div>
//         )}

//         {chatHistory.map((m, i) => (
//           <div
//             key={i}
//             className={`flex ${
//               m.role === "user"
//                 ? "justify-end"
//                 : "justify-start"
//             }`}
//           >
//             <div
//               className={`flex gap-2 max-w-[80%] ${
//                 m.role === "user"
//                   ? "flex-row-reverse"
//                   : ""
//               }`}
//             >

//               {/* Avatar */}
//               <div
//                 className={`w-7 h-7 shrink-0 rounded-full flex items-center justify-center text-xs font-bold ${
//                   m.role === "user"
//                     ? "bg-brand-600 text-white"
//                     : "bg-white border border-gray-300 text-gray-600"
//                 }`}
//               >
//                 {m.role === "user" ? "You" : "AI"}
//               </div>

//               {/* Message */}
//               <div
//                 className={`rounded-2xl px-4 py-2.5 text-sm shadow-sm ${
//                   m.role === "user"
//                     ? "bg-brand-600 text-white rounded-tr-sm"
//                     : "bg-white border border-gray-200 text-gray-800 rounded-tl-sm"
//                 }`}
//               >
//                 <div className="whitespace-pre-wrap break-words">
//                   {m.content}
//                 </div>

//                 <div
//                   className={`text-[10px] mt-1 ${
//                     m.role === "user"
//                       ? "text-brand-100"
//                       : "text-gray-400"
//                   }`}
//                 >
//                   {new Date(
//                     m.created_at
//                   ).toLocaleTimeString([], {
//                     hour: "2-digit",
//                     minute: "2-digit",
//                   })}
//                 </div>
//               </div>
//             </div>
//           </div>
//         ))}

//         {sending && (
//           <div className="flex justify-start">
//             <div className="flex gap-2 max-w-[80%]">

//               <div className="w-7 h-7 shrink-0 rounded-full bg-white border border-gray-300 flex items-center justify-center text-xs font-bold text-gray-600">
//                 AI
//               </div>

//               <div className="rounded-2xl rounded-tl-sm px-4 py-2.5 text-sm bg-white border border-gray-200 text-gray-400 animate-pulse">
//                 Regenerating your resume…
//               </div>

//             </div>
//           </div>
//         )}

//         <div ref={bottomRef} />
//       </div>

//       {/* Error */}
//       {error && (
//         <div className="flex-shrink-0 px-4 sm:px-6 pt-2 bg-white">
//           <p className="text-xs text-red-600">
//             {error}
//           </p>
//         </div>
//       )}

//       {/* Input */}
//       <div className="flex-shrink-0 p-4 sm:p-6 border-t border-gray-100 bg-white flex gap-2 items-end">

//         <textarea
//           className="flex-1 min-w-0 border border-gray-300 rounded-lg p-2.5 text-sm resize-none disabled:bg-gray-100 disabled:text-gray-400 focus:outline-none focus:ring-2 focus:ring-brand-500"
//           rows={2}
//           placeholder={
//             limitReached
//               ? "Revision limit reached for this run."
//               : "Type a message and press Enter to send…"
//           }
//           value={message}
//           onChange={(e) => setMessage(e.target.value)}
//           onKeyDown={handleKeyDown}
//           disabled={sending || limitReached}
//         />

//         <button
//           onClick={handleSend}
//           disabled={
//             sending ||
//             limitReached ||
//             !message.trim()
//           }
//           className="text-sm bg-brand-600 hover:bg-brand-700 text-white px-4 py-2.5 rounded-lg disabled:opacity-50 shrink-0 transition"
//         >
//           {sending ? "Sending…" : "Send"}
//         </button>

//       </div>
//     </div>
//   );
// }

import { useEffect, useRef, useState } from "react";
import { chatRevise } from "../../services/api";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  created_at: string;

  // Optional fields for richer assistant responses
  changes?: ResumeChange[];
  resume?: any;
}

interface ResumeChange {
  section?: string;
  subsection?: string;
  type?: string;
  title?: string;
  before?: string;
  after?: string;
  content?: string;
}

interface Props {
  runId: string;
  chatHistory: ChatMessage[];
  resume: any;
  revisionCount: number;
  maxRevisions?: number;
  onRevised: () => void;
}

export default function ChatResumeThread({
  runId,
  chatHistory,
  resume,
  revisionCount,
  maxRevisions = 5,
  onRevised,
}: Props) {
  const [message, setMessage] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const remaining = Math.max(
    0,
    maxRevisions - revisionCount
  );

  const limitReached = remaining <= 0;

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [chatHistory.length, sending]);

  async function handleSend() {
    const trimmed = message.trim();

    if (
      !trimmed ||
      sending ||
      limitReached
    ) {
      return;
    }

    setSending(true);
    setError(null);

    try {
      await chatRevise(
        runId,
        trimmed
      );

      setMessage("");

      onRevised();

      requestAnimationFrame(() => {
        textareaRef.current?.focus();
      });

    } catch (err: any) {

      setError(
        err?.response?.data?.detail ||
        "Failed to apply your message."
      );

    } finally {
      setSending(false);
    }
  }

  function handleKeyDown(
    e: React.KeyboardEvent<HTMLTextAreaElement>
  ) {
    if (
      e.key === "Enter" &&
      !e.shiftKey
    ) {
      e.preventDefault();

      handleSend();
    }
  }

  function formatTime(
    createdAt: string
  ) {
    if (!createdAt) {
      return "";
    }

    return new Date(
      createdAt
    ).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  return (
    <div className="
      h-full
      min-h-0
      flex
      flex-col
      bg-gray-50
    ">

      {/* ========================================================
          CHAT HEADER
      ======================================================== */}

      <div className="
        shrink-0
        bg-white
        border-b
        border-gray-200
        px-4
        sm:px-6
        py-3
      ">

        <div className="
          max-w-4xl
          mx-auto
          flex
          items-center
          justify-between
          gap-4
        ">

          <div className="min-w-0">

            <h2 className="
              text-sm
              sm:text-base
              font-bold
              text-gray-900
            ">
              Chat with AI
            </h2>

            <p className="
              text-xs
              text-gray-500
              mt-0.5
              hidden
              sm:block
            ">
              Ask the AI to improve or change your resume.
            </p>

          </div>

          <div className="
            shrink-0
            text-xs
            font-medium
            px-2.5
            py-1
            rounded-full
            bg-gray-100
            text-gray-600
          ">
            {remaining} revision
            {remaining !== 1 ? "s" : ""} left
          </div>

        </div>

      </div>

      {/* ========================================================
          MESSAGES
      ======================================================== */}

      <div className="
        flex-1
        min-h-0
        overflow-y-auto
        px-4
        sm:px-6
        py-6
      ">

        <div className="
          max-w-4xl
          mx-auto
          space-y-6
        ">

          {/* Empty state */}

          {chatHistory.length === 0 && (
            <div className="
              flex
              flex-col
              items-center
              justify-center
              text-center
              py-16
              px-6
            ">

              <div className="
                w-14
                h-14
                rounded-2xl
                bg-brand-50
                border
                border-brand-100
                flex
                items-center
                justify-center
                text-2xl
                mb-4
              ">
                ✨
              </div>

              <h3 className="
                font-semibold
                text-gray-900
              ">
                What would you like to change?
              </h3>

              <p className="
                text-sm
                text-gray-500
                mt-1
                max-w-md
              ">
                Ask the AI to rewrite, add, remove,
                or improve something in your resume.
              </p>

              <div className="
                grid
                grid-cols-1
                sm:grid-cols-2
                gap-2
                mt-6
                w-full
                max-w-lg
              ">

                <SuggestionPrompt
                  text="Improve my professional summary"
                  onClick={() =>
                    setMessage(
                      "Improve my professional summary"
                    )
                  }
                />

                <SuggestionPrompt
                  text="Make my experience more ATS friendly"
                  onClick={() =>
                    setMessage(
                      "Make my experience more ATS friendly"
                    )
                  }
                />

                <SuggestionPrompt
                  text="Highlight my AI experience"
                  onClick={() =>
                    setMessage(
                      "Highlight my AI experience"
                    )
                  }
                />

                <SuggestionPrompt
                  text="Make my resume more concise"
                  onClick={() =>
                    setMessage(
                      "Make my resume more concise"
                    )
                  }
                />

              </div>

            </div>
          )}

          {/* Conversation */}

          {chatHistory.map(
            (m, index) => (
              <Message
                key={`${m.created_at}-${index}`}
                message={m}
              />
            )
          )}

          {/* Loading */}

          {sending && (
            <div className="
              flex
              justify-start
            ">

              <div className="
                max-w-[90%]
                sm:max-w-[75%]
              ">

                <div className="
                  flex
                  items-center
                  gap-2
                  mb-1.5
                ">

                  <Avatar role="assistant" />

                  <span className="
                    text-xs
                    font-medium
                    text-gray-500
                  ">
                    AI Assistant
                  </span>

                </div>

                <div className="
                  bg-white
                  border
                  border-gray-200
                  rounded-2xl
                  rounded-tl-sm
                  px-4
                  py-3
                  text-sm
                  text-gray-500
                  shadow-sm
                ">

                  <div className="
                    flex
                    items-center
                    gap-2
                  ">

                    <span className="
                      flex
                      gap-1
                    ">
                      <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" />
                      <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:100ms]" />
                      <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:200ms]" />
                    </span>

                    Regenerating your resume…

                  </div>

                </div>

              </div>

            </div>
          )}

          <div ref={bottomRef} />

        </div>

      </div>

      {/* ========================================================
          ERROR
      ======================================================== */}

      {error && (
        <div className="
          shrink-0
          px-4
          sm:px-6
          pb-2
          bg-white
        ">

          <div className="
            max-w-4xl
            mx-auto
            rounded-lg
            bg-red-50
            border
            border-red-200
            px-3
            py-2
            text-xs
            text-red-700
          ">
            {error}
          </div>

        </div>
      )}

      {/* ========================================================
          COMPOSER
      ======================================================== */}

      <div className="
        shrink-0
        bg-white
        border-t
        border-gray-200
        px-4
        sm:px-6
        py-3
        sm:py-4
      ">

        <div className="
          max-w-4xl
          mx-auto
        ">

          <div className="
            flex
            items-end
            gap-2
            rounded-xl
            border
            border-gray-300
            bg-white
            p-2
            shadow-sm
            focus-within:border-brand-500
            focus-within:ring-2
            focus-within:ring-brand-100
            transition
          ">

            <textarea
              ref={textareaRef}
              rows={1}
              value={message}
              onChange={(e) =>
                setMessage(e.target.value)
              }
              onKeyDown={handleKeyDown}
              disabled={
                sending ||
                limitReached
              }
              placeholder={
                limitReached
                  ? "Revision limit reached for this run."
                  : "Ask AI to change your resume…"
              }
              className="
                flex-1
                min-w-0
                max-h-32
                resize-none
                border-0
                outline-none
                bg-transparent
                px-2
                py-2
                text-sm
                text-gray-900
                placeholder:text-gray-400
                disabled:text-gray-400
              "
            />

            <button
              onClick={handleSend}
              disabled={
                sending ||
                limitReached ||
                !message.trim()
              }
              className="
                shrink-0
                w-9
                h-9
                rounded-lg
                bg-brand-600
                hover:bg-brand-700
                text-white
                flex
                items-center
                justify-center
                disabled:opacity-40
                disabled:cursor-not-allowed
                transition
              "
              aria-label="Send message"
            >

              {sending ? (
                <span className="
                  w-4
                  h-4
                  border-2
                  border-white
                  border-t-transparent
                  rounded-full
                  animate-spin"
                />
              ) : (
                <span className="text-lg">
                  
                </span>
              )}

            </button>

          </div>

          <p className="
            text-[10px]
            text-gray-400
            mt-1.5
            text-center
          ">
            Enter to send · Shift + Enter for a new line
          </p>

        </div>

      </div>

    </div>
  );
}


/* ================================================================
   MESSAGE
================================================================ */

function Message({
  message,
}: {
  message: ChatMessage;
}) {
  const isUser =
    message.role === "user";

  return (
    <div
      className={`
        flex
        ${isUser
          ? "justify-end"
          : "justify-start"
        }
      `}
    >

      <div className="
        max-w-[94%]
        sm:max-w-[80%]
      ">

        {/* Avatar + name */}

        <div
          className={`
            flex
            items-center
            gap-2
            mb-1.5
            ${isUser
              ? "justify-end"
              : "justify-start"
            }
          `}
        >

          {!isUser && (
            <Avatar role="assistant" />
          )}

          <span className="
            text-xs
            font-medium
            text-gray-500
          ">
            {isUser
              ? "You"
              : "AI Assistant"}
          </span>

          {isUser && (
            <Avatar role="user" />
          )}

        </div>

        {/* Message */}

        <div
          className={`
            rounded-2xl
            px-4
            py-3
            text-sm
            leading-6
            shadow-sm
            ${
              isUser
                ? `
                  bg-brand-600
                  text-white
                  rounded-tr-sm
                `
                : `
                  bg-white
                  border
                  border-gray-200
                  text-gray-800
                  rounded-tl-sm
                `
            }
          `}
        >

          <div className="whitespace-pre-wrap">
            {message.content}
          </div>

          {/* Resume changes */}

          {!isUser &&
            message.changes &&
            message.changes.length > 0 && (
              <ResumeChangeCard
                changes={message.changes}
              />
            )}

          {/* Optional generated resume */}

          {!isUser &&
            message.resume && (
              <ResumeSnapshot
                resume={message.resume}
              />
            )}

          <div
            className={`
              text-[10px]
              mt-2
              ${
                isUser
                  ? "text-brand-100"
                  : "text-gray-400"
              }
            `}
          >
            {formatMessageTime(
              message.created_at
            )}
          </div>

        </div>

      </div>

    </div>
  );
}


/* ================================================================
   RESUME CHANGE CARD
================================================================ */

function ResumeChangeCard({
  changes,
}: {
  changes: ResumeChange[];
}) {
  return (
    <div className="
      mt-4
      rounded-xl
      border
      border-brand-100
      bg-brand-50
      overflow-hidden
    ">

      <div className="
        px-4
        py-3
        border-b
        border-brand-100
        flex
        items-center
        gap-2
      ">

        <span>✨</span>

        <span className="
          font-semibold
          text-sm
          text-gray-900
        ">
          Resume updated
        </span>

      </div>

      <div className="p-4 space-y-4">

        {changes.map(
          (change, index) => (
            <div
              key={index}
              className="space-y-2"
            >

              <div className="
                flex
                items-center
                justify-between
                gap-2
              ">

                <span className="
                  text-xs
                  uppercase
                  tracking-wide
                  font-semibold
                  text-brand-700
                ">
                  {change.section ||
                    "Resume"}
                </span>

                {change.type && (
                  <span className="
                    text-[10px]
                    px-2
                    py-0.5
                    rounded-full
                    bg-white
                    border
                    border-brand-100
                    text-gray-500
                  ">
                    {change.type}
                  </span>
                )}

              </div>

              {change.title && (
                <div className="
                  text-sm
                  font-semibold
                  text-gray-900
                ">
                  {change.title}
                </div>
              )}

              {change.before && (
                <div>

                  <div className="
                    text-[10px]
                    uppercase
                    tracking-wide
                    text-gray-400
                    mb-1
                  ">
                    Before
                  </div>

                  <div className="
                    text-xs
                    text-gray-500
                    bg-white
                    border
                    border-gray-200
                    rounded-lg
                    p-2.5
                  ">
                    {change.before}
                  </div>

                </div>
              )}

              {change.after && (
                <div>

                  <div className="
                    text-[10px]
                    uppercase
                    tracking-wide
                    text-brand-600
                    mb-1
                  ">
                    Updated
                  </div>

                  <div className="
                    text-xs
                    text-gray-700
                    bg-white
                    border
                    border-brand-200
                    rounded-lg
                    p-2.5
                  ">
                    {change.after}
                  </div>

                </div>
              )}

              {change.content && (
                <div className="
                  text-xs
                  text-gray-700
                  bg-white
                  border
                  border-gray-200
                  rounded-lg
                  p-2.5
                ">
                  {change.content}
                </div>
              )}

            </div>
          )
        )}

      </div>

    </div>
  );
}


/* ================================================================
   RESUME SNAPSHOT
================================================================ */

function ResumeSnapshot({
  resume,
}: {
  resume: any;
}) {
  if (!resume) {
    return null;
  }

  const skills =
    resume.technical_skills?.categories
      ?.flatMap(
        (category: any) =>
          category.skills || []
      )
      ?.slice(0, 12) || [];

  const experience =
    resume.professional_experience
      ?.slice(0, 3) || [];

  return (
    <div className="
      mt-4
      rounded-xl
      border
      border-gray-200
      bg-white
      overflow-hidden
    ">

      <div className="
        px-4
        py-3
        bg-gray-50
        border-b
        border-gray-200
        flex
        items-center
        justify-between
      ">

        <div>
          <div className="
            text-xs
            uppercase
            tracking-wide
            text-gray-400
          ">
            Latest draft
          </div>

          <div className="
            text-sm
            font-bold
            text-gray-900
            mt-0.5
          ">
            {resume.name}
          </div>
        </div>

        <span className="text-lg">
          📄
        </span>

      </div>

      <div className="
        p-4
        space-y-4
      ">

        {resume.headline && (
          <div className="
            text-xs
            text-gray-600
          ">
            {resume.headline}
          </div>
        )}

        {skills.length > 0 && (
          <div>

            <div className="
              text-[10px]
              uppercase
              tracking-wide
              font-semibold
              text-gray-400
              mb-2
            ">
              Key skills
            </div>

            <div className="
              flex
              flex-wrap
              gap-1.5
            ">

              {skills.map(
                (skill: string) => (
                  <span
                    key={skill}
                    className="
                      text-[10px]
                      px-2
                      py-1
                      rounded-full
                      bg-gray-50
                      border
                      border-gray-200
                      text-gray-600
                    "
                  >
                    {skill}
                  </span>
                )
              )}

            </div>

          </div>
        )}

        {experience.length > 0 && (
          <div>

            <div className="
              text-[10px]
              uppercase
              tracking-wide
              font-semibold
              text-gray-400
              mb-2
            ">
              Experience
            </div>

            <div className="space-y-2">

              {experience.map(
                (exp: any, index: number) => (
                  <div
                    key={index}
                    className="
                      text-xs
                      border-l-2
                      border-gray-200
                      pl-3
                    "
                  >

                    <div className="
                      font-semibold
                      text-gray-800
                    ">
                      {exp.role}
                    </div>

                    <div className="
                      text-gray-500
                    ">
                      {exp.company}
                    </div>

                  </div>
                )
              )}

            </div>

          </div>
        )}

      </div>

    </div>
  );
}


/* ================================================================
   AVATAR
================================================================ */

function Avatar({
  role,
}: {
  role: "user" | "assistant";
}) {
  return (
    <div
      className={`
        w-6
        h-6
        shrink-0
        rounded-full
        flex
        items-center
        justify-center
        text-[9px]
        font-bold
        ${
          role === "user"
            ? "bg-brand-600 text-white"
            : "bg-white border border-gray-300 text-gray-600"
        }
      `}
    >
      {role === "user"
        ? "U"
        : "AI"}
    </div>
  );
}


/* ================================================================
   QUICK PROMPT
================================================================ */

function SuggestionPrompt({
  text,
  onClick,
}: {
  text: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="
        text-left
        text-xs
        text-gray-600
        bg-white
        border
        border-gray-200
        rounded-lg
        px-3
        py-2.5
        hover:border-brand-300
        hover:bg-brand-50
        hover:text-brand-700
        transition
      "
    >
      {text}
    </button>
  );
}


/* ================================================================
   TIME
================================================================ */

function formatMessageTime(
  createdAt: string
) {
  if (!createdAt) {
    return "";
  }

  return new Date(
    createdAt
  ).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}