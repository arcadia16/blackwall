var eventSource = new EventSource("/stream");
console.log("Connecting to", eventSource.url)
ask_server('/hello')

eventSource.addEventListener('publish', function(event) {
        var data = JSON.parse(event.data)
        console.log(data)
    }, false);

eventSource.addEventListener('error', function(event) {
        console.log(event)
        console.log("Failed to connect to event stream. Is Redis running?")
        check_server('/stream', sseHealth)
    }, false);

eventSource.onmessage = (event) => {
    event = JSON.parse(event.data)
    console.log("SSE sent:", event)
};

eventSource.onopen = (event) => {
    console.log("Connected to SSE server!")
    send_to_server('/receive', {"agent_id": getCookieByName('blackwall_client-id'), "state": "ready"})
    check_server('/stream', sseHealth)
};

eventSource.onerror = (event) => {
    console.log(eventSource)
    check_server('/stream', sseHealth)
    check_server('/health', serverHealth)
    if (eventSource.readyState == 0) {
        console.log("Lost connection to SSE server, reconnecting...", eventSource.url)
        ask_server('/hello')
    } else {
        console.log("Error occurred!", event)
    }
};