# This file was created by: AJ Ordonio
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Define the sprite groups
        self.groups = game.all_sprites
        # Initialize the sprite using the superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # Set the player image and rect
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # Set initial velocity and position
        self.vx, self.vy = 0, 0
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        # Initialize player attributes
        self.moneybag = 0
        self.speed = 100

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            # Diagonal movement speed adjustment
            self.vx *= 0.7071
            self.vy *= 0.7071

    # Method to handle collision with walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            for wall in hits:
                if self.vx > 0:
                    self.rect.right = wall.rect.left
                elif self.vx < 0:
                    self.rect.left = wall.rect.right
                self.vx = 0
        elif dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            for wall in hits:
                if self.vy > 0:
                    self.rect.bottom = wall.rect.top
                elif self.vy < 0:
                    self.rect.top = wall.rect.bottom
                self.vy = 0

    # Method to handle collision with sprite groups
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        for hit in hits:
            if isinstance(hit, Coin):
                self.moneybag += 1
                self.game.collect_sound.play()
            elif isinstance(hit, PowerUp):
                self.game.powerup_sound.play()
                self.speed += 200
            elif isinstance(hit, Chest):
                self.moneybag += 5
                self.speed += 100
            

    def update(self):
        self.get_keys()
        self.rect.x += self.vx * self.game.dt
        self.rect.y += self.vy * self.game.dt
        self.collide_with_walls('x')
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)

       
 
# Definition of the Wall sprite
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Define the sprite groups
        self.groups = game.all_sprites, game.walls
        # Initialize the sprite using the superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        # Store a reference to the game object
        self.game = game
        # Set the wall image and rect
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        # Set initial position
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
 
# Definition of the Coin sprite
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Define the sprite groups
        self.groups = game.all_sprites, game.coins,
        # Initialize the sprite using the superclass
        pg.sprite.Sprite.__init__(self, self.groups,)
        # Store a reference to the game object
        self.game = game
        # Set the coin image and rect
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        # Set initial position
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
        
        

        
# Definition of the PowerUp sprite
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Define the sprite groups
        self.groups = game.all_sprites, game.power_ups
        # Initialize the sprite using the superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        # Store a reference to the game object
        self.game = game
        # Set the power-up image and rect
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        # Set initial position
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
 # Definition of the Chest sprite
class Chest(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Define the sprite groups
        self.groups = game.all_sprites, game.power_ups
        # Initialize the sprite using the superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        # Store a reference to the game object
        self.game = game
        # Set the chest image and rect
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        # Set initial position
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
#def mob sprite
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 100

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        
    