"""
Game entities for Pasta Savaşı: Player, AI, and Projectiles.
"""

import pygame
import math
import random
from typing import List, Tuple, Optional
from enum import Enum

from .constants import *


class EntityType(Enum):
    PLAYER = "player"
    AI = "ai"
    PROJECTILE = "projectile"


class Entity:
    """Base entity class."""
    
    def __init__(self, x: float, y: float, width: int, height: int, entity_type: EntityType):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.entity_type = entity_type
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.rect = pygame.Rect(int(x), int(y), width, height)
        
    def update(self, dt: float) -> None:
        """Update entity position and rect."""
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the entity (to be overridden by subclasses)."""
        pygame.draw.rect(screen, WHITE, self.rect)
        

class Projectile(Entity):
    """Pastry projectile entity."""
    
    def __init__(self, x: float, y: float, direction_x: float, direction_y: float, owner_type: EntityType):
        super().__init__(x, y, PROJECTILE_SIZE, PROJECTILE_SIZE, EntityType.PROJECTILE)
        
        # Normalize direction and apply speed
        magnitude = math.sqrt(direction_x**2 + direction_y**2)
        if magnitude > 0:
            self.velocity_x = (direction_x / magnitude) * PROJECTILE_SPEED
            self.velocity_y = (direction_y / magnitude) * PROJECTILE_SPEED
        
        self.owner_type = owner_type
        self.lifetime = PROJECTILE_LIFETIME
        self.damage = PROJECTILE_DAMAGE
        
    def update(self, dt: float) -> bool:
        """Update projectile. Returns False if should be destroyed."""
        super().update(dt)
        self.lifetime -= dt
        
        # Check screen bounds
        if (self.x < -self.width or self.x > SCREEN_WIDTH or
            self.y < -self.height or self.y > SCREEN_HEIGHT or
            self.lifetime <= 0):
            return False
            
        return True
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the projectile as a colored circle."""
        center = (int(self.x + self.width // 2), int(self.y + self.height // 2))
        radius = self.width // 2
        
        # Different colors based on owner
        if self.owner_type == EntityType.PLAYER:
            color = ORANGE  # Player projectiles are orange
        else:
            color = RED     # AI projectiles are red
            
        pygame.draw.circle(screen, color, center, radius)
        pygame.draw.circle(screen, BLACK, center, radius, 2)


class Character(Entity):
    """Base character class for Player and AI."""
    
    def __init__(self, x: float, y: float, entity_type: EntityType):
        super().__init__(x, y, PLAYER_SIZE, PLAYER_SIZE, entity_type)
        self.health = PLAYER_MAX_HEALTH
        self.facing_x = 1  # Direction facing (-1 for left, 1 for right)
        self.facing_y = 0
        self.throw_cooldown = 0.0
        self.speed = PLAYER_SPEED
        
    def update(self, dt: float) -> None:
        """Update character with friction."""
        # Apply friction
        self.velocity_x *= FRICTION
        self.velocity_y *= FRICTION
        
        # Update cooldown
        if self.throw_cooldown > 0:
            self.throw_cooldown -= dt
        
        super().update(dt)
        
        # Keep within screen bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
    def take_damage(self, damage: int) -> bool:
        """Take damage. Returns True if character died."""
        self.health -= damage
        return self.health <= 0
        
    def can_throw(self) -> bool:
        """Check if character can throw a projectile."""
        return self.throw_cooldown <= 0
        
    def throw_projectile(self, target_x: float, target_y: float) -> Optional[Projectile]:
        """Throw a projectile toward target position."""
        if not self.can_throw():
            return None
            
        # Calculate direction from character center to target
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        direction_x = target_x - center_x
        direction_y = target_y - center_y
        
        # Update facing direction
        if abs(direction_x) > abs(direction_y):
            self.facing_x = 1 if direction_x > 0 else -1
            self.facing_y = 0
        else:
            self.facing_y = 1 if direction_y > 0 else -1
            self.facing_x = 0
        
        # Set cooldown
        self.throw_cooldown = 1.0  # 1 second cooldown
        
        return Projectile(center_x, center_y, direction_x, direction_y, self.entity_type)


class Player(Character):
    """Human player character."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, EntityType.PLAYER)
        
    def handle_input(self, keys: dict, dt: float) -> None:
        """Handle player input."""
        # Movement
        move_x = 0
        move_y = 0
        
        if keys.get(pygame.K_LEFT) or keys.get(pygame.K_a):
            move_x -= 1
        if keys.get(pygame.K_RIGHT) or keys.get(pygame.K_d):
            move_x += 1
        if keys.get(pygame.K_UP) or keys.get(pygame.K_w):
            move_y -= 1
        if keys.get(pygame.K_DOWN) or keys.get(pygame.K_s):
            move_y += 1
            
        # Normalize diagonal movement
        if move_x != 0 and move_y != 0:
            move_x *= 0.707  # 1/sqrt(2)
            move_y *= 0.707
            
        self.velocity_x = move_x * self.speed
        self.velocity_y = move_y * self.speed
        
    def throw_at_mouse(self, mouse_pos: Tuple[int, int]) -> Optional[Projectile]:
        """Throw projectile toward mouse position."""
        return self.throw_projectile(float(mouse_pos[0]), float(mouse_pos[1]))
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player character."""
        # Draw player as a blue rectangle with direction indicator
        pygame.draw.rect(screen, BLUE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw facing direction indicator
        center_x = self.rect.centerx
        center_y = self.rect.centery
        indicator_size = 8
        
        if self.facing_x != 0:
            end_x = center_x + self.facing_x * indicator_size
            pygame.draw.line(screen, WHITE, (center_x, center_y), (end_x, center_y), 3)
        if self.facing_y != 0:
            end_y = center_y + self.facing_y * indicator_size
            pygame.draw.line(screen, WHITE, (center_x, center_y), (center_x, end_y), 3)


class AIOpponent(Character):
    """AI opponent character."""
    
    def __init__(self, x: float, y: float, difficulty: AIDifficulty):
        super().__init__(x, y, EntityType.AI)
        self.difficulty = difficulty
        self.settings = AI_SETTINGS[difficulty]
        self.speed = self.settings["speed"]
        self.throw_cooldown_max = self.settings["throw_cooldown"]
        self.reaction_time = self.settings["reaction_time"]
        
        # AI state
        self.target_x = x
        self.target_y = y
        self.last_seen_player_x = 0
        self.last_seen_player_y = 0
        self.reaction_timer = 0.0
        self.behavior_timer = 0.0
        self.current_behavior = "chase"  # "chase", "strafe", "retreat"
        
    def update_ai(self, player: Player, dt: float) -> Optional[Projectile]:
        """Update AI behavior and potentially throw projectile."""
        self.behavior_timer += dt
        self.reaction_timer += dt
        
        # Update last seen player position with reaction delay
        if self.reaction_timer >= self.reaction_time:
            self.last_seen_player_x = player.x + player.width // 2
            self.last_seen_player_y = player.y + player.height // 2
            self.reaction_timer = 0.0
            
        # Change behavior periodically
        if self.behavior_timer >= 3.0:  # Change behavior every 3 seconds
            behaviors = ["chase", "strafe", "retreat"]
            self.current_behavior = random.choice(behaviors)
            self.behavior_timer = 0.0
            
        # Calculate distance to player
        distance = math.sqrt(
            (self.last_seen_player_x - (self.x + self.width // 2))**2 +
            (self.last_seen_player_y - (self.y + self.height // 2))**2
        )
        
        # Choose target based on behavior
        if self.current_behavior == "chase":
            self.target_x = self.last_seen_player_x
            self.target_y = self.last_seen_player_y
        elif self.current_behavior == "strafe":
            # Move perpendicular to player direction
            angle = math.atan2(
                self.last_seen_player_y - (self.y + self.height // 2),
                self.last_seen_player_x - (self.x + self.width // 2)
            )
            strafe_angle = angle + math.pi / 2
            self.target_x = self.x + math.cos(strafe_angle) * 100
            self.target_y = self.y + math.sin(strafe_angle) * 100
        else:  # retreat
            # Move away from player
            if distance > 0:
                direction_x = (self.x + self.width // 2) - self.last_seen_player_x
                direction_y = (self.y + self.height // 2) - self.last_seen_player_y
                magnitude = math.sqrt(direction_x**2 + direction_y**2)
                if magnitude > 0:
                    self.target_x = self.x + (direction_x / magnitude) * 100
                    self.target_y = self.y + (direction_y / magnitude) * 100
        
        # Move toward target
        self._move_toward_target(dt)
        
        # Try to throw projectile if player is in range and line of sight
        projectile = None
        if distance < 300 and self.can_throw():  # Within throwing range
            if self._has_line_of_sight(player):
                projectile = self.throw_projectile(self.last_seen_player_x, self.last_seen_player_y)
                if projectile:
                    self.throw_cooldown = self.throw_cooldown_max
                    
        return projectile
    
    def _move_toward_target(self, dt: float) -> None:
        """Move AI toward current target."""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        direction_x = self.target_x - center_x
        direction_y = self.target_y - center_y
        
        distance = math.sqrt(direction_x**2 + direction_y**2)
        
        if distance > 10:  # Don't move if very close to target
            # Normalize and apply speed
            direction_x /= distance
            direction_y /= distance
            
            self.velocity_x = direction_x * self.speed
            self.velocity_y = direction_y * self.speed
        else:
            self.velocity_x = 0
            self.velocity_y = 0
    
    def _has_line_of_sight(self, player: Player) -> bool:
        """Simple line of sight check (always true for now)."""
        # TODO: Implement obstacle checking when adding arena obstacles
        return True
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the AI character."""
        # Draw AI as a red rectangle with direction indicator
        pygame.draw.rect(screen, RED, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw facing direction indicator
        center_x = self.rect.centerx
        center_y = self.rect.centery
        indicator_size = 8
        
        if self.facing_x != 0:
            end_x = center_x + self.facing_x * indicator_size
            pygame.draw.line(screen, WHITE, (center_x, center_y), (end_x, center_y), 3)
        if self.facing_y != 0:
            end_y = center_y + self.facing_y * indicator_size
            pygame.draw.line(screen, WHITE, (center_x, center_y), (center_x, end_y), 3)