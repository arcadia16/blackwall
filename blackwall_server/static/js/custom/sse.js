const eventSource = new EventSource("/sse/stream");
console.log("Connecting to", eventSource.url)
const serverStatus = document.querySelector(".server-status");
serverStatus.textContent = "Unknown"

eventSource.onmessage = (event) => {
    console.log("SSE sent:", event.data)
    serverStatus.textContent = event.data;
};

eventSource.onopen = (event) => {
    console.log("Connected to SSE server!")
    serverStatus.textContent = "Good"
};

eventSource.onerror = (event) => {
    console.log(eventSource)
    if (eventSource.readyState == 0) {
        serverStatus.textContent = "Bad"
        console.log("Lost connection to SSE server, reconnecting...", eventSource.url)
    } else {
        console.log("Error occurred!", e)
    }
};