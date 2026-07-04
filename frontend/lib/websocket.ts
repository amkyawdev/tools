const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws";

type MessageHandler = (data: any) => void;

class WebSocketClient {
  private ws: WebSocket | null = null;
  private handlers: Map<string, Set<MessageHandler>> = new Map();
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN) return;
    this.ws = new WebSocket(WS_URL);
    this.ws.onopen = () => { console.log("WebSocket connected"); this.emit("connected", {}); };
    this.ws.onmessage = (event) => { try { const data = JSON.parse(event.data); this.emit("message", data); if (data.type) this.emit(data.type, data); } catch (e) { console.error("WebSocket parse error:", e); } };
    this.ws.onclose = () => { console.log("WebSocket disconnected"); this.emit("disconnected", {}); this.scheduleReconnect(); };
    this.ws.onerror = (error) => { console.error("WebSocket error:", error); };
  }

  private scheduleReconnect() {
    if (this.reconnectTimer) return;
    this.reconnectTimer = setTimeout(() => { this.reconnectTimer = null; this.connect(); }, 3000);
  }

  on(event: string, handler: MessageHandler) {
    if (!this.handlers.has(event)) this.handlers.set(event, new Set());
    this.handlers.get(event)!.add(handler);
    return () => this.handlers.get(event)?.delete(handler);
  }

  private emit(event: string, data: any) {
    this.handlers.get(event)?.forEach((handler) => handler(data));
  }

  disconnect() {
    if (this.reconnectTimer) { clearTimeout(this.reconnectTimer); this.reconnectTimer = null; }
    this.ws?.close();
    this.ws = null;
  }
}

export const wsClient = new WebSocketClient();