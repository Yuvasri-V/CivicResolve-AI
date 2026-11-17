import { useEffect, useState } from "react";

const WS_URL = "ws://127.0.0.1:8000/ws/live";

export default function useLiveFeed() {
  const [events, setEvents] = useState([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    let socket;
    let retryTimer;

    function connect() {
      socket = new WebSocket(WS_URL);

      socket.onopen = () => setConnected(true);

      socket.onclose = () => {
        setConnected(false);
        retryTimer = window.setTimeout(connect, 3000);
      };

      socket.onmessage = (message) => {
        try {
          const payload = JSON.parse(message.data);
          setEvents((current) => [payload, ...current].slice(0, 40));
        } catch {
          // ignore malformed payloads
        }
      };
    }

    connect();

    return () => {
      window.clearTimeout(retryTimer);
      if (socket) socket.close();
    };
  }, []);

  return { events, connected };
}
