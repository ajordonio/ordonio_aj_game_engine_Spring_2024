# This file was created by: AJ Ordonio
# added this comment to prove github is working
# import libraries and modules
'''add these features: Start screen, coin counter, loot box, music'''
'''Beta: New Map'''
'''release version: '''

# Credits: ChatGPT
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path


LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"

class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
        self.game_over = False
        self.game_win = False
        self.paused = False
    
        self.shop_items = {
        "Armor (B)": 5,
        "Potion (N)": 3,
    }

    def show_item_shop(self):
        self.paused = True  # Set the paused flag to True when item shop opens

        # Clear the screen and draw item shop interface
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Item Shop", 64, WHITE, WIDTH // 2, HEIGHT // 4)
        self.draw_text(self.screen, "Press P to return to game", 24, WHITE, WIDTH // 2, HEIGHT // 2)
        pg.display.flip()

        # Wait for the player to return to the game
        #from chat gpt
        while self.paused:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.paused = False  # Unpause the game when 'P' is pressed
      # Check if the game should unpause after the delay
    

    # Load game datas
    def load_data(self):
        # Define game folder and sound folder paths
        self.game_folder = path.dirname(__file__)
        self.snd_folder = path.join(self.game_folder, 'sounds')
        self.map_data = []

        # Read map data from file
        

        with open(path.join(self.game_folder, LEVEL1), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
                
        # Parse map data and create game objects
    def change_level(self, lvl):
        self.currLvl = lvl 
        # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
        # reset criteria for changing level
        self.moneybag = 0
        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, lvl ), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        # repopulate the level with stuff
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
        # start playing sound on infinite loop (loops=-1)
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
             # Check if the game is over
             
            if self.game_over:
                self.playing = False
                self.show_end_screen()
                pg.mixer.music.fadeout(500)
        

            if self.game_over:
                self.playing = False 
                self.show_end_screen()

         # Check if the game is over
    





    # Quit the game
    def quit(self):
        pg.quit()
        sys.exit()

    

    # Update game state
    # Update game state
    def update(self):
        self.all_sprites.update()
        
        # Check for collision between player and mobs
        hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if hits:
            self.game_over = True  
            self.change_level(LEVEL1)
            self.moneybag = 0

        if self.player.moneybag > 6:
            self.change_level(LEVEL2)
            

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
            if event.type == pg.KEYUP:
                if event.key == pg.K_i:
                   self.show_item_shop()
                   

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
        