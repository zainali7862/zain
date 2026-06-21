# Game Configuration

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Level settings
LEVEL_MAX = 80
INITIAL_ENEMIES = 3
ENEMIES_PER_WAVE_INCREMENT = 2
WAVE_INCREMENT_INTERVAL = 5

# Player settings
PLAYER_START_HEALTH = 100
PLAYER_SPEED = 5
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 50

# Weapon settings
WEAPON_SETTINGS = {
    "PISTOL": {
        "damage": 10,
        "fire_rate": 10,
        "max_ammo": 30,
        "bullet_speed": 7,
        "spread_angle": 0,
    },
    "RIFLE": {
        "damage": 20,
        "fire_rate": 5,
        "max_ammo": 60,
        "bullet_speed": 8,
        "spread_angle": 15,
    },
    "SHOTGUN": {
        "damage": 15,
        "fire_rate": 20,
        "max_ammo": 24,
        "bullet_speed": 6,
        "spread_angle": 45,
    },
    "SNIPER": {
        "damage": 50,
        "fire_rate": 40,
        "max_ammo": 12,
        "bullet_speed": 10,
        "spread_angle": 0,
    },
}

# Enemy settings
ENEMY_TYPES = {
    "BASIC": {
        "width": 30,
        "height": 30,
        "health_base": 20,
        "speed_base": 2,
        "damage_base": 5,
    },
    "FAST": {
        "width": 25,
        "height": 25,
        "health_base": 15,
        "speed_base": 4,
        "damage_base": 3,
    },
    "TANKY": {
        "width": 40,
        "height": 40,
        "health_base": 40,
        "speed_base": 1,
        "damage_base": 8,
    },
}

# Scoring
BASE_SCORE_PER_ENEMY = 100
SCORE_LEVEL_MULTIPLIER = 10

# Colors
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "CYAN": (0, 255, 255),
    "ORANGE": (255, 165, 0),
    "PURPLE": (128, 0, 128),
}
