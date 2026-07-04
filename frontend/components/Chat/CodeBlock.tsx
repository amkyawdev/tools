"use client";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { useState } from "react";

interface CodeBlockProps { language: string; code: string; }

export default function CodeBlock({ language, code }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);
  const handleCopy = async () => { await navigator.clipboard.writeText(code); setCopied(true); setTimeout(() => setCopied(false), 2000); };
  return (<div className="relative my-3 rounded-xl overflow-hidden border border-slate-700"><div className="flex items-center justify-between px-4 py-2 bg-slate-800"><span className="text-xs text-slate-400 font-mono">{language}</span><button onClick={handleCopy} className="text-xs text-slate-400 hover:text-white transition-colors">{copied ? "✓ Copied!" : "📋 Copy"}</button></div><SyntaxHighlighter language={language} style={oneDark} customStyle={{ margin: 0, borderRadius: 0 }}>{code}</SyntaxHighlighter></div>);
}