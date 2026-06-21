import pygame
import random
import math
import sys
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
LEVEL_MAX = 80

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

class WeaponType(Enum):
    PISTOL = 1
    RIFLE = 2
    SHOTGUN = 3
    SNIPER = 4

@dataclass
class Weapon:
    name: str
    weapon_type: WeaponType
    damage: int
    fire_rate: int
    ammo: int
    max_ammo: int
    bullet_speed: int
    spread_angle: float
    
    def can_shoot(self):
        return self.ammo > 0

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 40
        self.height = 50
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.health = 100
        self.max_health = 100
        
        # Weapons
        self.weapons = {
            WeaponType.PISTOL: Weapon("Pistol", WeaponType.PISTOL, 10, 10, 30, 30, 7, 0),
            WeaponType.RIFLE: Weapon("Rifle", WeaponType.RIFLE, 20, 5, 60, 60, 8, 15),
            WeaponType.SHOTGUN: Weapon("Shotgun", WeaponType.SHOTGUN, 15, 20, 24, 24, 6, 45),
            WeaponType.SNIPER: Weapon("Sniper", WeaponType.SNIPER, 50, 40, 12, 12, 10, 0),
        }
        
        self.current_weapon = WeaponType.PISTOL
        self.shoot_cooldown = 0
        
        # Create surface
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def handle_input(self, keys):
        self.velocity_x = 0
        self.velocity_y = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = self.speed
        
        # Weapon switching
        if keys[pygame.K_1]:
            self.current_weapon = WeaponType.PISTOL
        if keys[pygame.K_2]:
            self.current_weapon = WeaponType.RIFLE
        if keys[pygame.K_3]:
            self.current_weapon = WeaponType.SHOTGUN
        if keys[pygame.K_4]:
            self.current_weapon = WeaponType.SNIPER
    
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Boundary checking
        if self.x < 0:
            self.x = 0
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def shoot(self, mouse_pos):
        weapon = self.weapons[self.current_weapon]
        
        if not weapon.can_shoot() or self.shoot_cooldown > 0:
            return []
        
        self.shoot_cooldown = weapon.fire_rate
        weapon.ammo -= 1
        
        bullets = []
        
        # Calculate direction
        dx = mouse_pos[0] - (self.x + self.width // 2)
        dy = mouse_pos[1] - (self.y + self.height // 2)
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance == 0:
            return bullets
        
        dx /= distance
        dy /= distance
        
        # Generate bullets based on weapon type
        if weapon.weapon_type == WeaponType.PISTOL:
            bullets.append(Bullet(self.x + self.width // 2, self.y + self.height // 2, 
                                 dx, dy, weapon.bullet_speed, weapon.damage, YELLOW))
        
        elif weapon.weapon_type == WeaponType.RIFLE:
            # Spread shots
            angles = [-7.5, 0, 7.5]
            for angle in angles:
                rad = math.radians(angle)
                new_dx = dx * math.cos(rad) - dy * math.sin(rad)
                new_dy = dx * math.sin(rad) + dy * math.cos(rad)
                bullets.append(Bullet(self.x + self.width // 2, self.y + self.height // 2,
                                     new_dx, new_dy, weapon.bullet_speed, weapon.damage, GREEN))
        
        elif weapon.weapon_type == WeaponType.SHOTGUN:
            # Wide spread
            for i in range(8):
                angle = -45 + (i * 12.5)
                rad = math.radians(angle)
                new_dx = dx * math.cos(rad) - dy * math.sin(rad)
                new_dy = dx * math.sin(rad) + dy * math.cos(rad)
                bullets.append(Bullet(self.x + self.width // 2, self.y + self.height // 2,
                                     new_dx, new_dy, weapon.bullet_speed - 2, weapon.damage // 2, ORANGE))
        
        elif weapon.weapon_type == WeaponType.SNIPER:
            # Single powerful shot
            bullets.append(Bullet(self.x + self.width // 2, self.y + self.height // 2,
                                 dx, dy, weapon.bullet_speed, weapon.damage, CYAN))
        
        return bullets
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, speed, damage, color):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.radius = 5
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill(color)
        self.rect = self.image.get_rect()
    
    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
        
        # Remove if off-screen
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type, level):
        super().__init__()
        self.x = x
        self.y = y
        self.enemy_type = enemy_type  # 0: Basic, 1: Fast, 2: Tanky
        self.level = level
        
        # Stats based on type and level
        if enemy_type == 0:  # Basic
            self.width = 30
            self.height = 30
            self.health = 20 + level * 2
            self.speed = 2 + level * 0.2
            self.damage = 5 + level
            self.color = RED
        elif enemy_type == 1:  # Fast
            self.width = 25
            self.height = 25
            self.health = 15 + level
            self.speed = 4 + level * 0.3
            self.damage = 3 + level
            self.color = PURPLE
        else:  # Tanky
            self.width = 40
            self.height = 40
            self.health = 40 + level * 3
            self.speed = 1 + level * 0.1
            self.damage = 8 + level * 1.5
            self.color = ORANGE
        
        self.max_health = self.health
        self.velocity_x = 0
        self.velocity_y = 0
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, player_pos):
        # Simple AI - move towards player
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            dx /= distance
            dy /= distance
        
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        self.rect.x = self.x
        self.rect.y = self.y
    
    def take_damage(self, damage):
        self.health -= damage
    
    def draw_health_bar(self, surface):
        bar_width = self.width
        bar_height = 5
        fill = (self.health / self.max_health) * bar_width
        
        outline_rect = pygame.Rect(self.x, self.y - 10, bar_width, bar_height)
        fill_rect = pygame.Rect(self.x, self.y - 10, fill, bar_height)
        
        pygame.draw.rect(surface, RED, outline_rect)
        pygame.draw.rect(surface, GREEN, fill_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("FIRING THE ENEMY 🎮")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 56)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        
        self.level = 1
        self.score = 0
        self.enemies_killed = 0
        self.game_over = False
        self.wave_count = 0
        self.wave_cooldown = 0
        
        self.spawn_wave()
    
    def spawn_wave(self):
        """Spawn enemies for current wave"""
        enemies_to_spawn = 3 + (self.level // 5) * 2
        
        for _ in range(enemies_to_spawn):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, 200)
            enemy_type = random.choices([0, 1, 2], weights=[0.6, 0.3, 0.1])[0]
            enemy = Enemy(x, y, enemy_type, self.level)
            self.enemies.add(enemy)
    
    def next_level(self):
        """Progress to next level"""
        if self.level < LEVEL_MAX:
            self.level += 1
            self.spawn_wave()
            
            # Refill ammo
            for weapon in self.player.weapons.values():
                weapon.ammo = weapon.max_ammo
            
            # Heal player slightly
            self.player.heal(10)
        else:
            self.game_over = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    new_bullets = self.player.shoot(mouse_pos)
                    self.bullets.add(*new_bullets)
        
        return True
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update()
        
        # Update enemies
        player_pos = (self.player.x + self.player.width // 2, 
                     self.player.y + self.player.height // 2)
        for enemy in self.enemies:
            enemy.update(player_pos)
        
        # Update bullets
        self.bullets.update()
        
        # Collision detection - bullets and enemies
        for bullet in self.bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, self.enemies, False)
            for enemy in hit_enemies:
                enemy.take_damage(bullet.damage)
                bullet.kill()
                
                if enemy.health <= 0:
                    self.score += 100 + self.level * 10
                    self.enemies_killed += 1
                    enemy.kill()
        
        # Collision detection - enemies and player
        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hit_enemies:
            self.player.take_damage(enemy.damage)
            enemy.kill()
        
        # Check if wave is complete
        if len(self.enemies) == 0 and self.wave_cooldown == 0:
            self.wave_cooldown = 120
        
        if self.wave_cooldown > 0:
            self.wave_cooldown -= 1
            if self.wave_cooldown == 0:
                self.next_level()
        
        # Game over condition
        if self.player.health <= 0:
            self.game_over = True
    
    def draw_hud(self):
        """Draw heads-up display"""
        weapon = self.player.weapons[self.player.current_weapon]
        
        # Level
        level_text = self.font_small.render(f"LEVEL: {self.level}/{LEVEL_MAX}", True, WHITE)
        self.screen.blit(level_text, (20, 20))
        
        # Score
        score_text = self.font_small.render(f"SCORE: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 60))
        
        # Health
        health_text = self.font_small.render(f"HEALTH: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (20, 100))
        
        # Current Weapon
        weapon_text = self.font_small.render(f"WEAPON: {weapon.name.upper()} [{weapon.ammo}/{weapon.max_ammo}]", True, CYAN)
        self.screen.blit(weapon_text, (SCREEN_WIDTH - 400, 20))
        
        # Weapon switching instructions
        switch_text = self.font_small.render("Press 1-4 to switch weapons", True, YELLOW)
        self.screen.blit(switch_text, (SCREEN_WIDTH - 400, 60))
        
        # Enemies remaining
        enemies_text = self.font_small.render(f"ENEMIES: {len(self.enemies)}", True, RED)
        self.screen.blit(enemies_text, (SCREEN_WIDTH - 400, 100))
    
    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        if self.player.health <= 0:
            title = self.font_large.render("GAME OVER!", True, RED)
        else:
            title = self.font_large.render("YOU WON!", True, GREEN)
        
        score_text = self.font_medium.render(f"FINAL SCORE: {self.score}", True, WHITE)
        level_text = self.font_medium.render(f"LEVEL REACHED: {self.level}", True, WHITE)
        killed_text = self.font_medium.render(f"ENEMIES KILLED: {self.enemies_killed}", True, WHITE)
        
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 150, 300))
        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - 150, 350))
        self.screen.blit(killed_text, (SCREEN_WIDTH // 2 - 150, 400))
        
        restart_text = self.font_small.render("Close window to exit", True, YELLOW)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, 500))
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw player
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        
        # Draw enemies and their health bars
        for enemy in self.enemies:
            self.screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y))
            enemy.draw_health_bar(self.screen)
        
        # Draw bullets
        for bullet in self.bullets:
            self.screen.blit(bullet.image, (bullet.rect.x, bullet.rect.y))
        
        # Draw HUD
        self.draw_hud()
        
        # Draw game over screen if needed
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            running = self.handle_events()
            
            if not self.game_over:
                self.update()
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
