document.addEventListener("DOMContentLoaded", () => {
    const socket = io();

    // Handle motor commands
    function sendMotorCommand(motorId, value) {
        socket.emit("motor_command", { motor_id: motorId, value });
    }

    document.querySelectorAll(".control button").forEach(button => {
        button.addEventListener("click", event => {
            const control = event.target.closest(".control");
            const motorId = control.dataset.motorId;
            const value = control.querySelector("input").value;
            sendMotorCommand(motorId, value);
        });
    });

    // Handle saved positions
    const savedPositionsContainer = document.querySelector(".saved-positions ul");

    socket.on("saved_positions", positions => {
        savedPositionsContainer.innerHTML = "";
        positions.forEach(position => {
            const li = document.createElement("li");
            li.textContent = position;
            const loadButton = document.createElement("button");
            loadButton.textContent = "Load";
            loadButton.addEventListener("click", () => {
                socket.emit("load_position", position);
            });
            li.appendChild(loadButton);
            savedPositionsContainer.appendChild(li);
        });
    });

    socket.emit("request_positions");
});
