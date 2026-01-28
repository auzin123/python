import arcade
import config
from bird import Bird
from game import GameView

if __name__ == "__main__":
    window = arcade.Window(fullscreen=True)
    window.set_update_rate(1/config.FPS)
    view = GameView()
    window.show_view(view)
    arcade.run()