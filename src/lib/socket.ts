export class BuildSocketClient {
  private socket: WebSocket | null = null;
  private project_id: string;
  private onMessageCallback: (data: any) => void;

  constructor(project_id: string, onMessageCallback: (data: any) => void) {
    this.project_id = project_id;
    this.onMessageCallback = onMessageCallback;
  }

  connect() {
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";
    const fullUrl = `${wsUrl}/ws/build/${this.project_id}`;

    this.socket = new WebSocket(fullUrl);

    this.socket.onopen = () => {
      console.log(`[ForgeAI Socket] Connected to stream for project ${this.project_id}`);
    };

    this.socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        this.onMessageCallback(payload);
      } catch (err) {
        console.error("[ForgeAI Socket] Error parsing socket payload:", err);
      }
    };

    this.socket.onerror = (err) => {
      console.error("[ForgeAI Socket] Error:", err);
    };

    this.socket.onclose = () => {
      console.log("[ForgeAI Socket] Connection closed");
    };
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}
