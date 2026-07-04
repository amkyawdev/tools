"use client";

import { useState } from "react";
import { Menu } from "lucide-react";
import "@/styles/globals.css";
import { Toaster } from "sonner";
import Sidebar from "@/components/UI/Sidebar";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  return (<html lang="en"><body><div className="flex h-screen overflow-hidden"><div className="lg:hidden fixed top-0 left-0 right-0 z-30 bg-white border-b border-slate-200 px-4 py-3 flex items-center gap-3"><button onClick={() => setSidebarOpen(true)} className="p-1 rounded-md hover:bg-slate-100 text-slate-700"><Menu className="w-6 h-6" /></button><span className="font-bold text-slate-900 text-sm">AmkyawDev Tools</span></div><Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} /><main className="flex-1 overflow-y-auto bg-slate-50 pt-14 lg:pt-0">{children}</main></div><Toaster position="bottom-right" /></body></html>);
}