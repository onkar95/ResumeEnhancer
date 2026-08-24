import { useEffect, useRef, useState } from "react";
import { chatRevise } from "../../services/api";

interface ChatMessage { role: "user" | "assistant"; content: string; created_at: string; }
interface Props { runId: string; chatHistory: ChatMessage[]; resume: any; revisionCount: number; maxRevisions?: number; onRevised: () => void; }

function ResumeSnapshot({ resume }: { resume: any }) {
  return (
    <div className="rounded-2xl border border-brand-100 bg-brand-50/50 p-4">
      <div className="flex items-center justify-between gap-3 border-b border-brand-100 pb-3">
        <div><div className="text-[10px] font-bold uppercase tracking-wider text-brand-700">Updated resume</div><div className="mt-1 text-sm font-bold text-gray-900">{resume?.name || "Resume"}</div></div>
        <span className="rounded-full bg-white px-2 py-1 text-[10px] font-semibold text-brand-700">Live draft</span>
      </div>
      {resume?.professional_summary?.content && <div className="py-3 text-xs leading-5 text-gray-700"><div className="mb-1 font-bold uppercase tracking-wide text-gray-400">Summary</div>{resume.professional_summary.content}</div>}
      {resume?.technical_skills?.categories?.length > 0 && <div className="border-t border-brand-100 pt-3"><div className="mb-2 text-[10px] font-bold uppercase tracking-wide text-gray-400">Skills</div><div className="flex flex-wrap gap-1.5">{resume.technical_skills.categories.flatMap((c: any) => c.skills || []).slice(0, 16).map((s: string) => <span key={s} className="rounded-full bg-white px-2 py-1 text-[10px] text-gray-600 shadow-sm">{s}</span>)}</div></div>}
      {resume?.professional_experience?.length > 0 && (
        <div className="border-t border-brand-100 pt-3 mt-3">
          <div className="mb-3 text-[10px] font-bold uppercase tracking-wide text-gray-400">Professional Experience</div>
          {resume.professional_experience.slice(0, 2).map((exp: any, i: number) => (
            <div key={i} className={i > 0 ? "mt-4 border-t border-brand-100 pt-3" : ""}>
              <div className="text-xs font-bold text-gray-900">{exp.role}</div>
              <div className="text-[11px] text-gray-500">{exp.company} · {exp.start_date} – {exp.end_date}</div>
              <ul className="mt-2 space-y-1 text-[11px] leading-4 text-gray-700">
                {(exp.responsibilities || []).slice(0, 3).map((b: string, j: number) => <li key={j}>• {b}</li>)}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function ChatResumeThread({ runId, chatHistory, resume, revisionCount, maxRevisions = 5, onRevised }: Props) {
  const [message, setMessage] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const remaining = Math.max(0, maxRevisions - revisionCount);
  const limitReached = remaining === 0;

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [chatHistory.length, sending]);

  async function send() {
    const text = message.trim();
    if (!text || sending || limitReached) return;
    setSending(true); setError(null);
    try { await chatRevise(runId, text); setMessage(""); await onRevised(); }
    catch (err: any) { setError(err?.response?.data?.detail || "The assistant could not update this draft."); }
    finally { setSending(false); }
  }

  return (
    <div className="grid h-full min-h-0 grid-cols-1 lg:grid-cols-[minmax(0,1fr)_420px]">
      <section className="flex min-h-0 flex-col border-r border-gray-200 bg-white">
        <div className="shrink-0 border-b border-gray-100 px-4 py-3 sm:px-6">
          <div className="flex items-center justify-between gap-3"><div><h2 className="font-bold text-gray-950">Chat with AI</h2><p className="mt-0.5 text-xs text-gray-500">Ask for a specific resume change. The updated draft appears in context.</p></div><span className={`shrink-0 rounded-full px-2.5 py-1 text-[11px] font-semibold ${limitReached ? "bg-red-50 text-red-700" : "bg-gray-100 text-gray-600"}`}>{remaining} revisions left</span></div>
        </div>
        <div className="min-h-0 flex-1 overflow-y-auto bg-gray-50 px-4 py-5 sm:px-6">
          {chatHistory.length === 0 && <div className="mx-auto mt-10 max-w-lg text-center"><div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-50 text-brand-700">AI</div><h3 className="mt-4 font-semibold text-gray-900">What would you like to change?</h3><p className="mt-1 text-sm text-gray-500">Try: “Make my summary more focused on backend engineering.”</p></div>}
          <div className="mx-auto max-w-3xl space-y-5">
            {chatHistory.map((m, i) => <div key={`${m.created_at}-${i}`} className={m.role === "user" ? "flex justify-end" : "flex justify-start"}><div className="max-w-[88%] sm:max-w-[78%]"><div className="mb-1 flex items-center gap-2 text-[10px] font-semibold text-gray-400">{m.role === "assistant" ? "AI Assistant" : "You"}<span>{new Date(m.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span></div><div className={`rounded-2xl px-4 py-3 text-sm leading-6 shadow-sm ${m.role === "user" ? "rounded-tr-sm bg-brand-600 text-white" : "rounded-tl-sm border border-gray-200 bg-white text-gray-800"}`}>{m.content}</div>{m.role === "assistant" && <div className="mt-3"><ResumeSnapshot resume={resume} /></div>}</div></div>)}
            {sending && <div className="flex justify-start"><div className="rounded-2xl border border-gray-200 bg-white px-4 py-3 text-sm text-gray-400 shadow-sm animate-pulse">Updating your resume…</div></div>}
            <div ref={bottomRef} />
          </div>
        </div>
        <div className="shrink-0 border-t border-gray-200 bg-white p-3 sm:p-4">
          {error && <div className="mb-2 rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700">{error}</div>}
          <div className="mx-auto flex max-w-3xl items-end gap-2 rounded-2xl border border-gray-300 bg-white p-2 shadow-sm focus-within:border-brand-400 focus-within:ring-2 focus-within:ring-brand-50">
            <textarea value={message} onChange={(e) => setMessage(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }} disabled={sending || limitReached} rows={2} className="min-w-0 flex-1 resize-none border-0 bg-transparent px-2 py-1.5 text-sm outline-none placeholder:text-gray-400" placeholder={limitReached ? "Revision limit reached" : "Ask AI to change your resume…"} />
            <button onClick={send} disabled={!message.trim() || sending || limitReached} className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-600 text-white transition hover:bg-brand-700 disabled:opacity-40">↑</button>
          </div>
          <div className="mt-1 text-center text-[10px] text-gray-400">Enter to send · Shift + Enter for a new line</div>
        </div>
      </section>
      <aside className="hidden min-h-0 overflow-y-auto bg-gray-50 p-5 lg:block"><div className="sticky top-0"><div className="mb-3 flex items-center justify-between"><div><div className="text-xs font-semibold uppercase tracking-wider text-gray-400">Live preview</div><div className="mt-1 font-bold text-gray-900">Current resume</div></div><span className="rounded-full bg-brand-50 px-2 py-1 text-[10px] font-semibold text-brand-700">Draft</span></div><ResumeSnapshot resume={resume} /></div></aside>
    </div>
  );
}
