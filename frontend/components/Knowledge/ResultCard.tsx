interface ResultCardProps { id: string; content: string; score?: number; skill?: string; }

export default function ResultCard({ id, content, score, skill }: ResultCardProps) {
  return (<div className="bg-white border border-slate-200 rounded-xl p-4 hover:border-primary-300 transition-colors"><div className="flex items-center justify-between mb-2"><span className="font-mono text-sm text-primary-600">{id}</span><div className="flex items-center gap-2">{skill && <span className="px-2 py-0.5 bg-slate-100 text-slate-600 rounded text-xs">{skill}</span>}{score !== undefined && <span className="text-xs text-slate-400">{(score * 100).toFixed(0)}% match</span>}</div></div><p className="text-sm text-slate-700 line-clamp-4">{content}</p></div>);
}