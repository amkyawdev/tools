"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { User, Bot } from "lucide-react";

interface Message { role: "user" | "assistant"; content: string; }
interface MessageListProps { messages: Message[]; }

export default function MessageList({ messages }: MessageListProps) {
  return (<div className="space-y-6">{messages.map((message, index) => (<div key={index} className={`flex gap-3 ${message.role === "user" ? "flex-row-reverse" : "flex-row"}`}><div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${message.role === "user" ? "bg-primary-600" : "bg-slate-700"}`}>{message.role === "user" ? <User className="w-4 h-4 text-white" /> : <Bot className="w-4 h-4 text-white" />}</div><div className={message.role === "user" ? "chat-bubble-user" : "chat-bubble-assistant"}>{message.role === "assistant" ? (<ReactMarkdown components={{ code({ node, className, children, ...props }) { const match = /language-(\w+)/.exec(className || ""); const inline = !match; if (inline) return <code className="bg-slate-200 text-slate-800 px-1.5 py-0.5 rounded text-sm" {...props}>{children}</code>; return <CodeBlock language={match![1]}>{String(children).replace(/\n$/, "")}</CodeBlock>; } }}>{message.content}</ReactMarkdown>) : <p className="whitespace-pre-wrap text-sm">{message.content}</p>}</div></div>))}</div>);
}

function CodeBlock({ language, children }: { language: string; children: string }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = async () => { await navigator.clipboard.writeText(children); setCopied(true); setTimeout(() => setCopied(false), 2000); };
  return (<div className="relative my-3"><div className="flex items-center justify-between px-4 py-2 bg-slate-800 rounded-t-lg"><span className="text-xs text-slate-400 font-mono">{language}</span><button onClick={handleCopy} className="text-xs text-slate-400 hover:text-white transition-colors">{copied ? "Copied!" : "Copy"}</button></div><SyntaxHighlighter language={language} style={oneDark} customStyle={{ margin: 0, borderTopLeftRadius: 0, borderTopRightRadius: 0, borderBottomLeftRadius: "0.75rem", borderBottomRightRadius: "0.75rem" }}>{children}</SyntaxHighlighter></div>);
}