import { useEffect, useRef } from 'react';

const CHAT_API_URL = `${process.env.NEXT_PUBLIC_CHAT_BACKEND}`;

export const useWebSocket = (sessionId: string | null | undefined) => {
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!sessionId) return; // Prevent connecting without sessionId

    const wsUrl = `${CHAT_API_URL.replace(/^http/, 'ws')}/ws/conversation/${sessionId}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('✅ WebSocket connected');
      ws.send(JSON.stringify({ type: 'start' }));
    };

    ws.onclose = () => {
      console.log('🔌 WebSocket disconnected');
    };

    const pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000);

    return () => {
      clearInterval(pingInterval);
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'end' }));
        ws.close();
      }
    };
  }, [sessionId]);
};