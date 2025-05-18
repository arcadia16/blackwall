const axiosAgents = document.querySelectorAll(".axios-get");
axiosAgents.forEach((axiosAgent) => axiosAgent.addEventListener("click", axios_get_agent_state))

async function axios_get_agent_state() {
    const axios_resp = document.querySelector("#agent_" + this.value)
    axios_resp.textContent = 'Pending...'
    const response = await axios.get('/agent/' + this.value)
    console.log(response)
    if (response.data == null) {
        axios_resp.textContent = 'Agent connection failed.'
    }
    else {
        var status = document.querySelector("#status_" + this.value)
        axios_resp.textContent = `Agent ${response.data.AGENT_ID}: ${response.data.STATE}`
        // Separate classes for states DEAD, BRCH, WARN, GOOD, make switch function
        if (response.data.STATE == 200) {
            status.classList.remove("text-warning-emphasis", "text-danger")
            status.classList.add("text-success")
        }
        if (response.data.STATE == 300) {
            status.classList.remove("text-success", "text-danger")
            status.classList.add("text-warning-emphasis")
        }
        if (response.data.STATE == 400 || response.data.STATE == 500) {
            status.classList.remove("text-success", "text-warning-emphasis")
            status.classList.add("text-danger")
        }
    }
}