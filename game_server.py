# game_server.py

import asyncio
import websockets
import json
import random

PORT = 8765
BOARD_SIZE = 30

game_state = {
    "players": [],
    "fruit": {"x": 10, "y": 10},
}

def new_snake():
    return [{"x": 5, "y": 5}, {"x": 4, "y": 5}]

class GameServer:
    def __init__(self):
        self.clients = []

    async def start(self):
        print(f"🟢 WebSocket сервер запущен на порту {PORT}")
        async with websockets.serve(self.handler, "0.0.0.0", PORT):
            while True:
                await self.game_loop()
                await asyncio.sleep(0.15)

    async def handler(self, websocket):
        player = {"ws": websocket, "snake": new_snake(), "dir": {"x": 1, "y": 0}}
        game_state["players"].append(player)
        try:
            async for msg in websocket:
                data = json.loads(msg)
                if data["type"] == "dir":
                    player["dir"] = data["dir"]
        except:
            pass
        finally:
            game_state["players"].remove(player)

    async def game_loop(self):
        for player in game_state["players"]:
            dx = player["dir"]["x"]
            dy = player["dir"]["y"]
            head = {
                "x": (player["snake"][0]["x"] + dx) % BOARD_SIZE,
                "y": (player["snake"][0]["y"] + dy) % BOARD_SIZE
            }
            player["snake"].insert(0, head)
            if head["x"] == game_state["fruit"]["x"] and head["y"] == game_state["fruit"]["y"]:
                game_state["fruit"] = {
                    "x": random.randint(0, BOARD_SIZE - 1),
                    "y": random.randint(0, BOARD_SIZE - 1)
                }
            else:
                player["snake"].pop()

        # отправка обновлений
        for player in game_state["players"]:
            try:
                await player["ws"].send(json.dumps({
                    "type": "update",
                    "players": [p["snake"] for p in game_state["players"]],
                    "fruit": game_state["fruit"]
                }))
            except:
                pass
