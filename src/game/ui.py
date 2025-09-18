"""
UI components for Pasta Savaşı game.
Implements retro pixel-style interface inspired by the HTML mockup.
"""

import pygame
from typing import Callable, Optional, List, Tuple
from enum import Enum

from .constants import *


class ButtonState(Enum):
    NORMAL = "normal"
    HOVER = "hover"
    PRESSED = "pressed"


class PixelButton:
    """
    Retro pixel-style button with shadow effects matching HTML mockup design.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 color: Tuple[int, int, int], font: pygame.font.Font,
                 callback: Optional[Callable] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = font
        self.callback = callback
        self.state = ButtonState.NORMAL
        self.enabled = True
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse and keyboard events. Returns True if button was clicked."""
        if not self.enabled:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.state = ButtonState.PRESSED
                return False
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.state == ButtonState.PRESSED:
                if self.rect.collidepoint(event.pos):
                    if self.callback:
                        self.callback()
                    self.state = ButtonState.HOVER
                    return True
                else:
                    self.state = ButtonState.NORMAL
                    
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if self.state != ButtonState.PRESSED:
                    self.state = ButtonState.HOVER
            else:
                if self.state != ButtonState.PRESSED:
                    self.state = ButtonState.NORMAL
                    
        return False
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button with pixel-perfect shadow effects."""
        if not self.enabled:
            return
            
        # Calculate offset based on state (matching HTML behavior)
        offset_x = 0
        offset_y = 0
        shadow_offset = SHADOW_OFFSET
        
        if self.state == ButtonState.HOVER:
            offset_x = 2
            offset_y = 2
            shadow_offset = 2
        elif self.state == ButtonState.PRESSED:
            offset_x = 4
            offset_y = 4
            shadow_offset = 0
            
        # Draw shadow
        if shadow_offset > 0:
            shadow_rect = pygame.Rect(
                self.rect.x + shadow_offset,
                self.rect.y + shadow_offset,
                self.rect.width,
                self.rect.height
            )
            pygame.draw.rect(screen, BLACK, shadow_rect)
            
        # Draw button background
        button_rect = pygame.Rect(
            self.rect.x + offset_x,
            self.rect.y + offset_y,
            self.rect.width,
            self.rect.height
        )
        pygame.draw.rect(screen, self.color, button_rect)
        
        # Draw border
        pygame.draw.rect(screen, BLACK, button_rect, BUTTON_BORDER)
        
        # Draw text with shadow
        text_surface = self.font.render(self.text, False, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        
        # Text shadow
        shadow_text_rect = text_rect.copy()
        shadow_text_rect.x += 2
        shadow_text_rect.y += 2
        shadow_text_surface = self.font.render(self.text, False, BLACK)
        screen.blit(shadow_text_surface, shadow_text_rect)
        
        # Main text
        screen.blit(text_surface, text_rect)


class Menu:
    """Base menu class with keyboard navigation support."""
    
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.buttons: List[PixelButton] = []
        self.selected_index = 0
        
    def add_button(self, button: PixelButton) -> None:
        """Add a button to the menu."""
        self.buttons.append(button)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for all buttons and keyboard navigation."""
        # Handle keyboard navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
                return True
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
                return True
            elif event.key == pygame.K_RETURN:
                if self.buttons[self.selected_index].callback:
                    self.buttons[self.selected_index].callback()
                return True
                
        # Handle mouse events
        for i, button in enumerate(self.buttons):
            if button.handle_event(event):
                self.selected_index = i
                return True
                
        return False
    
    def update_selection(self) -> None:
        """Update button states based on keyboard selection."""
        for i, button in enumerate(self.buttons):
            if i == self.selected_index:
                # Keyboard selection takes precedence over mouse hover
                mouse_pos = pygame.mouse.get_pos()
                if not button.rect.collidepoint(mouse_pos):
                    button.state = ButtonState.HOVER
            # Mouse hover is handled in button.handle_event()
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw all buttons."""
        self.update_selection()
        for button in self.buttons:
            button.draw(screen)


class HealthBar:
    """Health bar UI component."""
    
    def __init__(self, x: int, y: int, width: int, height: int, max_health: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_health = max_health
        self.current_health = max_health
        
    def set_health(self, health: int) -> None:
        """Set current health value."""
        self.current_health = max(0, min(health, self.max_health))
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the health bar."""
        # Background
        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Health fill
        if self.current_health > 0:
            health_ratio = self.current_health / self.max_health
            fill_width = int((self.rect.width - 4) * health_ratio)
            fill_rect = pygame.Rect(
                self.rect.x + 2,
                self.rect.y + 2,
                fill_width,
                self.rect.height - 4
            )
            
            # Color based on health level
            if health_ratio > 0.6:
                color = (0, 255, 0)  # Green
            elif health_ratio > 0.3:
                color = (255, 255, 0)  # Yellow
            else:
                color = (255, 0, 0)  # Red
                
            pygame.draw.rect(screen, color, fill_rect)


def load_font(size: int) -> pygame.font.Font:
    """
    Load the Press Start 2P font or fallback to system font.
    """
    try:
        # Try to load custom font from assets
        font_path = "assets/fonts/PressStart2P.ttf"
        return pygame.font.Font(font_path, size)
    except (pygame.error, FileNotFoundError):
        # Fallback to system monospace font
        print(f"Warning: Could not load custom font, using system fallback")
        return pygame.font.Font(None, size * 2)  # System font needs larger size


def draw_text_with_shadow(surface: pygame.Surface, text: str, font: pygame.font.Font,
                         pos: Tuple[int, int], color: Tuple[int, int, int] = WHITE,
                         shadow_color: Tuple[int, int, int] = BLACK,
                         shadow_offset: Tuple[int, int] = (2, 2)) -> None:
    """Draw text with a shadow effect."""
    # Draw shadow
    shadow_surface = font.render(text, False, shadow_color)
    shadow_pos = (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1])
    surface.blit(shadow_surface, shadow_pos)
    
    # Draw main text
    text_surface = font.render(text, False, color)
    surface.blit(text_surface, pos)