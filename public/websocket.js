const ws = new WebSocket("ws://localhost:8000/ws");

ws.onopen = () => {
    console.log("Connected to WebSocket server");
};

ws.onmessage = (event) => {
    const data = event.data;
    console.log("Message received from server:", data);
    // Aquí puedes actualizar la UI con los datos recibidos
};

ws.onclose = () => {
    console.log("Disconnected from WebSocket server");
};

ws.onerror = (error) => {
    console.error("WebSocket error:", error);
};
