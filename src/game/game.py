"""
Main game loop and state management for Pasta Savaşı.
"""

import pygame
import sys
from typing import Optional, List

from .constants import *
from .ui import *
from .entities import *


class Game:
    """Main game class handling all game states and logic."""
    
    def __init__(self, fullscreen: bool = False, ai_difficulty: AIDifficulty = AIDifficulty.NORMAL):
        pygame.init()
        pygame.mixer.init()
        
        # Set up display
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            # Update screen size for fullscreen
            global SCREEN_WIDTH, SCREEN_HEIGHT
            SCREEN_WIDTH, SCREEN_HEIGHT = self.screen.get_size()
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            
        pygame.display.set_caption("6C Sınıfı - Pasta Savaşı")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        self.ai_difficulty = ai_difficulty
        
        # Load fonts
        self.font_large = load_font(FONT_SIZE_LARGE)
        self.font_medium = load_font(FONT_SIZE_MEDIUM)
        self.font_small = load_font(FONT_SIZE_SMALL)
        
        # Game settings
        self.volume = 0.5
        
        # Initialize game objects
        self.player: Optional[Player] = None
        self.ai_opponent: Optional[AIOpponent] = None
        self.projectiles: List[Projectile] = []
        self.player_health_bar: Optional[HealthBar] = None
        self.ai_health_bar: Optional[HealthBar] = None
        
        # Initialize menus
        self._init_menus()
        
        # Game state
        self.winner: Optional[str] = None
        self.paused = False
        
    def _init_menus(self) -> None:
        """Initialize all menu systems."""
        # Main menu
        self.main_menu = Menu(self.font_medium)
        
        # Calculate button positions (centered)
        button_width = 200
        button_height = 60
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 2 + 100
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        # Main menu buttons
        play_button = PixelButton(
            center_x, start_y,
            button_width, button_height,
            "OYNA", ORANGE, self.font_medium,
            self._start_game
        )
        
        settings_button = PixelButton(
            center_x, start_y + button_height + button_spacing,
            button_width, button_height,
            "AYARLAR", BLUE, self.font_medium,
            self._show_settings
        )
        
        quit_button = PixelButton(
            center_x, start_y + 2 * (button_height + button_spacing),
            button_width, button_height,
            "ÇIKIŞ", RED, self.font_medium,
            self._quit_game
        )
        
        self.main_menu.add_button(play_button)
        self.main_menu.add_button(settings_button)
        self.main_menu.add_button(quit_button)
        
        # Settings menu
        self.settings_menu = Menu(self.font_medium)
        
        # Settings buttons
        difficulty_button = PixelButton(
            center_x, start_y - 50,
            button_width, button_height,
            f"ZORLUK: {self.ai_difficulty.value.upper()}", ORANGE, self.font_small,
            self._cycle_difficulty
        )
        
        volume_button = PixelButton(
            center_x, start_y + button_spacing,
            button_width, button_height,
            f"SES: {int(self.volume * 100)}%", BLUE, self.font_small,
            self._cycle_volume
        )
        
        back_button = PixelButton(
            center_x, start_y + 2 * (button_height + button_spacing),
            button_width, button_height,
            "GERİ", RED, self.font_medium,
            self._show_main_menu
        )
        
        self.settings_menu.add_button(difficulty_button)
        self.settings_menu.add_button(volume_button)
        self.settings_menu.add_button(back_button)
        
        # Game over menu
        self.game_over_menu = Menu(self.font_medium)
        
        restart_button = PixelButton(
            center_x, start_y,
            button_width, button_height,
            "YENİDEN OYNA", ORANGE, self.font_medium,
            self._restart_game
        )
        
        menu_button = PixelButton(
            center_x, start_y + button_height + button_spacing,
            button_width, button_height,
            "MENÜ", BLUE, self.font_medium,
            self._show_main_menu
        )
        
        self.game_over_menu.add_button(restart_button)
        self.game_over_menu.add_button(menu_button)
    
    def _start_game(self) -> None:
        """Start a new game."""
        self.state = GameState.PLAYING
        self.paused = False
        
        # Initialize player and AI
        self.player = Player(100, SCREEN_HEIGHT // 2)
        self.ai_opponent = AIOpponent(SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2, self.ai_difficulty)
        self.projectiles = []
        
        # Initialize health bars
        self.player_health_bar = HealthBar(20, 20, 200, 20, PLAYER_MAX_HEALTH)
        self.ai_health_bar = HealthBar(SCREEN_WIDTH - 220, 20, 200, 20, PLAYER_MAX_HEALTH)
        
        self.winner = None
    
    def _show_settings(self) -> None:
        """Show settings menu."""
        self.state = GameState.SETTINGS
        
    def _show_main_menu(self) -> None:
        """Show main menu."""
        self.state = GameState.MENU
        
    def _quit_game(self) -> None:
        """Quit the game."""
        self.state = GameState.QUIT
        
    def _cycle_difficulty(self) -> None:
        """Cycle through AI difficulty levels."""
        difficulties = list(AIDifficulty)
        current_index = difficulties.index(self.ai_difficulty)
        self.ai_difficulty = difficulties[(current_index + 1) % len(difficulties)]
        
        # Update button text
        self.settings_menu.buttons[0].text = f"ZORLUK: {self.ai_difficulty.value.upper()}"
        
    def _cycle_volume(self) -> None:
        """Cycle through volume levels."""
        volumes = [0.0, 0.25, 0.5, 0.75, 1.0]
        current_index = volumes.index(self.volume) if self.volume in volumes else 2
        self.volume = volumes[(current_index + 1) % len(volumes)]
        
        # Update button text
        self.settings_menu.buttons[1].text = f"SES: {int(self.volume * 100)}%"
        
        # Apply volume (when we have sounds)
        pygame.mixer.music.set_volume(self.volume)
        
    def _restart_game(self) -> None:
        """Restart the current game."""
        self._start_game()
        
    def handle_events(self) -> None:
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.paused = not self.paused
                    elif self.state == GameState.SETTINGS:
                        self._show_main_menu()
                    elif self.state == GameState.GAME_OVER:
                        self._show_main_menu()
                elif event.key == pygame.K_F11:
                    # Toggle fullscreen
                    pygame.display.toggle_fullscreen()
                    
                # Handle space for throwing in game
                elif event.key == pygame.K_SPACE and self.state == GameState.PLAYING and not self.paused:
                    if self.player and self.player.can_throw():
                        mouse_pos = pygame.mouse.get_pos()
                        projectile = self.player.throw_at_mouse(mouse_pos)
                        if projectile:
                            self.projectiles.append(projectile)
            
            # Handle menu events
            if self.state == GameState.MENU:
                self.main_menu.handle_event(event)
            elif self.state == GameState.SETTINGS:
                self.settings_menu.handle_event(event)
            elif self.state == GameState.GAME_OVER:
                self.game_over_menu.handle_event(event)
    
    def update(self, dt: float) -> None:
        """Update game logic."""
        if self.state == GameState.PLAYING and not self.paused:
            # Update player
            if self.player:
                keys = pygame.key.get_pressed()
                self.player.handle_input(keys, dt)
                self.player.update(dt)
                
            # Update AI
            if self.ai_opponent and self.player:
                ai_projectile = self.ai_opponent.update_ai(self.player, dt)
                if ai_projectile:
                    self.projectiles.append(ai_projectile)
                self.ai_opponent.update(dt)
                
            # Update projectiles
            self.projectiles = [p for p in self.projectiles if p.update(dt)]
            
            # Check collisions
            self._check_collisions()
            
            # Update health bars
            if self.player_health_bar and self.player:
                self.player_health_bar.set_health(self.player.health)
            if self.ai_health_bar and self.ai_opponent:
                self.ai_health_bar.set_health(self.ai_opponent.health)
                
            # Check win condition
            if self.player and self.player.health <= 0:
                self.winner = "AI KAZANDI!"
                self.state = GameState.GAME_OVER
            elif self.ai_opponent and self.ai_opponent.health <= 0:
                self.winner = "OYUNCU KAZANDI!"
                self.state = GameState.GAME_OVER
    
    def _check_collisions(self) -> None:
        """Check collisions between projectiles and characters."""
        for projectile in self.projectiles[:]:  # Copy list to allow modification
            hit = False
            
            # Check collision with player
            if (projectile.owner_type != EntityType.PLAYER and 
                self.player and projectile.rect.colliderect(self.player.rect)):
                self.player.take_damage(projectile.damage)
                hit = True
                
            # Check collision with AI
            elif (projectile.owner_type != EntityType.AI and 
                  self.ai_opponent and projectile.rect.colliderect(self.ai_opponent.rect)):
                self.ai_opponent.take_damage(projectile.damage)
                hit = True
                
            if hit:
                self.projectiles.remove(projectile)
    
    def draw(self) -> None:
        """Draw everything on screen."""
        self.screen.fill(BACKGROUND_COLOR)
        
        if self.state == GameState.MENU:
            self._draw_main_menu()
        elif self.state == GameState.SETTINGS:
            self._draw_settings_menu()
        elif self.state == GameState.PLAYING:
            self._draw_game()
        elif self.state == GameState.GAME_OVER:
            self._draw_game_over()
            
        pygame.display.flip()
    
    def _draw_main_menu(self) -> None:
        """Draw the main menu."""
        # Title
        title_text = "6C Sınıfı"
        subtitle_text = "Pasta Savaşı"
        
        # Draw title with shadow
        title_pos = (SCREEN_WIDTH // 2 - self.font_large.size(title_text)[0] // 2, 150)
        draw_text_with_shadow(self.screen, title_text, self.font_large, title_pos, WHITE, BLACK, (4, 4))
        
        # Draw subtitle with shadow
        subtitle_pos = (SCREEN_WIDTH // 2 - self.font_medium.size(subtitle_text)[0] // 2, 220)
        draw_text_with_shadow(self.screen, subtitle_text, self.font_medium, subtitle_pos, GOLD, BLACK, (3, 3))
        
        # Draw menu buttons
        self.main_menu.draw(self.screen)
        
        # Version info
        version_text = "v1.0.0"
        version_pos = (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 30)
        version_surface = self.font_small.render(version_text, False, (255, 255, 255, 128))
        self.screen.blit(version_surface, version_pos)
    
    def _draw_settings_menu(self) -> None:
        """Draw the settings menu."""
        # Title
        title_text = "AYARLAR"
        title_pos = (SCREEN_WIDTH // 2 - self.font_large.size(title_text)[0] // 2, 150)
        draw_text_with_shadow(self.screen, title_text, self.font_large, title_pos, WHITE, BLACK, (4, 4))
        
        # Draw settings buttons
        self.settings_menu.draw(self.screen)
    
    def _draw_game(self) -> None:
        """Draw the game state."""
        # Draw entities
        if self.player:
            self.player.draw(self.screen)
        if self.ai_opponent:
            self.ai_opponent.draw(self.screen)
            
        for projectile in self.projectiles:
            projectile.draw(self.screen)
            
        # Draw UI
        if self.player_health_bar:
            self.player_health_bar.draw(self.screen)
        if self.ai_health_bar:
            self.ai_health_bar.draw(self.screen)
            
        # Draw health labels
        player_label = "OYUNCU"
        ai_label = "RAKIP"
        label_pos_player = (20, 50)
        label_pos_ai = (SCREEN_WIDTH - 220, 50)
        
        self.screen.blit(self.font_small.render(player_label, False, WHITE), label_pos_player)
        self.screen.blit(self.font_small.render(ai_label, False, WHITE), label_pos_ai)
        
        # Draw pause overlay if paused
        if self.paused:
            pause_text = "DURAKLADI - ESC ile devam"
            pause_size = self.font_medium.size(pause_text)
            pause_pos = ((SCREEN_WIDTH - pause_size[0]) // 2, (SCREEN_HEIGHT - pause_size[1]) // 2)
            
            # Semi-transparent background
            pause_bg = pygame.Surface((pause_size[0] + 40, pause_size[1] + 20))
            pause_bg.fill(BLACK)
            pause_bg.set_alpha(180)
            self.screen.blit(pause_bg, (pause_pos[0] - 20, pause_pos[1] - 10))
            
            draw_text_with_shadow(self.screen, pause_text, self.font_medium, pause_pos, WHITE, BLACK)
    
    def _draw_game_over(self) -> None:
        """Draw the game over screen."""
        # Draw game background first
        self._draw_game()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Winner announcement
        if self.winner:
            winner_size = self.font_large.size(self.winner)
            winner_pos = ((SCREEN_WIDTH - winner_size[0]) // 2, 200)
            draw_text_with_shadow(self.screen, self.winner, self.font_large, winner_pos, GOLD, BLACK, (4, 4))
        
        # Draw game over menu
        self.game_over_menu.draw(self.screen)
    
    def run(self) -> None:
        """Main game loop."""
        while self.running and self.state != GameState.QUIT:
            dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
            
        # Clean shutdown
        pygame.mixer.quit()
        pygame.quit()