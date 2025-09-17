#!/usr/bin/env python3
"""
Main entry point for Pasta Savaşı (Cake/Pastry Battle) game.

6C Sınıfı - Pasta Savaşı
A retro-style arcade game where players throw pastries at each other in classroom combat.

Usage:
    python main.py [options]
    
Options:
    --fullscreen         Launch in fullscreen mode
    --windowed WIDTHxHEIGHT    Launch in windowed mode with specified resolution
    --ai DIFFICULTY      Set AI difficulty (easy|normal|hard)
    --seed SEED          Set random seed for deterministic gameplay (for testing)
    --help              Show this help message
"""

import sys
import argparse
import random
from typing import Tuple, Optional

# Add src to path for imports
sys.path.insert(0, 'src')

from game.game import Game
from game.constants import AIDifficulty, SCREEN_WIDTH, SCREEN_HEIGHT


def parse_resolution(resolution_str: str) -> Tuple[int, int]:
    """Parse resolution string like '1024x768' into (width, height) tuple."""
    try:
        width, height = resolution_str.split('x')
        return int(width), int(height)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid resolution format: {resolution_str}. Use WIDTHxHEIGHT (e.g., 1024x768)")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="6C Sınıfı - Pasta Savaşı: Retro arcade pastry battle game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py                          # Launch with default settings
    python main.py --fullscreen            # Launch in fullscreen
    python main.py --windowed 800x600      # Launch in 800x600 window
    python main.py --ai hard               # Launch with hard AI difficulty
    python main.py --seed 42               # Launch with deterministic random seed
        """
    )
    
    # Display options
    display_group = parser.add_mutually_exclusive_group()
    display_group.add_argument(
        '--fullscreen',
        action='store_true',
        help='Launch the game in fullscreen mode'
    )
    display_group.add_argument(
        '--windowed',
        type=parse_resolution,
        metavar='WIDTHxHEIGHT',
        help='Launch in windowed mode with specified resolution (e.g., 1024x768)'
    )
    
    # AI difficulty
    parser.add_argument(
        '--ai',
        choices=['easy', 'normal', 'hard'],
        default='normal',
        help='Set AI opponent difficulty (default: normal)'
    )
    
    # Random seed for testing
    parser.add_argument(
        '--seed',
        type=int,
        help='Set random seed for deterministic gameplay (useful for testing)'
    )
    
    # Version
    parser.add_argument(
        '--version',
        action='version',
        version='6C Sınıfı - Pasta Savaşı v1.0.0'
    )
    
    return parser.parse_args()


def setup_resolution(args: argparse.Namespace) -> None:
    """Set up screen resolution based on command line arguments."""
    if args.windowed:
        global SCREEN_WIDTH, SCREEN_HEIGHT
        # Import and modify constants
        import game.constants as constants
        constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT = args.windowed
        print(f"Setting windowed resolution to {args.windowed[0]}x{args.windowed[1]}")


def main() -> None:
    """Main entry point."""
    try:
        # Parse command line arguments
        args = parse_args()
        
        # Set random seed if provided
        if args.seed is not None:
            random.seed(args.seed)
            print(f"Using random seed: {args.seed}")
        
        # Setup resolution
        setup_resolution(args)
        
        # Convert AI difficulty string to enum
        ai_difficulty_map = {
            'easy': AIDifficulty.EASY,
            'normal': AIDifficulty.NORMAL,
            'hard': AIDifficulty.HARD
        }
        ai_difficulty = ai_difficulty_map[args.ai]
        
        print("Starting 6C Sınıfı - Pasta Savaşı...")
        print(f"AI Difficulty: {args.ai}")
        
        if args.fullscreen:
            print("Launching in fullscreen mode")
        elif args.windowed:
            print(f"Launching in windowed mode: {args.windowed[0]}x{args.windowed[1]}")
        else:
            print(f"Launching in default windowed mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        
        # Create and run the game
        game = Game(fullscreen=args.fullscreen, ai_difficulty=ai_difficulty)
        game.run()
        
        print("Game ended normally.")
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()