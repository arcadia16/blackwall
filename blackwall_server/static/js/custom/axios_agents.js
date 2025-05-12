const axiosAgents = document.querySelectorAll(".axios-get");
axiosAgents.forEach((axiosAgent) => axiosAgent.addEventListener("click", axios_get_agent_state))

async function axios_get_agent_state() {
    const axios_resp = document.querySelector("#agent_" + this.value)
    axios_resp.textContent = 'Pending...'
    const response = await axios.get('/ag/' + this.value)
    console.log(response)
    if (response.data == null) {
        axios_resp.textContent = 'Agent connection failed.'
    }
    else {
        var status = document.querySelector("#status_" + this.value)
        status.classList.remove("bi-question-circle")
        axios_resp.textContent = `Agent ${response.data.AGENT_ID}: ${response.data.STATE}`
        // Separate classes for states DEAD, BRCH, WARN, GOOD, make switch function
        if (response.data.STATE == 200) {
            status.classList.add("bi-check-circle-fill", "text-success")
        }
        if (response.data.STATE == 300) {
            status.classList.add("bi-wrench-adjustable-circle-fill", "text-warning-emphasis")
        }
        if (response.data.STATE == 400) {
            status.classList.add("bi-x-circle-fill", "text-danger")
        }
    }
}