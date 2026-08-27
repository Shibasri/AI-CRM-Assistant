async function sendMessage() {
    const input = document.getElementById("message");
    const chatbox = document.getElementById("chatbox");

    const message = input.value.trim();

    if (!message) {
        return;
    }

    // Show user message
    const userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.innerHTML = `<strong>You:</strong> ${message}`;
    chatbox.appendChild(userMessage);

    input.value = "";

    // Send message to backend
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        // Show AI response
        const aiMessage = document.createElement("div");
        aiMessage.className = "message ai";
        aiMessage.innerHTML = `<strong>AI:</strong><br>${data.response.replace(/\n/g, "<br>")}`;

        chatbox.appendChild(aiMessage);

        chatbox.scrollTop = chatbox.scrollHeight;

    } catch (error) {
        const errorMessage = document.createElement("div");
        errorMessage.className = "message ai";
        errorMessage.innerHTML =
            "<strong>AI:</strong> Unable to connect to the server.";

        chatbox.appendChild(errorMessage);
    }
}


// Press Enter to send
document.getElementById("message").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});