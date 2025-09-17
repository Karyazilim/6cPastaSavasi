# Keep this directory in version control
# This directory contains placeholders for game assets

## Expected Asset Structure:
```
assets/
├── fonts/
│   └── PressStart2P.ttf  # Retro pixel font (fallback to system font if not available)
├── sounds/
│   ├── throw.wav         # Pastry throwing sound
│   ├── hit.wav           # Hit sound effect
│   ├── menu_select.wav   # Menu selection sound
│   └── background.ogg    # Background music
└── sprites/
    ├── player.png        # Player sprite sheets
    ├── ai.png           # AI opponent sprites
    ├── pastries.png     # Various pastry projectiles
    └── arena.png        # Arena background elements
```

## Notes:
- All assets should be in appropriate formats for pygame
- Sounds should be short and looped where appropriate
- Sprites should be designed for pixel art style
- Color palette should match the game's retro aesthetic (#5C946E, #FFD700, etc.)