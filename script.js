<script>
    // Connect to the server (use your actual deployed URL)
    const socket = io("https://multiplayergame-wboi.onrender.com");

    // Button click event to create a game
    document.getElementById("create-game").addEventListener("click", function() {
        console.log("Create Game button clicked!");
        socket.emit("create_game");
    });

    // Handle game creation response from the server
    socket.on("game_created", (data) => {
        console.log("Game created with ID:", data.game_id);
        alert(`Game Created! ID: ${data.game_id}`);
    });
</script>
