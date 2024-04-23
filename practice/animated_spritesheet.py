import pygame as pg
from pygame.sprite import Sprite
from os import path

BLACK = (0,0,0)
SPRITESHEET = "theBell.png"

TITLE = "Sprite"
FONT_NAME = "arial"
WIDTH = 300
HEIGHT = 200
FPS = 30
BGCOLOR = (0,0,0)
WHITE = (255,255,255)

dir = path.dirname(__file__)
img_dir = path.join(dir, 'images')


# sets up file with multiple images...
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 4, height * 4))
        return image 
     
    