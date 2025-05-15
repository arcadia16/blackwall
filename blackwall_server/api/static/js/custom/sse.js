var eventSource = new EventSource("/sse/stream");

console.log("Connecting to", eventSource.url)
ask_server('/sse/healthmon')

eventSource.onmessage = (event) => {
    console.log(event.data)
    if (JSON.parse(event.data) == 1) {console.log("Subscribed, server ready!")}
    console.log(event, "parsed:", JSON.parse(event.data))
};

eventSource.onopen = (event) => {
    console.log("Connected to SSE server!")
    //send_to_server('/receive', {"client_id": getCookieByName('blackwall_client-id'), "state": "ready"})
    check_server('/sse/healthmon', sseHealth)
};

eventSource.onerror = (event) => {
    console.log(eventSource.readyState, event)
    console.log("Failed to connect to event stream. Is Redis running?")
    check_server('/sse/healthmon', sseHealth)
    check_server('/health', serverHealth)
    if (eventSource.readyState == 0) {
        console.log("Lost connection to SSE server, reconnecting...", eventSource.url)
    } else {
        console.log("Error occurred!", event)
    }
};