"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2, Sparkles, Bot, Zap } from "lucide-react";
import MessageList from "@/components/Chat/MessageList";
import { processMessage, sendChatMessage } from "@/lib/api-client";
import { toast } from "sonner";

interface Message { role: "user" | "assistant"; content: string; taskType?: string; }

const SKILLS_OPTIONS = [
  { value: "python-expert", label: "Python Expert", icon: "🐍" },
  { value: "react-developer", label: "React Developer", icon: "⚛️" },
  { value: "system-architect", label: "System Architect", icon: "🏗️" },
  { value: "code-reviewer", label: "Code Reviewer", icon: "🔍" },
  { value: "devops-engineer", label: "DevOps Engineer", icon: "🚀" },
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [sessionId] = useState(() => `web_${Date.now()}`);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const toggleSkill = (skill: string) => {
    setSelectedSkills((prev) => prev.includes(skill) ? prev.filter((s) => s !== skill) : [...prev, skill]);
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const um: Message = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, um]);
    setInput("");
    setLoading(true);
    try {
      let response: string;
      let taskType = "chat";
      
      try {
        const r = await processMessage({
          message: input.trim(),
          channel: "web",
          session_id: sessionId,
          skills: selectedSkills.length > 0 ? selectedSkills : undefined,
        });
        response = r.response;
        taskType = r.task_type;
      } catch {
        const r = await sendChatMessage({
          messages: [...messages, um],
          skills: selectedSkills.length > 0 ? selectedSkills : undefined,
        });
        response = r.message;
      }
      
      setMessages((prev) => [...prev, { 
        role: "assistant", 
        content: response,
        taskType: taskType,
      }]);
    } catch (e: any) { 
      const msg = e?.response?.data?.detail || e?.message || "Failed to get response";
      if (msg.includes("429") || msg.includes("rate")) {
        toast.error("Rate limited. Please try again later.");
      } else {
        toast.error(msg);
      }
    } finally { 
      setLoading(false); 
    }
  };

  const getTaskTypeBadge = (taskType?: string) => {
    const badges: Record<string, { label: string; color: string }> = {
      chat: { label: "💬 Chat", color: "bg-violet-500/10 text-violet-400 border-violet-500/20" },
      code: { label: "💻 Code", color: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" },
      scrape: { label: "🌐 Scrape", color: "bg-amber-500/10 text-amber-400 border-amber-500/20" },
      search: { label: "🔍 Search", color: "bg-blue-500/10 text-blue-400 border-blue-500/20" },
      analyze: { label: "📊 Analyze", color: "bg-rose-500/10 text-rose-400 border-rose-500/20" },
    };
    const badge = taskType ? badges[taskType] : null;
    if (!badge) return null;
    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${badge.color}`}>
        {badge.label}
      </span>
    );
  };

  return (
    <div className="flex flex-col h-full relative">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-violet-500/5 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-indigo-500/5 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }} />
      </div>

      {/* Header */}
      <header className="relative z-10 glass px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-violet-500/30 animate-pulse-glow">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">AI Agent Chat</h2>
              <div className="flex items-center gap-2 text-sm text-slate-400">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span>Powered by Orchestrator</span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="badge">
              <Zap className="w-3 h-3 mr-1.5" />
              AI Active
            </div>
          </div>
        </div>
      </header>
      
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-6 relative z-10">
        <div className="max-w-4xl mx-auto">
          {messages.length === 0 ? (
            <div className="text-center py-16 animate-fade-in">
              <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-gradient-to-br from-violet-500/20 to-indigo-500/20 border border-violet-500/20 mb-6">
                <Sparkles className="w-10 h-10 text-violet-400" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3 gradient-text">Welcome to AmkyawDev Tools</h3>
              <p className="text-slate-400 mb-8 max-w-md mx-auto">
                Your AI-powered coding assistant. Select skills below and start building.
              </p>
              
              {/* Skills Selection */}
              <div className="flex flex-wrap justify-center gap-3 mb-8">
                {SKILLS_OPTIONS.map((sk, i) => (
                  <button 
                    key={sk.value} 
                    onClick={() => toggleSkill(sk.value)}
                    className={`
                      px-5 py-3 rounded-2xl text-sm font-medium transition-all duration-300 flex items-center gap-2
                      ${selectedSkills.includes(sk.value) 
                        ? "bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-lg shadow-violet-500/30 scale-105" 
                        : "glass text-slate-300 hover:text-white hover:scale-105"
                      }
                    `}
                    style={{ animationDelay: `${i * 100}ms` }}
                  >
                    <span>{sk.icon}</span>
                    <span>{sk.label}</span>
                  </button>
                ))}
              </div>

              {/* Quick Actions */}
              <div className="flex flex-wrap justify-center gap-3">
                {["Write a Python REST API", "Create React component", "Debug my code"].map((prompt) => (
                  <button
                    key={prompt}
                    onClick={() => setInput(prompt)}
                    className="glass px-4 py-2 rounded-xl text-sm text-slate-400 hover:text-white hover:border-violet-500/30 transition-all duration-300"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((msg, i) => (
                <div key={i}>
                  {msg.taskType && msg.role === "assistant" && (
                    <div className="flex items-center gap-2 mb-4 ml-2">
                      {getTaskTypeBadge(msg.taskType)}
                    </div>
                  )}
                </div>
              ))}
              <MessageList messages={messages} />
            </>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      {/* Input Area */}
      <div className="relative z-10 glass px-6 py-4">
        <div className="max-w-4xl mx-auto">
          {selectedSkills.length > 0 && (
            <div className="flex items-center gap-2 mb-4 flex-wrap">
              <span className="text-xs text-slate-500">Active Skills:</span>
              {selectedSkills.map((sk) => {
                const skill = SKILLS_OPTIONS.find((s) => s.value === sk);
                return (
                  <span key={sk} className="badge">
                    <span className="mr-1">{skill?.icon}</span>
                    {skill?.label}
                  </span>
                );
              })}
            </div>
          )}
          <div className="flex items-end gap-4">
            <textarea 
              value={input} 
              onChange={(e) => setInput(e.target.value)} 
              onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); }}}
              placeholder="Ask anything about code..." 
              rows={1} 
              className="input-field resize-none max-h-40 flex-1" 
              disabled={loading} 
            />
            <button 
              onClick={handleSend} 
              disabled={!input.trim() || loading} 
              className="btn-primary flex items-center gap-2 shrink-0 px-6 py-4"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
              <span>Send</span>
            </button>
          </div>
          <p className="text-xs text-slate-600 mt-3 text-center">
            Press Enter to send, Shift+Enter for new line
          </p>
        </div>
      </div>
    </div>
  );
}