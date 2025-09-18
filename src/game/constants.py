"""
Game constants and configuration for Pasta Savaşı.
"""

from enum import Enum
from typing import Tuple

# Screen settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors (inspired by HTML mockup)
BACKGROUND_COLOR = (92, 148, 110)  # #5C946E
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)  # #FFD700
ORANGE = (244, 141, 37)  # #F48D25
BLUE = (74, 122, 140)  # #4A7A8C
RED = (168, 74, 74)  # #A84A4A

# Game states
class GameState(Enum):
    MENU = "menu"
    SETTINGS = "settings"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    QUIT = "quit"

# Player settings
PLAYER_SPEED = 300  # pixels per second
PLAYER_SIZE = 40
PLAYER_MAX_HEALTH = 100

# AI settings
class AIDifficulty(Enum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"

AI_SETTINGS = {
    AIDifficulty.EASY: {
        "speed": 150,
        "throw_cooldown": 2.0,
        "reaction_time": 1.0
    },
    AIDifficulty.NORMAL: {
        "speed": 200,
        "throw_cooldown": 1.5,
        "reaction_time": 0.7
    },
    AIDifficulty.HARD: {
        "speed": 250,
        "throw_cooldown": 1.0,
        "reaction_time": 0.4
    }
}

# Projectile settings
PROJECTILE_SPEED = 400
PROJECTILE_SIZE = 15
PROJECTILE_DAMAGE = 20
PROJECTILE_LIFETIME = 3.0  # seconds

# UI settings
BUTTON_PADDING = 12
BUTTON_BORDER = 4
SHADOW_OFFSET = 4
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 16

# Input settings
KEYS_PLAYER1 = {
    "up": "up",
    "down": "down", 
    "left": "left",
    "right": "right",
    "throw": "space"
}

KEYS_PLAYER2 = {
    "up": "w",
    "down": "s",
    "left": "a", 
    "right": "d",
    "throw": "f"
}

# Physics
FRICTION = 0.8