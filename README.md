# 6C Sınıfı - Pasta Savaşı

Retro-style arcade game where players engage in epic pastry battles! Throw cakes, cupcakes, and other delicious projectiles in fast-paced classroom combat.

## 🎮 Game Overview

**Pasta Savaşı** (Cake/Pastry Battle) is a 2D arcade-style arena game inspired by classic pixel art aesthetics. Players face off against AI opponents (or future multiplayer) in intense pastry-throwing combat, featuring:

- **Retro pixel art style** with authentic 8-bit inspired visuals
- **Classroom theme** perfect for educational gaming
- **Fast-paced arcade action** with simple but engaging mechanics
- **Configurable AI difficulty** from easy to challenging
- **Responsive controls** supporting both keyboard and planned gamepad input

## 🖼️ Visual Design

The game's visual design is inspired by retro arcade games and features:
- **Color palette**: Forest green background (#5C946E), gold highlights (#FFD700), and vibrant button colors
- **Typography**: Pixel-perfect font styling reminiscent of classic arcade games
- **UI Elements**: Buttons with authentic pixel shadows and hover effects
- **Character design**: Simple geometric shapes with clear visual distinction

*Design reference available in `web/mockup/index.html`*

## 📋 System Requirements

- **Python**: 3.11 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 100+ MB RAM
- **Storage**: 50+ MB available space
- **Display**: 800x600 minimum resolution

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Karyazilim/6cPastaSavasi.git
   cd 6cPastaSavasi
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python main.py
   ```

## 🎯 How to Play

### Controls

**Player Movement:**
- **Arrow Keys** or **WASD**: Move your character
- **Spacebar**: Throw pastry projectile toward mouse cursor
- **ESC**: Pause game / Return to menu
- **F11**: Toggle fullscreen

**Menu Navigation:**
- **Up/Down Arrow Keys**: Navigate menu options
- **Enter**: Select menu option
- **ESC**: Go back / Exit

### Gameplay

1. **Objective**: Reduce your opponent's health to zero by hitting them with pastry projectiles
2. **Movement**: Use arrow keys to move around the arena
3. **Combat**: Aim with your mouse and press Spacebar to throw pastries
4. **Health**: Monitor your health bar (top-left) and opponent's health (top-right)
5. **Strategy**: Use movement to dodge incoming projectiles while aiming your own shots

### Game Modes

- **Single Player**: Battle against AI opponent with configurable difficulty
- *Future: Local multiplayer, online battles, tournament mode*

## ⚙️ Command Line Options

```bash
python main.py [options]
```

### Available Options:

- `--fullscreen`: Launch in fullscreen mode
- `--windowed WIDTHxHEIGHT`: Launch in windowed mode with custom resolution (e.g., `--windowed 800x600`)
- `--ai DIFFICULTY`: Set AI difficulty level
  - `easy`: Slower movement, longer cooldowns, delayed reactions
  - `normal`: Balanced gameplay (default)
  - `hard`: Fast movement, quick reactions, aggressive tactics
- `--seed SEED`: Set random seed for deterministic gameplay (useful for testing)
- `--version`: Display version information
- `--help`: Show detailed help message

### Examples:

```bash
# Launch with default settings
python main.py

# Launch in fullscreen with hard AI
python main.py --fullscreen --ai hard

# Launch in custom window size with easy AI
python main.py --windowed 1280x720 --ai easy

# Launch with deterministic random seed
python main.py --seed 42
```

## 🏗️ Project Structure

```
6cPastaSavasi/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── main.py                  # Main entry point
├── src/                     # Source code
│   └── game/               # Game package
│       ├── __init__.py     # Package initialization
│       ├── constants.py    # Game constants and configuration
│       ├── entities.py     # Player, AI, and projectile classes
│       ├── game.py         # Main game loop and state management
│       └── ui.py           # UI components and menu systems
├── assets/                  # Game assets (fonts, sounds, sprites)
│   ├── README.md           # Asset documentation
│   └── .gitkeep           # Keep directory in version control
└── web/                    # Design references
    └── mockup/             
        └── index.html      # HTML design mockup reference
```

## 🎨 Asset Information

The game currently uses placeholder graphics (colored rectangles and circles) for all visual elements. The asset system is designed to support:

### Planned Asset Types:
- **Fonts**: Press Start 2P or similar pixel fonts
- **Sprites**: Character animations, projectile graphics, UI elements
- **Sounds**: Throwing sounds, hit effects, background music
- **Backgrounds**: Arena themes, classroom decorations

*See `assets/README.md` for detailed asset specifications.*

## 🔧 Development

### Code Style
- **Type hints** for better code documentation
- **Docstrings** for all public functions and classes  
- **Modular design** for easy feature expansion
- **Constants** centralized in `constants.py`
- **< 60 lines** per function where possible

### Key Components

1. **State Management**: Clean separation between menu, game, settings, and game-over states
2. **Entity System**: Modular character and projectile classes with inheritance
3. **UI Framework**: Reusable button and menu components with retro styling
4. **Input Handling**: Unified system supporting keyboard and future gamepad input
5. **Collision Detection**: Efficient rectangle-based collision system

### Adding Features

The codebase is structured for easy expansion:
- **New projectile types**: Extend `Projectile` class in `entities.py`
- **Additional arenas**: Modify drawing functions in `game.py`
- **Power-ups**: Add new entity types and collision handling
- **Multiplayer**: Extend input handling and add network layer

## 🗺️ Roadmap

### Phase 1: Core Game ✅
- [x] Basic gameplay mechanics
- [x] Single player vs AI
- [x] Retro-styled UI
- [x] Settings and difficulty options
- [x] Command-line configuration

### Phase 2: Content Expansion 🚧
- [ ] Multiple pastry types with different properties
- [ ] Power-ups (Speed Boost, Shield, Mega Pastry)
- [ ] Multiple arena maps
- [ ] Animated sprites and particle effects
- [ ] Sound effects and background music

### Phase 3: Multiplayer 📋
- [ ] Local 2-player mode
- [ ] Online multiplayer support
- [ ] Tournament and ranking systems
- [ ] Spectator mode

### Phase 4: Polish 📋
- [ ] Advanced AI with machine learning
- [ ] Story mode with progression
- [ ] Achievement system
- [ ] Steam integration

## 🤝 Contributing

We welcome contributions! Whether it's:
- 🐛 Bug reports and fixes
- ✨ New features and enhancements  
- 🎨 Art assets and animations
- 🎵 Sound effects and music
- 📖 Documentation improvements

Please feel free to submit issues and pull requests.

## 📄 License

[Add license information here]

## 👥 Credits

- **Game Design**: Inspired by classic arcade pastry battle concepts
- **Visual Design**: Based on retro pixel art aesthetics and the provided HTML mockup
- **Development**: Built with Python and Pygame

## 🐛 Troubleshooting

### Common Issues:

**Game won't start:**
- Ensure Python 3.11+ is installed
- Check that pygame is properly installed: `pip install pygame`
- Verify all files are present in the project directory

**Performance issues:**
- Try windowed mode instead of fullscreen
- Close other applications to free up memory
- Check that your graphics drivers are up to date

**Controls not responsive:**
- Ensure the game window has focus
- Try restarting the game
- Check if other applications are capturing input

**Audio problems:**
- Verify system audio is working
- Check volume settings in the game's settings menu
- Ensure no other applications are using audio exclusively

### Getting Help:

If you encounter issues not covered here:
1. Check the [Issues](https://github.com/Karyazilim/6cPastaSavasi/issues) page for existing reports
2. Create a new issue with detailed information about your problem
3. Include your operating system, Python version, and any error messages

---

**Have fun battling with pastries! 🧁⚔️🍰**