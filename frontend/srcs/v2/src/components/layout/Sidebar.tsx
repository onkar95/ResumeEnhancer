import { NavLink, useLocation } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

interface Props {
  onNavigate?: () => void;
}

function getRunId(pathname: string): string | null {
  const match = pathname.match(/^\/review\/([^/]+)/);
  return match?.[1] || null;
}

function itemClass(isActive: boolean, compact = false) {
  return `block rounded-lg px-3 ${compact ? "py-2 text-xs" : "py-2.5 text-sm"} font-medium transition ${
    isActive
      ? "bg-brand-50 text-brand-700"
      : "text-gray-600 hover:bg-gray-50 hover:text-gray-950"
  }`;
}

export default function Sidebar({ onNavigate }: Props) {
  const { user, logout } = useAuth();
  const location = useLocation();
  const runId = getRunId(location.pathname);
  const inReview = Boolean(runId);
  const inAssistant = location.pathname.includes("/assistant");
  const assistantChat = location.pathname.endsWith("/chat");

  return (
    <aside className="flex h-full w-64 flex-col border-r border-gray-200 bg-white px-3 py-4">
      <div className="mb-8 flex items-center gap-2 px-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600 text-xs font-bold text-white">
          RE
        </div>
        <span className="font-bold text-gray-950">Resume Enhancer</span>
      </div>

      <div className="px-2 pb-2 text-[10px] font-bold uppercase tracking-widest text-gray-400">
        Workspace
      </div>
      <nav className="space-y-1">
        <NavLink to="/" end onClick={onNavigate} className={({ isActive }) => itemClass(isActive)}>
          Dashboard
        </NavLink>
        <NavLink to="/generate" onClick={onNavigate} className={({ isActive }) => itemClass(isActive)}>
          + New resume
        </NavLink>
        <NavLink to="/history" onClick={onNavigate} className={({ isActive }) => itemClass(isActive)}>
          History
        </NavLink>
        <NavLink to="/versions" onClick={onNavigate} className={({ isActive }) => itemClass(isActive)}>
          Resume versions
        </NavLink>
      </nav>

      {inReview && runId && (
        <>
          <div className="mt-7 px-2 pb-2 text-[10px] font-bold uppercase tracking-widest text-gray-400">
            Current draft
          </div>
          <nav className="space-y-1">
            <NavLink
              to={`/review/${runId}`}
              end
              onClick={onNavigate}
              className={({ isActive }) => itemClass(isActive)}
            >
              Review & Compare
            </NavLink>

            <div className="mt-2 px-3 pt-2 text-[10px] font-bold uppercase tracking-widest text-gray-400">
              AI Assistant
            </div>
            <NavLink
              to={`/review/${runId}/assistant/suggestions`}
              onClick={onNavigate}
              className={() => itemClass(inAssistant && !assistantChat, true)}
            >
              Suggestions
            </NavLink>
            <NavLink
              to={`/review/${runId}/assistant/chat`}
              onClick={onNavigate}
              className={() => itemClass(inAssistant && assistantChat, true)}
            >
              Chat & Resume
            </NavLink>
          </nav>
        </>
      )}

      <div className="mt-auto border-t border-gray-100 pt-4">
        {user && (
          <>
            <div className="truncate px-2 text-xs font-medium text-gray-900">{user.email}</div>
            <div className="px-2 pt-1 text-[11px] text-gray-400">
              {user.remaining_quota} generations left today
            </div>
            <button
              onClick={logout}
              className="mt-3 w-full rounded-lg px-3 py-2 text-left text-xs font-medium text-red-500 hover:bg-red-50"
            >
              Log out
            </button>
          </>
        )}
      </div>
    </aside>
  );
}
