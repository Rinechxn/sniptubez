function checkStatus() {
    const apiUrl = "http://localhost:5000/download"; // Replace with the actual API URL

    fetch(apiUrl, {
        method: "GET",
        mode: "no-cors",
        cache: "no-cache",
    })
    .then(() => {
        setStatusText("Online");
    })
    .catch(() => {
        setStatusText("Offline");
    });
}

function setStatusText(status) {
    const statusTextElement = document.getElementById("status-text");
    statusTextElement.textContent = `Sniptubez.app is currently ${status}.`;
}

// Auto check status every 10 seconds (adjust the interval as needed)
setInterval(checkStatus, 10000);