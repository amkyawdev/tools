"use client";

import { useState, useEffect } from "react";
import { Upload, FileText, Loader2 } from "lucide-react";
import { listFiles, uploadFile } from "@/lib/api-client";
import { toast } from "sonner";

interface FileInfo { name: string; path: string; size: number; modified: string; }

export default function FilesPage() {
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  useEffect(() => { loadFiles(); }, []);

  const loadFiles = async () => { try { const data = await listFiles(); setFiles(data.files || []); } catch (e: any) { toast.error("Failed to load files"); } finally { setLoading(false); } };

  const handleUpload = async (ev: React.ChangeEvent<HTMLInputElement>) => { const f = ev.target.files?.[0]; if (!f) return; setUploading(true); try { await uploadFile(f); toast.success(`Uploaded: ${f.name}`); await loadFiles(); } catch (e: any) { toast.error(e.message || "Upload failed"); } finally { setUploading(false); } };

  const fmtSize = (b: number) => b < 1024 ? `${b} B` : b < 1048576 ? `${(b / 1024).toFixed(1)} KB` : `${(b / 1048576).toFixed(1)} MB`;

  return (<div className="flex flex-col h-full">
    <header className="bg-white border-b border-slate-200 px-6 py-4"><div className="max-w-4xl mx-auto flex items-center justify-between"><div><h2 className="text-lg font-semibold text-slate-900">Files</h2><p className="text-sm text-slate-500">Manage uploaded and generated files</p></div><label className="btn-primary flex items-center gap-2 cursor-pointer">{uploading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Upload className="w-4 h-4" />}Upload<input type="file" onChange={handleUpload} className="hidden" /></label></div></header>
    <div className="flex-1 overflow-y-auto px-6 py-6"><div className="max-w-4xl mx-auto">{loading ? (<div className="flex items-center justify-center py-20"><Loader2 className="w-6 h-6 animate-spin text-slate-400" /></div>) : files.length === 0 ? (<div className="text-center py-20"><FileText className="w-12 h-12 text-slate-300 mx-auto mb-4" /><h3 className="text-lg font-medium text-slate-700 mb-2">No files yet</h3><p className="text-slate-500">Upload files or generate code to see them here</p></div>) : (<div className="bg-white border border-slate-200 rounded-xl overflow-hidden"><div className="grid grid-cols-12 gap-4 px-4 py-3 bg-slate-50 text-xs font-medium text-slate-500 uppercase"><div className="col-span-5">Name</div><div className="col-span-3">Path</div><div className="col-span-2">Size</div><div className="col-span-2">Modified</div></div>{files.map((f, i) => (<div key={i} className="grid grid-cols-12 gap-4 px-4 py-3 border-t border-slate-100 text-sm hover:bg-slate-50"><div className="col-span-5 font-medium text-slate-900 flex items-center gap-2"><FileText className="w-4 h-4 text-slate-400" />{f.name}</div><div className="col-span-3 text-slate-500 font-mono text-xs truncate">{f.path}</div><div className="col-span-2 text-slate-500">{fmtSize(f.size)}</div><div className="col-span-2 text-slate-500">{new Date(f.modified).toLocaleDateString()}</div></div>))}</div>)}</div></div>
  </div>);
}