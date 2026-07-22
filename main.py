from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.core.text import Label as CoreLabel
from kivy.clock import Clock
import random

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        
        # Game variables
        self.score = 0
        self.speed = 20
        
        # Schedule the main game loop at 60 FPS
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_size(self, *args):
        # Initialize positions based on actual screen size when window opens
        self.player_size = self.width // 6
        self.player_pos = [self.width // 2 - self.player_size // 2, 50]
        
        self.target_size = self.width // 10
        self.target_pos = [random.randint(0, self.width - self.target_size), self.height]

    def on_touch_move(self, touch):
        # Move player with touch/drag anywhere on screen
        self.player_pos[0] = touch.x - (self.player_size // 2)

    def on_touch_down(self, touch):
        # Allow instant tap-to-position movement
        self.player_pos[0] = touch.x - (self.player_size // 2)

    def update(self, dt):
        # Target movement logic
        self.target_pos[1] -= self.speed
        
        # Reset target if it falls past the bottom
        if self.target_pos[1] < 0:
            self.target_pos = [random.randint(0, self.width - self.target_size), self.height]
            self.score -= 1

        # Simple bounding box collision detection
        player_x, player_y = self.player_pos
        target_x, target_y = self.target_pos
        
        if (player_x < target_x + self.target_size and
            player_x + self.player_size > target_x and
            player_y < target_y + self.target_size and
            player_y + self.player_size > target_y):
            self.score += 1
            self.target_pos = [random.randint(0, self.width - self.target_size), self.height]
            self.speed += 0.2

        # Redraw everything
        self.canvas.clear()
        with self.canvas:
            # Background (White)
            Color(1, 1, 1, 1)
            Rectangle(pos=(0, 0), size=(self.width, self.height))

            # Player (Blue Box)
            Color(0.2, 0.2, 1, 1)
            Rectangle(pos=(self.player_pos[0], self.player_pos[1]), size=(self.player_size, self.player_size))

            # Target (Red Circle/Ellipse)
            Color(1, 0.2, 0.2, 1)
            Ellipse(pos=(self.target_pos[0], self.target_pos[1]), size=(self.target_size, self.target_size))

class CatchTheBallApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    CatchTheBallApp().run()
