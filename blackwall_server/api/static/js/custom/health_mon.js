async function check_server(endpoint, status_object) {
    const result = await fetch(endpoint)
    .then(response => {
            return response.status
    })
    .catch(error => {
            if (error == "TypeError: Failed to fetch"){return 503}
            return error
    });
    console.log(`HealthMon for ${endpoint}: ${result}`)
    if (result == 200) {
        status_object.textContent = `Online/${result}`
    }
    if (result == 500) {
        status_object.textContent = `Online/${result} (Server-side error)`
    }
    if (result == 503) {
        status_object.textContent = `Offline/${result}`
    }
    if (result == 404) {
        status_object.textContent = `Online/${result} (No found)`
    }
}

const sseHealth = document.querySelector(".sse-status");
const serverHealth = document.querySelector(".server-status");
check_server('/health', serverHealth);
check_server('/sse/healthmon', sseHealth);

