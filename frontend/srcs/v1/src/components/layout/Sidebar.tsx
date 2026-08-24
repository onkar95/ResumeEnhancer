import { NavLink } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

interface Props { onNavigate?: () => void; }
const main = [
  ["/", "Dashboard"],
  ["/generate", "+ New resume"],
  ["/history", "History"],
];

export default function Sidebar({ onNavigate }: Props) {
  const { user, logout } = useAuth();
  return <aside className="flex h-full w-64 flex-col border-r border-gray-200 bg-white px-3 py-4">
    <div className="mb-8 flex items-center gap-2 px-2"><div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600 text-xs font-bold text-white">RE</div><span className="font-bold text-gray-950">Resume Enhancer</span></div>
    <div className="px-2 pb-2 text-[10px] font-bold uppercase tracking-widest text-gray-400">Workspace</div>
    <nav className="space-y-1">{main.map(([to, label]) => <NavLink key={to} to={to} end={to === "/"} onClick={onNavigate} className={({isActive}) => `block rounded-lg px-3 py-2.5 text-sm font-medium transition ${isActive ? "bg-brand-600 text-white" : "text-gray-600 hover:bg-gray-50 hover:text-gray-950"}`}>{label}</NavLink>)}</nav>
    <div className="mt-7 px-2 pb-2 text-[10px] font-bold uppercase tracking-widest text-gray-400">AI workspace</div>
    <NavLink to="/history" onClick={onNavigate} className="rounded-lg px-3 py-2.5 text-sm text-gray-600 hover:bg-gray-50">Resume versions</NavLink>
    <div className="mt-auto border-t border-gray-100 pt-4">{user && <><div className="truncate px-2 text-xs font-medium text-gray-900">{user.email}</div><div className="px-2 pt-1 text-[11px] text-gray-400">{user.remaining_quota} generations left today</div><button onClick={logout} className="mt-3 w-full rounded-lg px-3 py-2 text-left text-xs font-medium text-red-500 hover:bg-red-50">Log out</button></>}</div>
  </aside>;
}
