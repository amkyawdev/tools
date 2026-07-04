"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2 } from "lucide-react";
import MessageList from "@/components/Chat/MessageList";
import { sendChatMessage } from "@/lib/api-client";
import { toast } from "sonner";

interface Message { role: "user" | "assistant"; content: string; }
const SKILLS_OPTIONS = [
  { value: "python-expert", label: "Python Expert" },
  { value: "react-developer", label: "React Developer" },
  { value: "system-architect", label: "System Architect" },
  { value: "code-reviewer", label: "Code Reviewer" },
  { value: "devops-engineer", label: "DevOps Engineer" },
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);
  const toggleSkill = (skill: string) => setSelectedSkills((prev) => prev.includes(skill) ? prev.filter((s) => s !== skill) : [...prev, skill]);
  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const um: Message = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, um]);
    setInput("");
    setLoading(true);
    try {
      const r = await sendChatMessage({ messages: [...messages, um], skills: selectedSkills.length > 0 ? selectedSkills : undefined });
      setMessages((prev) => [...prev, { role: "assistant", content: r.message }]);
    } catch (e: any) { toast.error(e.message || "Failed"); }
    finally { setLoading(false); }
  };

  return (<div className="flex flex-col h-full">
    <header className="bg-white border-b border-slate-200 px-6 py-4"><div className="max-w-4xl mx-auto"><h2 className="text-lg font-semibold text-slate-900">Chat</h2><p className="text-sm text-slate-500">Ask the AI Coder Agent anything</p></div></header>
    <div className="flex-1 overflow-y-auto px-6 py-4"><div className="max-w-4xl mx-auto">{messages.length === 0 ? (<div className="text-center py-20"><h3 className="text-xl font-semibold text-slate-700 mb-2">Welcome to AmkyawDev Tools</h3><p className="text-slate-500 mb-6">Select skills below and start a conversation</p><div className="flex flex-wrap justify-center gap-2">{SKILLS_OPTIONS.map((sk) => (<button key={sk.value} onClick={() => toggleSkill(sk.value)} className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${selectedSkills.includes(sk.value) ? "bg-primary-600 text-white" : "bg-slate-100 text-slate-600 hover:bg-slate-200"}`}>{sk.label}</button>))}</div></div>) : (<MessageList messages={messages} />)}<div ref={messagesEndRef} /></div></div>
    <div className="bg-white border-t border-slate-200 px-6 py-4"><div className="max-w-4xl mx-auto">{selectedSkills.length > 0 && (<div className="flex items-center gap-2 mb-3 flex-wrap"><span className="text-xs text-slate-500">Skills:</span>{selectedSkills.map((sk) => (<span key={sk} className="px-2 py-0.5 bg-primary-50 text-primary-700 rounded-full text-xs font-medium">{SKILLS_OPTIONS.find((s) => s.value === sk)?.label}</span>))}</div>)}<div className="flex items-end gap-3"><textarea value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); }}} placeholder="Ask the AI Coder Agent..." rows={1} className="input-field resize-none max-h-32" disabled={loading} /><button onClick={handleSend} disabled={!input.trim() || loading} className="btn-primary flex items-center gap-2 shrink-0">{loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}<span>Send</span></button></div></div></div>
  </div>);
}