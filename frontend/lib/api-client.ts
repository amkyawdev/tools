import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 60000,
  headers: { "Content-Type": "application/json" },
});

// ============ AGENT ROUTES ============

export async function sendChatMessage(data: { messages: { role: string; content: string }[]; skills?: string[]; model?: string }) {
  const response = await api.post("/api/agent/chat", data);
  return response.data;
}

export async function generateCode(data: { prompt: string; language?: string; skills?: string[]; context?: string }) {
  const response = await api.post("/api/agent/generate", data);
  return response.data;
}

export async function listSkills() {
  const response = await api.get("/api/agent/skills");
  return response.data;
}

// ============ ORCHESTRATOR ROUTES ============

export interface OrchestratorRequest {
  message: string;
  channel?: "web" | "telegram" | "cli" | "voice" | "api";
  session_id?: string;
  skills?: string[];
  context?: Record<string, any>;
}

export interface OrchestratorResponse {
  response: string;
  task_type: string;
  session_id: string;
  duration_ms: number;
  metadata: Record<string, any>;
  actions: Array<{ type: string; url?: string; label?: string }>;
}

export async function processMessage(data: OrchestratorRequest): Promise<OrchestratorResponse> {
  const response = await api.post("/api/orchestrator/process", data);
  return response.data;
}

export async function scrapeUrl(url: string): Promise<{
  url: string;
  html_length: number;
  html_preview: string;
  summary?: string;
}> {
  const response = await api.post("/api/orchestrator/scrape", null, { params: { url } });
  return response.data;
}

export async function getSessionInfo(sessionId: string) {
  const response = await api.get(`/api/orchestrator/session/${sessionId}`);
  return response.data;
}

export async function clearSession(sessionId: string) {
  const response = await api.delete(`/api/orchestrator/session/${sessionId}`);
  return response.data;
}

export async function getServicesStatus() {
  const response = await api.get("/api/orchestrator/services/status");
  return response.data;
}

// ============ KNOWLEDGE ROUTES ============

export async function searchKnowledge(query: string, skill?: string, limit = 10) {
  const response = await api.get("/api/knowledge/search", { params: { q: query, skill, limit } });
  return response.data;
}

export async function upsertKnowledge(data: { id: string; content: string; metadata?: Record<string, any>; skill?: string }) {
  const response = await api.post("/api/knowledge/upsert", data);
  return response.data;
}

// ============ FILE ROUTES ============

export async function uploadFile(file: File, skill?: string) {
  const formData = new FormData();
  formData.append("file", file);
  if (skill) formData.append("skill", skill);
  const response = await api.post("/api/files/upload", formData, { headers: { "Content-Type": "multipart/form-data" } });
  return response.data;
}

export async function listFiles(skill?: string) {
  const response = await api.get("/api/files/list", { params: { skill } });
  return response.data;
}

export async function exportFiles(format: "zip" | "pdf" = "zip", skill?: string) {
  const response = await api.get("/api/files/export", { params: { format, skill }, responseType: "blob" });
  return response.data;
}

// ============ TELEGRAM (ADMIN) ============

export async function setTelegramWebhook(url: string) {
  const response = await api.post("/api/telegram/webhook/set", null, { params: { url } });
  return response.data;
}

export async function testTelegramWebhook() {
  const response = await api.get("/api/telegram/webhook/test");
  return response.data;
}