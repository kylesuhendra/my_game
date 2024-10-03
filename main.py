#this file was created by: Kyle Suhendra

#Importing the code needed to create game from other files
import pygame as pg
from settings import *
from sprites import *
from tilemap import *
from os import path

# create a game class that carries all the properties of the game and methods
class Game:
  # initializes all the things we need to run the game...includes the game clock which can set the FPS
  def __init__(self):
    pg.init()
    # sound mixer...
    pg.mixer.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Kyle's Game")
    self.playing = True
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    self.map = Map(path.join(self.game_folder, 'level1.txt'))
  # this is where the game creates the stuff you see and hear
  def new(self):
    self.load_data()
    # create the all sprites group to allow for batch updates and draw methods
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    # instantiating the class to create the player object 
    #self.player = Player(self, 5, 5)
    #self.mob = Mob(self, 100, 100)
    #self.wall = Wall(self, WIDTH//2, HEIGHT//2)
    # instantiates wall and mob objects
    #for i in range(12):
    #Wall(self, TILESIZE*i, HEIGHT/2)
    #Mob(self, TILESIZE*i, TILESIZE*i)
    for row, tiles in enumerate(self.map.data):
      print(row)
      for col, tile in enumerate(tiles):
        print(col)
        if tile == "1":
          Wall(self, col*TILESIZE, row*TILESIZE)
        if tile == "M":
          Mob(self, col*TILESIZE, row*TILESIZE)
        if tile == "P":
          self.player = Player(self, col*TILESIZE, row*TILESIZE)

# methods are like functions that are part of a class
# the run method runs the game loop
  def run(self):
    while self.playing:
      self.dt = self.clock.tick(FPS) / 1000
      # input
      self.events()
      # process
      self.update()
      # output
      self.draw()

    pg.quit()
  # input
  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          self.playing = False
  # process
  # this is where the game updates the game state
  def update(self):
    # update all the sprites
    self.all_sprites.update()

  # output
  def draw(self):
    self.screen.fill((0, 0, 0))
    self.all_sprites.draw(self.screen)
    pg.display.flip()

if __name__ == "__main__":
  # instantiate
  g = Game()
  g.new()
  g.run()