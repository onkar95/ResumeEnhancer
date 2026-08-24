import { useState } from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";

export default function AppLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  return <div className="flex min-h-screen w-full bg-gray-50">
    <div className="sticky top-0 hidden h-screen shrink-0 lg:block"><Sidebar /></div>
    {mobileOpen && <div className="fixed inset-0 z-50 lg:hidden"><button aria-label="Close menu" className="absolute inset-0 bg-black/30" onClick={() => setMobileOpen(false)} /><div className="absolute inset-y-0 left-0 shadow-2xl"><Sidebar onNavigate={() => setMobileOpen(false)} /></div></div>}
    <div className="flex min-w-0 flex-1 flex-col">
      <div className="sticky top-0 z-40 flex h-14 items-center border-b border-gray-200 bg-white px-4 lg:hidden"><button onClick={() => setMobileOpen(true)} className="mr-3 rounded-lg p-2 text-gray-600 hover:bg-gray-100">☰</button><span className="font-bold text-gray-950">Resume Enhancer</span></div>
      <main className="min-w-0 flex-1 overflow-x-hidden"><Outlet /></main>
    </div>
  </div>;
}
