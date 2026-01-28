import arcade
import random

class Game(arcade.Window):
    def __init__(self):
        super().__init__(fullscreen=True)
        self.text = "2026"
        self.snow_list = arcade.SpriteList()
        self.speed = 2 
        
        self.colors = [
            arcade.color.WHITE, 
            arcade.color.RED, 
            arcade.color.GOLD, 
            arcade.color.CYAN, 
            arcade.color.GREEN_YELLOW
        ]
        self.current_color = arcade.color.WHITE
        self.color_timer = 0

        current_y = 0
        while current_y < self.height:
            self.add_snow_row(current_y)
            current_y += self.snow_list[-1].height

    def add_snow_row(self, y_position):
        half_width = self.width // 2
        
        snow_left = arcade.Sprite("snow.png")
        snow_left.width = half_width
        snow_left.left = 0
        snow_left.bottom = y_position
        snow_left.alpha = random.randint(150, 255)
        
        snow_right = arcade.Sprite("snow.png")
        snow_right.width = half_width
        snow_right.left = half_width
        snow_right.bottom = y_position
        snow_right.alpha = snow_left.alpha
        
        self.snow_list.append(snow_left)
        self.snow_list.append(snow_right)

    def on_draw(self):
        self.clear()
        self.snow_list.draw()
        arcade.draw_text(
            self.text, self.width // 2, self.height // 2,
            self.current_color, font_size=100,
            anchor_x="center", anchor_y="center"
        )

    def on_update(self, delta_time):
        self.color_timer += delta_time
        if self.color_timer >= 1.0:
            self.current_color = random.choice(self.colors)
            self.color_timer = 0

        for snow in self.snow_list:
            snow.center_y -= self.speed

        if self.snow_list[-1].top <= self.height:
            self.add_snow_row(self.snow_list[-1].top)

        if len(self.snow_list) > 0 and self.snow_list[0].top < 0:
            self.snow_list.pop(0)
            self.snow_list.pop(0)

if __name__ == "__main__":
    Game()
    arcade.run()