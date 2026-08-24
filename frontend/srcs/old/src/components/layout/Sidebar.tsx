import { NavLink } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const base = "block px-4 py-2.5 rounded-lg text-sm font-medium transition";
const active = "bg-brand-600 text-white";
const inactive = "text-gray-600 hover:bg-brand-50 hover:text-brand-700";

interface Props {
  onNavigate?: () => void;
}

export default function Sidebar({ onNavigate }: Props) {
   const { user, logout } = useAuth();
  return (
    <div className="w-64 h-full bg-white border-r border-gray-200 p-4 flex flex-col">
      <div className="flex items-center gap-2 mb-8 px-2">
        <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white font-bold text-sm">
          RE
        </div>
        <span className="text-lg font-bold text-gray-900">Resume Enhancer</span>
      </div>

      <nav className="space-y-1">
        <NavLink
          to="/"
          end
          onClick={onNavigate}
          className={({ isActive }) => `${base} ${isActive ? active : inactive}`}
        >
          Generate
        </NavLink>

        <NavLink
          to="/history"
          onClick={onNavigate}
          className={({ isActive }) => `${base} ${isActive ? active : inactive}`}
        >
          History
        </NavLink>
      </nav>
       <div className="mt-auto pt-4 border-t text-sm">
        {user && (
          <>
            <div className="px-2 mb-1 truncate">{user.email}</div>
            <div className="px-2 mb-3 text-xs text-gray-500">
              {user.remaining_quota} generation{user.remaining_quota === 1 ? "" : "s"} left today
            </div>
            <button
              onClick={logout}
              className="w-full text-left px-4 py-2 text-red-500 hover:bg-red-50 rounded-lg"
            >
              Log out
            </button>
          </>
        )}
      </div>
    </div>
  );
}