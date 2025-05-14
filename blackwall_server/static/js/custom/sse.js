const eventSource = new EventSource("/sse/stream");
console.log("Connecting to", eventSource.url)

eventSource.onmessage = (event) => {
    event = JSON.parse(event.data)
    console.log("SSE sent:", event)
    console.log(event.SERVER_EVENT)
    if (event.SERVER_EVENT == "OFF"){
        alert("Server is going down")
        eventSource.close()
    }
};

eventSource.onopen = (event) => {
    console.log("Connected to SSE server!")
    send_to_server('/sse/receive', {"agent_id": getCookieByName('blackwall_client-id'), "state": "ready"})
    check_server('/sse', sseHealth);
    check_server('/health', serverHealth)
};

eventSource.onerror = (event) => {
    console.log(eventSource)
    check_server('/sse', sseHealth)
    check_server('/health', serverHealth)
    if (eventSource.readyState == 0) {
        console.log("Lost connection to SSE server, reconnecting...", eventSource.url)
    } else {
        console.log("Error occurred!", event)
    }
};