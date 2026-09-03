import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchRunHistory } from "../services/api";
import LoadingScreen from "../components/layout/LoadingScreen";
import { useQuery } from "@tanstack/react-query";

export default function DashboardPage() {
  const navigate = useNavigate();

  const { data: history = [], isLoading } = useQuery({
    queryKey: ["runHistory"],
    queryFn: fetchRunHistory,
  });


  const stats = useMemo(() => {
    const finalized = history.filter((r) => r.finalized).length;
    const improvements = history
      .filter((r) => r.ats_before != null && r.ats_after != null)
      .map((r) => Number(r.ats_after) - Number(r.ats_before));
    const avg = improvements.length
      ? Math.round(
          improvements.reduce((a, b) => a + b, 0) / improvements.length,
        )
      : 0;
    return { total: history.length, finalized, avg };
  }, [history]);

  if (isLoading) return <LoadingScreen message="Loading dashboard..." />;

  return (
    <div className="min-h-full bg-gray-50">
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-brand-700">
              Workspace
            </p>
            <h1 className="mt-1 text-3xl font-bold tracking-tight text-gray-950">
              Dashboard
            </h1>
            <p className="mt-2 max-w-2xl text-sm text-gray-500">
              Create, tailor, review and export job-ready resumes from one
              workspace.
            </p>
          </div>
          <button
            onClick={() => navigate("/generate")}
            className="btn-primary self-start sm:self-auto"
          >
            + New resume
          </button>
        </div>

        <div className="mt-7 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {[
            ["Total drafts", stats.total, "All generated resumes"],
            ["Finalized", stats.finalized, "Ready to use"],
            ["Avg. ATS improvement", `+${stats.avg}`, "Across scored drafts"],
            [
              "Recent activity",
              history.length ? "Active" : "Start",
              history.length
                ? "Your workspace is ready"
                : "Create your first draft",
            ],
          ].map(([label, value, helper]) => (
            <div key={String(label)} className="card p-5">
              <div className="text-xs font-medium text-gray-500">{label}</div>
              <div className="mt-2 text-3xl font-bold text-gray-950">
                {value}
              </div>
              <div className="mt-1 text-xs text-gray-400">{helper}</div>
            </div>
          ))}
        </div>

        <div className="mt-7 grid gap-6 xl:grid-cols-[minmax(0,1fr)_360px]">
          <section className="card overflow-hidden">
            <div className="flex items-center justify-between border-b border-gray-100 px-5 py-4">
              <div>
                <h2 className="font-bold text-gray-950">Recent drafts</h2>
                <p className="mt-0.5 text-xs text-gray-500">
                  Pick up where you left off.
                </p>
              </div>
              <button
                onClick={() => navigate("/history")}
                className="text-xs font-semibold text-brand-700 hover:text-brand-800"
              >
                View all
              </button>
            </div>
            {history.length === 0 ? (
              <div className="px-5 py-14 text-center">
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-50 text-xl">
                  📄
                </div>
                <h3 className="mt-4 font-semibold text-gray-900">
                  No drafts yet
                </h3>
                <p className="mx-auto mt-1 max-w-sm text-sm text-gray-500">
                  Upload your current resume and a job description to create
                  your first tailored version.
                </p>
                <button
                  onClick={() => navigate("/generate")}
                  className="btn-primary mt-5"
                >
                  Create a resume
                </button>
              </div>
            ) : (
              <div className="divide-y divide-gray-100">
                {history.slice(0, 6).map((item) => (
                  <button
                    key={item.run_id}
                    onClick={() => navigate(`/review/${item.run_id}`)}
                    className="flex w-full items-center gap-4 px-5 py-4 text-left transition hover:bg-gray-50"
                  >
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-700">
                      ▣
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="truncate text-sm font-semibold text-gray-900">
                        {item.job_title || "Untitled role"}
                      </div>
                      <div className="mt-1 truncate text-xs text-gray-500">
                        {item.resume_name || "Resume"}
                        {item.company ? ` · ${item.company}` : ""}
                      </div>
                      <div className="mt-1 text-[11px] text-gray-400">
                        {new Date(item.created_at).toLocaleString()}
                      </div>
                    </div>
                    <div className="hidden text-right sm:block">
                      <div className="text-xs font-semibold text-gray-700">
                        ATS {item.ats_after ?? "—"}
                      </div>
                      <span
                        className={`mt-1 inline-flex rounded-full px-2 py-0.5 text-[10px] font-semibold ${item.finalized ? "bg-brand-50 text-brand-700" : "bg-gray-100 text-gray-500"}`}
                      >
                        {item.finalized ? "Finalized" : "Draft"}
                      </span>
                    </div>
                    <span className="text-gray-300">›</span>
                  </button>
                ))}
              </div>
            )}
          </section>

          <section className="card p-5">
            <h2 className="font-bold text-gray-950">
              Create a better application
            </h2>
            <p className="mt-1 text-sm leading-6 text-gray-500">
              Use the workflow in three simple steps.
            </p>
            <div className="mt-5 space-y-4">
              {[
                ["01", "Upload your resume", "Start from your existing PDF."],
                ["02", "Add the target role", "Paste the job description."],
                [
                  "03",
                  "Review with AI",
                  "Approve suggestions or chat with the assistant.",
                ],
              ].map(([n, title, copy]) => (
                <div key={n} className="flex gap-3">
                  <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-brand-50 text-xs font-bold text-brand-700">
                    {n}
                  </span>
                  <div>
                    <div className="text-sm font-semibold text-gray-900">
                      {title}
                    </div>
                    <div className="mt-0.5 text-xs leading-5 text-gray-500">
                      {copy}
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <button
              onClick={() => navigate("/generate")}
              className="btn-secondary mt-6 w-full"
            >
              Start a new draft
            </button>
          </section>
        </div>
      </div>
    </div>
  );
}
