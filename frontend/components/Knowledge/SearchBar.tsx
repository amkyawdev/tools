import { Search } from "lucide-react";

interface SearchBarProps { value: string; onChange: (value: string) => void; onSearch: () => void; loading?: boolean; placeholder?: string; }

export default function SearchBar({ value, onChange, onSearch, loading, placeholder = "Search..." }: SearchBarProps) {
  return (<div className="flex gap-3"><div className="relative flex-1"><Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" /><input type="text" value={value} onChange={(e) => onChange(e.target.value)} onKeyDown={(e) => e.key === "Enter" && onSearch()} placeholder={placeholder} className="input-field pl-10" /></div><button onClick={onSearch} disabled={loading || !value.trim()} className="btn-primary">{loading ? "Searching..." : "Search"}</button></div>);
}