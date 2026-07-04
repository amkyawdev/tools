"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { MessageSquare, Database, FolderOpen, Settings, Brain, Code2, X } from "lucide-react";
import clsx from "clsx";

const navItems = [
  { href: "/", label: "Chat", icon: MessageSquare },
  { href: "/knowledge", label: "Knowledge", icon: Database },
  { href: "/files", label: "Files", icon: FolderOpen },
  { href: "/settings", label: "Settings", icon: Settings },
];

interface SidebarProps { open: boolean; onClose: () => void; }

export default function Sidebar({ open, onClose }: SidebarProps) {
  const pathname = usePathname();
  return (<>{open && <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" onClick={onClose} />}<aside className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-white border-r border-slate-200 flex flex-col transition-transform duration-300 ${open ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}`}><div className="p-5 border-b border-slate-200 flex items-center justify-between"><div className="flex items-center gap-3"><div className="w-9 h-9 bg-primary-600 rounded-lg flex items-center justify-center"><Brain className="w-5 h-5 text-white" /></div><div><h1 className="font-bold text-slate-900 text-sm">AmkyawDev</h1><p className="text-xs text-slate-500">Tools v1.0</p></div></div><button onClick={onClose} className="lg:hidden p-1 rounded-md hover:bg-slate-100 text-slate-500"><X className="w-5 h-5" /></button></div><nav className="flex-1 p-3 space-y-1">{navItems.map((item) => { const Icon = item.icon; const isActive = pathname === item.href; return (<Link key={item.href} href={item.href} onClick={onClose} className={clsx("sidebar-link", isActive && "active")}><Icon className="w-5 h-5" /><span>{item.label}</span></Link>); })}</nav><div className="p-4 border-t border-slate-200"><a href="https://amkyaw.dev" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-xs text-slate-500 hover:text-primary-600"><Code2 className="w-4 h-4" /><span>amkyaw.dev</span></a></div></aside></>);
}