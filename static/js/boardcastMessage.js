let messageBoxContainer = document.getElementById("message-box");

function boardcastMessage(message, status) {
    if(!messageBoxContainer) return;

    let messageBox = document.createElement("div");
    messageBox.classList.add("alert");
    messageBox.classList.add(`alert-${status}`);
    
    let messageBoxItem = document.createElement("div");
    messageBoxItem.innerHTML = `
        <p><strong>${status}</strong>: ${message}</p>
    `;

    let closeButton = document.createElement("button");
    closeButton.innerHTML = "&times;";

    closeButton.addEventListener("click", () => {
        messageBox.remove();
    });

    messageBox.appendChild(messageBoxItem);
    messageBox.appendChild(closeButton);
    messageBoxContainer.appendChild(messageBox);
}