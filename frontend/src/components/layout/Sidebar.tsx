import { NavLink } from "react-router-dom";

const base = "block px-4 py-2.5 rounded-lg text-sm font-medium transition";
const active = "bg-blue-600 text-white";
const inactive = "text-gray-600 hover:bg-gray-100";

export default function Sidebar() {
  return (
    <aside className="w-56 shrink-0 border-r bg-white h-screen sticky top-0 p-4 flex flex-col">
      <div className="text-lg font-bold mb-8 px-2">Resume Enhancer</div>

      <nav className="space-y-1">
        <NavLink
          to="/"
          end
          className={({ isActive }) => `${base} ${isActive ? active : inactive}`}
        >
          Generate
        </NavLink>

        <NavLink
          to="/history"
          className={({ isActive }) => `${base} ${isActive ? active : inactive}`}
        >
          History
        </NavLink>
      </nav>
    </aside>
  );
}