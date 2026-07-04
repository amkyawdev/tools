import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 60000,
  headers: { "Content-Type": "application/json" },
});

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

export async function searchKnowledge(query: string, skill?: string, limit = 10) {
  const response = await api.get("/api/knowledge/search", { params: { q: query, skill, limit } });
  return response.data;
}

export async function upsertKnowledge(data: { id: string; content: string; metadata?: Record<string, any>; skill?: string }) {
  const response = await api.post("/api/knowledge/upsert", data);
  return response.data;
}

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