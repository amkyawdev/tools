"use client";

import { useState, useEffect } from "react";
import { Key, Globe, Bot, RefreshCw, Zap } from "lucide-react";
import { getServicesStatus } from "@/lib/api-client";
import { toast } from "sonner";

interface ServiceStatus {
  llm: { configured: boolean; service: string };
  neon: { configured: boolean; service: string };
  browserless: { configured: boolean; service: string };
  kafka: { enabled: boolean };
}

export default function SettingsPage() {
  const [services, setServices] = useState<ServiceStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [webhookUrl, setWebhookUrl] = useState("");

  useEffect(() => {
    loadServices();
  }, []);

  const loadServices = async () => {
    setLoading(true);
    try {
      const status = await getServicesStatus();
      setServices(status);
    } catch (e: any) {
      toast.error("Failed to load services status");
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (configured: boolean) => {
    if (configured) {
      return <span className="text-xs px-2 py-1 bg-green-50 text-green-700 rounded-full">✅ Active</span>;
    }
    return <span className="text-xs px-2 py-1 bg-yellow-50 text-yellow-700 rounded-full">⚠️ Not configured</span>;
  };

  const serviceList = services ? [
    { name: "OpenRouter (LLM)", configured: services.llm?.configured || false },
    { name: "Neon (PostgreSQL)", configured: services.neon?.configured || false },
    { name: "Browserless (Web Scraping)", configured: services.browserless?.configured || false },
    { name: "Kafka (Events)", configured: services.kafka?.enabled || false },
  ] : [
    { name: "OpenRouter (LLM)", configured: false },
    { name: "Neon (PostgreSQL)", configured: false },
    { name: "Browserless (Web Scraping)", configured: false },
    { name: "Kafka (Events)", configured: false },
  ];

  return (
    <div className="flex flex-col h-full">
      <header className="bg-white border-b border-slate-200 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Settings</h2>
            <p className="text-sm text-slate-500">Configure your AmkyawDev Tools</p>
          </div>
          <button onClick={loadServices} disabled={loading} className="btn-secondary flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            Refresh
          </button>
        </div>
      </header>
      
      <div className="flex-1 overflow-y-auto px-6 py-6">
        <div className="max-w-4xl mx-auto space-y-6">
          {/* API Configuration */}
          <section className="bg-white border border-slate-200 rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <Key className="w-5 h-5 text-primary-600" />
              <h3 className="font-semibold text-slate-900">API Configuration</h3>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">OpenRouter API Key</label>
                <input type="password" value="************" disabled className="input-field bg-slate-50" />
                <p className="text-xs text-slate-500 mt-1">Set via OPENROUTER_API_KEY env var</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Default Model</label>
                <input type="text" value="google/gemma-4-31b-it:free" disabled className="input-field bg-slate-50" />
              </div>
            </div>
          </section>

          {/* Service Connections */}
          <section className="bg-white border border-slate-200 rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <Globe className="w-5 h-5 text-green-600" />
              <h3 className="font-semibold text-slate-900">Service Connections</h3>
            </div>
            <div className="space-y-3">
              {serviceList.map((svc) => (
                <div key={svc.name} className="flex items-center justify-between py-2 border-b border-slate-100 last:border-0">
                  <span className="text-sm text-slate-700">{svc.name}</span>
                  {getStatusBadge(svc.configured)}
                </div>
              ))}
            </div>
          </section>

          {/* Telegram Configuration */}
          <section className="bg-white border border-slate-200 rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <Zap className="w-5 h-5 text-blue-600" />
              <h3 className="font-semibold text-slate-900">Telegram Bot</h3>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Webhook URL</label>
                <input 
                  type="url" 
                  placeholder="https://your-domain.com/api/telegram/webhook"
                  value={webhookUrl}
                  onChange={(e) => setWebhookUrl(e.target.value)}
                  className="input-field"
                />
                <p className="text-xs text-slate-500 mt-1">Set this URL in your Telegram Bot Father settings</p>
              </div>
              <div className="flex gap-2">
                <button className="btn-primary">
                  Save Webhook
                </button>
                <button className="btn-secondary">
                  Test Connection
                </button>
              </div>
            </div>
          </section>

          {/* Agent Information */}
          <section className="bg-white border border-slate-200 rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <Bot className="w-5 h-5 text-purple-600" />
              <h3 className="font-semibold text-slate-900">Agent Information</h3>
            </div>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div><span className="text-slate-500">Version:</span><span className="ml-2 text-slate-900 font-medium">1.0.0</span></div>
              <div><span className="text-slate-500">Backend:</span><span className="ml-2 text-slate-900 font-medium">FastAPI + Python</span></div>
              <div><span className="text-slate-500">Frontend:</span><span className="ml-2 text-slate-900 font-medium">Next.js 14 + React</span></div>
              <div><span className="text-slate-500">Orchestrator:</span><span className="ml-2 text-slate-900 font-medium">Active ✅</span></div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}