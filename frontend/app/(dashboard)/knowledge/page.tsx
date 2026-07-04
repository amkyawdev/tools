"use client";

import { useState } from "react";
import { Search, Plus, Loader2 } from "lucide-react";
import { searchKnowledge, upsertKnowledge } from "@/lib/api-client";
import { toast } from "sonner";

interface KnowledgeEntry { id: string; score?: number; content: string; metadata?: Record<string, any>; skill?: string; }

export default function KnowledgePage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<KnowledgeEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [showAdd, setShowAdd] = useState(false);
  const [newId, setNewId] = useState("");
  const [newContent, setNewContent] = useState("");
  const [newSkill, setNewSkill] = useState("");
  const [adding, setAdding] = useState(false);

  const handleSearch = async () => { if (!query.trim()) return; setLoading(true); try { const data = await searchKnowledge(query); setResults(data.results || []); } catch (e: any) { toast.error(e.message || "Search failed"); } finally { setLoading(false); } };
  const handleAdd = async () => { if (!newId.trim() || !newContent.trim()) return; setAdding(true); try { await upsertKnowledge({ id: newId.trim(), content: newContent.trim(), skill: newSkill.trim() || undefined }); toast.success("Knowledge entry added!"); setNewId(""); setNewContent(""); setNewSkill(""); setShowAdd(false); } catch (e: any) { toast.error(e.message || "Failed"); } finally { setAdding(false); } };

  return (<div className="flex flex-col h-full"><header className="bg-white border-b border-slate-200 px-6 py-4"><div className="max-w-4xl mx-auto flex items-center justify-between"><div><h2 className="text-lg font-semibold text-slate-900">Knowledge Base</h2><p className="text-sm text-slate-500">Vector search your code knowledge</p></div><button onClick={() => setShowAdd(!showAdd)} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" />Add Entry</button></div></header><div className="flex-1 overflow-y-auto px-6 py-6"><div className="max-w-4xl mx-auto space-y-6">{showAdd && (<div className="bg-white border border-slate-200 rounded-xl p-4 space-y-3"><h3 className="font-medium text-slate-900">New Knowledge Entry</h3><input placeholder="Entry ID" value={newId} onChange={(e) => setNewId(e.target.value)} className="input-field" /><textarea placeholder="Content..." value={newContent} onChange={(e) => setNewContent(e.target.value)} rows={4} className="input-field" /><input placeholder="Skill (optional)" value={newSkill} onChange={(e) => setNewSkill(e.target.value)} className="input-field" /><div className="flex gap-2"><button onClick={handleAdd} disabled={adding} className="btn-primary">{adding ? <Loader2 className="w-4 h-4 animate-spin" /> : "Save"}</button><button onClick={() => setShowAdd(false)} className="btn-secondary">Cancel</button></div></div>)}<div className="flex gap-3"><input placeholder="Search knowledge base..." value={query} onChange={(e) => setQuery(e.target.value)} onKeyDown={(e) => e.key === "Enter" && handleSearch()} className="input-field" /><button onClick={handleSearch} disabled={loading} className="btn-primary flex items-center gap-2">{loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}Search</button></div>{results.length > 0 && (<div className="space-y-3"><p className="text-sm text-slate-500">{results.length} results</p>{results.map((entry) => (<div key={entry.id} className="bg-white border border-slate-200 rounded-xl p-4"><div className="flex items-center justify-between mb-2"><span className="font-mono text-sm text-primary-600">{entry.id}</span><div className="flex items-center gap-2">{entry.skill && <span className="px-2 py-0.5 bg-slate-100 text-slate-600 rounded text-xs">{entry.skill}</span>}{entry.score !== undefined && <span className="text-xs text-slate-400">{(entry.score * 100).toFixed(0)}% match</span>}</div></div><p className="text-sm text-slate-700 line-clamp-4">{entry.content}</p></div>))}</div>)}{results.length === 0 && !loading && query && (<div className="text-center py-12"><p className="text-slate-500">No results found</p></div>)}</div></div></div>);
}