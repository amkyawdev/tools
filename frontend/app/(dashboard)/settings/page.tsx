"use client";

import { Key, Globe, Bot } from "lucide-react";

const services = [
  { name: "Qdrant (Vector DB)", configured: "Not configured" },
  { name: "Neon (PostgreSQL)", configured: "Not configured" },
  { name: "ElevenLabs (TTS)", configured: "Not configured" },
  { name: "NVIDIA NIM", configured: "Not configured" },
  { name: "Telegram Bot", configured: "Not configured" },
];

export default function SettingsPage() {
  return (<div className="flex flex-col h-full">
    <header className="bg-white border-b border-slate-200 px-6 py-4"><div className="max-w-4xl mx-auto"><h2 className="text-lg font-semibold text-slate-900">Settings</h2><p className="text-sm text-slate-500">Configure your AmkyawDev Tools</p></div></header>
    <div className="flex-1 overflow-y-auto px-6 py-6"><div className="max-w-4xl mx-auto space-y-6">
      <section className="bg-white border border-slate-200 rounded-xl p-6"><div className="flex items-center gap-3 mb-4"><Key className="w-5 h-5 text-primary-600" /><h3 className="font-semibold text-slate-900">API Configuration</h3></div><div className="space-y-4"><div><label className="block text-sm font-medium text-slate-700 mb-1">OpenRouter API Key</label><input type="password" value="************" disabled className="input-field bg-slate-50" /><p className="text-xs text-slate-500 mt-1">Set via OPENROUTER_API_KEY env var</p></div><div><label className="block text-sm font-medium text-slate-700 mb-1">Default Model</label><input type="text" value="anthropic/claude-sonnet-4.5" disabled className="input-field bg-slate-50" /></div></div></section>
      <section className="bg-white border border-slate-200 rounded-xl p-6"><div className="flex items-center gap-3 mb-4"><Globe className="w-5 h-5 text-green-600" /><h3 className="font-semibold text-slate-900">Service Connections</h3></div><div className="space-y-3">{services.map((svc) => (<div key={svc.name} className="flex items-center justify-between py-2 border-b border-slate-100 last:border-0"><span className="text-sm text-slate-700">{svc.name}</span><span className="text-xs px-2 py-1 bg-yellow-50 text-yellow-700 rounded-full">{svc.configured}</span></div>))}</div></section>
      <section className="bg-white border border-slate-200 rounded-xl p-6"><div className="flex items-center gap-3 mb-4"><Bot className="w-5 h-5 text-purple-600" /><h3 className="font-semibold text-slate-900">Agent Information</h3></div><div className="grid grid-cols-2 gap-4 text-sm"><div><span className="text-slate-500">Version:</span><span className="ml-2 text-slate-900 font-medium">1.0.0</span></div><div><span className="text-slate-500">Backend:</span><span className="ml-2 text-slate-900 font-medium">FastAPI + Python 3.11</span></div><div><span className="text-slate-500">Frontend:</span><span className="ml-2 text-slate-900 font-medium">Next.js 14 + React</span></div><div><span className="text-slate-500">Skills Loaded:</span><span className="ml-2 text-slate-900 font-medium">5 (.amkyaw)</span></div></div></section>
    </div></div>
  </div>);
}