import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { runWorkflow } from "../services/api";
import LoadingScreen from "../components/layout/LoadingScreen";

export default function GeneratePage() {
  const navigate = useNavigate();
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jdText, setJdText] = useState("");
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit() {
    if (!resumeFile) return alert("Please upload your resume PDF.");
    if (!jdText.trim()) return alert("Please paste the job description.");
    try {
      setLoading(true);
      const result = await runWorkflow(resumeFile, jdText, notes);
      if (result?.run_id) navigate(`/review/${result.run_id}`);
    } catch (error) {
      console.error(error);
      alert("Resume generation failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-full bg-gray-50">
      {loading && <LoadingScreen />}
      <div className="mx-auto max-w-5xl px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
        <button onClick={() => navigate("/")} className="mb-5 text-sm text-gray-500 hover:text-brand-700">← Dashboard</button>
        <div className="max-w-2xl">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-brand-700">New draft</p>
          <h1 className="mt-1 text-3xl font-bold tracking-tight text-gray-950">Tailor your resume</h1>
          <p className="mt-2 text-sm leading-6 text-gray-500">Upload your current resume, add the target job description, and let the AI create a focused first draft.</p>
        </div>

        <div className="mt-7 grid gap-6 lg:grid-cols-[minmax(0,1fr)_280px]">
          <div className="card p-5 sm:p-7">
            <div>
              <label className="text-sm font-semibold text-gray-900">1. Upload resume</label>
              <label className="mt-3 flex min-h-36 cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-gray-300 bg-gray-50 px-5 text-center transition hover:border-brand-400 hover:bg-brand-50/40">
                <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-white text-lg shadow-sm">↑</span>
                <span className="mt-3 text-sm font-semibold text-gray-800">{resumeFile ? resumeFile.name : "Choose a PDF resume"}</span>
                <span className="mt-1 text-xs text-gray-500">Drag & drop or browse from your computer</span>
                <input type="file" accept=".pdf" className="hidden" onChange={(e) => setResumeFile(e.target.files?.[0] || null)} />
              </label>
            </div>

            <div className="mt-7">
              <label className="text-sm font-semibold text-gray-900">2. Job description</label>
              <textarea value={jdText} onChange={(e) => setJdText(e.target.value)} className="mt-3 h-72 w-full resize-y rounded-xl border border-gray-300 bg-white p-4 text-sm leading-6 outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100" placeholder="Paste the full job description here..." />
              <div className="mt-1 text-right text-[11px] text-gray-400">{jdText.length} characters</div>
            </div>

            <div className="mt-6">
              <label className="text-sm font-semibold text-gray-900">3. Additional notes <span className="font-normal text-gray-400">(optional)</span></label>
              <textarea value={notes} onChange={(e) => setNotes(e.target.value)} className="mt-3 h-28 w-full resize-y rounded-xl border border-gray-300 p-4 text-sm leading-6 outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100" placeholder="Mention skills, experience or preferences you want the AI to consider..." />
            </div>

            <div className="mt-7 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
              <button onClick={() => navigate("/")} className="btn-secondary">Cancel</button>
              <button onClick={submit} disabled={loading} className="btn-primary">{loading ? "Generating…" : "Generate tailored resume"}</button>
            </div>
          </div>

          <aside className="space-y-4">
            <div className="card p-5">
              <h2 className="font-semibold text-gray-900">What happens next?</h2>
              <div className="mt-4 space-y-4 text-sm">
                <p><b>01.</b> AI parses your resume.</p>
                <p><b>02.</b> The job description is analyzed for relevant requirements.</p>
                <p><b>03.</b> A tailored draft and improvement suggestions are generated.</p>
                <p><b>04.</b> You review, edit and export the final version.</p>
              </div>
            </div>
            <div className="rounded-2xl border border-brand-100 bg-brand-50 p-5 text-sm text-brand-900">
              <div className="font-semibold">Keep control</div>
              <p className="mt-1 leading-6 text-brand-800">The assistant works from your existing resume and verified information. Review every AI change before exporting.</p>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
