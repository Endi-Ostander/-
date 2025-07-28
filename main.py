# main.py

import asyncio
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang import Builder
from game_server import GameServer
import threading

class SnakeWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30.0)

    def update(self, dt):
        self.canvas.clear()
        self.draw_snakes()
        self.draw_fruit()

    def draw_snakes(self):
        from game_server import game_state
        with self.canvas:
            for player in game_state["players"]:
                for segment in player["snake"]:
                    self.draw_cell(segment["x"], segment["y"], color=(0, 1, 0, 1))

    def draw_fruit(self):
        from game_server import game_state
        fruit = game_state["fruit"]
        self.draw_cell(fruit["x"], fruit["y"], color=(1, 1, 0, 1))

    def draw_cell(self, x, y, color):
        from kivy.graphics import Color, Rectangle
        cell_size = 20
        Color(*color)
        Rectangle(pos=(x * cell_size, y * cell_size), size=(cell_size, cell_size))

class SnakeApp(App):
    def build(self):
        Builder.load_file("ui.kv")
        threading.Thread(target=self.start_server, daemon=True).start()
        return SnakeWidget()

    def start_server(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(GameServer().start())

if __name__ == "__main__":
    SnakeApp().run()
