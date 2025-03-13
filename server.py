from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import socketio

# Create FastAPI app
app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Create Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(sio, app)

# Game logic
games = {}

class Game:
    def __init__(self, game_id):
        self.id = game_id
        self.players = {}  # {sid: {"name": "Player1", "number": None}}
        self.started = False

    def add_player(self, sid, name):
        if self.started or len(self.players) >= 5:
            return False
        self.players[sid] = {"name": name, "number": None}
        return True

    def submit_number(self, sid, number):
        if sid in self.players:
            self.players[sid]["number"] = number
            return True
        return False

    def all_submitted(self):
        return all(player["number"] is not None for player in self.players.values())

    def calculate_winner(self):
        numbers = [p["number"] for p in self.players.values()]
        avg = sum(numbers) / len(numbers)
        target = avg * 0.8

        closest_player = min(
            self.players.items(),
            key=lambda p: abs(p[1]["number"] - target),
        )
        return {"target": target, "winner": closest_player[1]["name"], "players": self.players}

# Socket.IO Events
@sio.event
async def connect(sid, environ):
    print(f"Player {sid} connected")

@sio.event
async def create_game(sid):
    game_id = str(len(games) + 1)
    games[game_id] = Game(game_id)
    await sio.emit("game_created", {"game_id": game_id}, room=sid)

@sio.event
async def join_game(sid, data):
    game_id, name = data["game_id"], data["name"]
    if game_id in games and games[game_id].add_player(sid, name):
        await sio.enter_room(sid, game_id)
        await sio.emit("player_joined", {"name": name}, room=game_id)
    else:
        await sio.emit("error", {"message": "Game full or started"}, room=sid)

@sio.event
async def submit_number(sid, data):
    game_id, number = data["game_id"], data["number"]
    if game_id in games and games[game_id].submit_number(sid, number):
        if games[game_id].all_submitted():
            result = games[game_id].calculate_winner()
            await sio.emit("game_results", result, room=game_id)
    else:
        await sio.emit("error", {"message": "Invalid submission"}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"Player {sid} disconnected")

# Run ASGI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(sio_app, host="0.0.0.0", port=8000)


