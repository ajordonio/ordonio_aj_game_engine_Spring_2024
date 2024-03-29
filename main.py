# This file was created by: AJ Ordonio
# added this comment to prove github is working
# import libraries and modules

'''add these features: Start screen, coin counter, loot box, music'''

import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path

class Game:
    # Initialize game
    def __init__(self):
        # Initialize pygame and mixer
        pg.init()
        pg.mixer.init()

        # Set up the display
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)

        # Set up the clock
        self.clock = pg.time.Clock()

        # Load game data
        self.load_data()

        self.game_over = False
        self.game_win = False
       

    # Load game data
    def load_data(self):
        # Define game folder and sound folder paths
        self.game_folder = path.dirname(__file__)
        self.snd_folder = path.join(self.game_folder, 'sounds')
        self.map_data = []

        # Read map data from file
        with open(path.join(self.game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line.strip()) 

    # Create new game
    def new(self):
        # Load background music and sound effects
        pg.mixer.music.load(path.join(self.snd_folder, 'gamesoundtrack1.mp3'))
        self.collect_sound = pg.mixer.Sound(path.join(self.snd_folder, 'coinsound.mp3'))
        self.powerup_sound = pg.mixer.Sound(path.join(self.snd_folder, 'powerupsound.mp3'))

        # Create sprite groups
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()

         # Define the range of coordinates
        

        # Parse map data and create game objects
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
                if tile == 'L':
                    Chest(self, col, row)

    # Run the game
    def run(self):
        # Set background music volume and play
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            # Limit the frame rate
            self.dt = self.clock.tick(FPS) / 1000
            # Handle events
            self.events()
            # Update game state
            self.update()
            # Draw game elements
            self.draw()
        
         # Check if the game is over
            if self.game_over:
                self.playing = False
                self.show_end_screen()
                pg.mixer.music.fadeout(500)
        

            if self.game_over:
                self.playing = False 
                self.show_end_screen()
         
        
        
            

    # Quit the game
    def quit(self):
        pg.quit()
        sys.exit()

    # Update game state
    def update(self):
        self.all_sprites.update()
        
        # Check for collision between player and mobs
        hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if hits:
            self.game_over = True  
            self.moneybag = 0

        if self.player.moneybag >= 6:
            self.game_win = True
            # Exit the game loop
            self.playing = False
            self.moneybag = 0
            
        

    # Draw the grid
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    # Draw text on the screen
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('Arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)

    # Draw game elements
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, "Coins" + str(self.player.moneybag), 24, WHITE, WIDTH // 2 - 32, 2)
        
        #coin counter using moneybag
       
        
        pg.display.flip()

    # Handle game events
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    # Display the start screen
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press any key to play", 24, WHITE, 2, 3)
        pg.display.flip()
        self.wait_for_key() 

    def show_end_screen(self):
        # Display the end screen
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Game Over", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Press any key to play again", 24, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
            # Add a delay to keep the end screen visible
        pg.time.delay(3000)  # Delay for 3000 milliseconds (3 seconds)

        # Reset the game state
        self.game_over = False

    def show_win_screen(self):
        # Display the win screen
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "YOU WON!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Press any key to play again", 24, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
            # Add a delay to keep the end screen visible
        pg.time.delay(3000)  # Delay for 3000 milliseconds (3 seconds)

        # Reset the game state
        self.game_win = False


    def player_hit_mob(self):
        # Check if the player has collided with a mob
        hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        return bool(hits)

    # Wait for a key press
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# Initialize the game
g = Game()

# Show the start screen
g.show_start_screen()

# Run the game loop
while True:
    # Start a new game
    g.new()
    
    # Run the game
    g.run()
    
    # Check if the game is over
    if g.game_over:
        # Show the end screen
        g.show_start_screen()
    if g.game_win:
        g.show_start_screen()