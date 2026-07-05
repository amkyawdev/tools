"use client";

import { useState } from "react";
import { Menu, Bot } from "lucide-react";
import "@/styles/globals.css";
import { Toaster } from "sonner";
import Sidebar from "@/components/UI/Sidebar";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  return (
    <html lang="en">
      <body>
        <div className="flex h-screen overflow-hidden">
          {/* Mobile Header */}
          <div className="lg:hidden fixed top-0 left-0 right-0 z-30 glass px-4 py-3 flex items-center gap-3">
            <button onClick={() => setSidebarOpen(true)} className="p-2 rounded-xl hover:bg-white/10 text-white">
              <Menu className="w-6 h-6" />
            </button>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-violet-600 to-indigo-600 rounded-xl flex items-center justify-center">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <span className="font-bold text-white text-sm">AmkyawDev Tools</span>
            </div>
          </div>
          
          <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
          
          <main className="flex-1 overflow-y-auto pt-14 lg:pt-0">
            {children}
          </main>
        </div>
        <Toaster position="bottom-right" />
      </body>
    </html>
  );
}