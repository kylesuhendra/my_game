#this file was created by: Kyle Suhendra

#Importing the code needed to create game from other files
import pygame as pg
from settings import *
#from sprites import *
#from sprites_side_scroller import *
from sprites_race_thing import *
from tilemap import *
from utils import *
from os import path

'''
GOALS: collect all dots in the maze
RULES: don't hit the goasts
FEEDBACK: number of dots eaten and what level you're on
FREEDOM: can move around and turn
'''


# create a game class that carries all the properties of the game and methods
class Game:
  # initializes all the things we need to run the game...includes the game clock which can set the FPS
  def __init__(self):
    pg.init()
    # sound mixer
    pg.mixer.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Kyle's Game")
    self.playing = True
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    self.map = Map(path.join(self.game_folder, 'track1.txt'))

  # this is where the game creates the stuff you see and hear
  def new(self):
    self.load_data()
    print(self.map.data)
    # create the all sprites group to allow for batch updates and draw methods
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_powerups = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()

    self.game_timer = Timer(self)
    self.game_timer.cd = 45
    # instantiating the class to create the player object
     
    #self.player = Player(self, 5, 5)
    #self.mob = Mob(self, 100, 100)
    #self.wall = Wall(self, WIDTH//2, HEIGHT//2)
    # instantiates wall and mob objects
    #for i in range(12):
    #Wall(self, TILESIZE*i, HEIGHT/2)
    #Mob(self, TILESIZE*i, TILESIZE*i)

    # code to create sprites from level1
    for row, tiles in enumerate(self.map.data):
      print(row)
      for col, tile in enumerate(tiles):
        print(col)
        if tile == "W":
          Wall(self, col, row)
        if tile == "M":
          Mob(self, col, row)
        if tile == "U":
          Powerup(self, col, row)
        if tile == "C":
          Coin(self, col, row)
        if tile == "P":
          self.player = Player(self, col, row)
        
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
    if self.game_timer.cd < 1:

    # update all the sprites
     self.all_sprites.update()

  # Where we define text
  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

  # output
  #Drawing text 
  def draw(self):
    self.screen.fill(BLACK)
    self.all_sprites.draw(self.screen)
    #Drawing "hi"
    #self.draw_text(self.screen, "hi", 24, WHITE, WIDTH/2, HEIGHT/2)
    #self.draw_text(self.screen, str(self.player.coin_count), 24, WHITE, 1000, 30)
    self.draw_text(self.screen, str(self.player.speed), 24, WHITE, 1000, 30)
    #Drawing FPS
    #self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    self.draw_text(self.screen, str(self.game_timer.get_countdown()), 24, WHITE, WIDTH/30, HEIGHT/30)
    pg.display.flip()

if __name__ == "__main__":
  # instantiate
  g = Game()
  g.new()
  g.run()