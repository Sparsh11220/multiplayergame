const socket = io("https://your-backend-url.onrender.com");  // Replace with Render URL

document.getElementById("createGame").addEventListener("click", () => {
    socket.emit("create_game");
});

document.getElementById("joinGame").addEventListener("click", () => {
    let gameCode = document.getElementById("gameCode").value;
    let playerName = prompt("Enter your name:");
    if (gameCode && playerName) {
        socket.emit("join_game", { game_code: gameCode, player_name: playerName });
    }
});

socket.on("game_created", (data) => {
    document.getElementById("gameArea").style.display = "block";
    document.getElementById("codeDisplay").innerText = data.game_code;
});

socket.on("player_joined", (data) => {
    alert(`Players: ${data.players.join(", ")}`);
});

document.getElementById("startGame").addEventListener("click", () => {
    let gameCode = document.getElementById("codeDisplay").innerText;
    socket.emit("start_game", { game_code: gameCode });
});

socket.on("game_started", () => {
    alert("Game started! Enter your number.");
});

document.getElementById("submitNumber").addEventListener("click", () => {
    let gameCode = document.getElementById("codeDisplay").innerText;
    let playerName = document.getElementById("playerName").value;
    let number = parseInt(document.getElementById("playerNumber").value);
    if (!isNaN(number)) {
        socket.emit("submit_number", { game_code: gameCode, player_name: playerName, number: number });
    }
});

socket.on("game_result", (data) => {
    document.getElementById("results").innerHTML = `
        <h3>Target: ${data.target.toFixed(2)}</h3>
        <p>Numbers: ${JSON.stringify(data.numbers)}</p>
        <h3>Winner: ${data.winner}</h3>
    `;
});
