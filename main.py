#this file was created by: Kyle Suhendra

'''
Sources are:
Mr. Cozort - Countdown, Movement, Text, Sprite Images, Spritesheet
https://github.com/Mosedo/Machine-Learning/blob/main/smart_dots.py - Max Speed
https://www.youtube.com/watch?v=2iyx8_elcYg - Main Menu
https://stackoverflow.com/questions/13984066/pygame-restart - Restart
ChatGPT input: Can you make a level the same size and similar to mine? (inputted Track 3 code) - Track 4
'''

#Importing the code needed to create game from other files
import pygame as pg
from settings import *
from sprites_race_thing import *
from tilemap import *
from utils import *
from os import path


'''
GOALS: Get to the finish before the countdown hits 0
RULES: Don't hit the debuffs
FEEDBACK: Time left
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
    self.game_timer = Timer(self)
    self.playing = True
    self.track_selected = None 
    self.map = None 
    self.player = None
    self.track_open = False
    self.player_active = False
    self.score = 0
    self.current_time = 0 
    
    

  def main_menu(self):
        #creates menu first
        menu_running = True
        while menu_running:
            self.screen.fill(BLACK)
            #Text on screen
            self.draw_text(self.screen, "Select Track", 32, WHITE, WIDTH / 2, HEIGHT / 4)
            self.draw_text(self.screen, "Press 0 for TUTORIAL", 24, WHITE, WIDTH / 2, HEIGHT / 2 - 40)
            self.draw_text(self.screen, "Press 1 for Track 1", 24, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text(self.screen, "Press 2 for Track 2", 24, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            self.draw_text(self.screen, "Press 3 for Track 3", 24, WHITE, WIDTH / 2, HEIGHT / 2 + 80)
            self.draw_text(self.screen, "Press 4 for Track 4", 24, WHITE, WIDTH / 2, HEIGHT / 2 + 120)
            pg.display.flip()

            self.game_folder = path.dirname(__file__)
        
            try:
              with open(path.join(self.game_folder, HS_FILE), 'r') as f:
                self.highscore = int(f.read())
            except:
              with open(path.join(self.game_folder, HS_FILE), 'w') as f:
                f.write(str(0))
          
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = False
                    menu_running = False
                #if number is clicked it will make the menu trun off and change self.track_selected to the right track
                elif event.type == pg.KEYDOWN:
                    keys = pg.key.get_pressed()
                    if event.key == pg.K_1:
                        self.track_selected = 1
                        menu_running = False
                    elif event.key == pg.K_2:
                        self.track_selected = 2
                        menu_running = False #Loads track based on what is pressed
                    elif event.key == pg.K_3:
                        self.track_selected = 3
                        menu_running = False 
                    elif event.key == pg.K_4:
                        self.track_selected = 4
                        menu_running = False 
                    elif event.key == pg.K_0:
                        self.track_selected = 100
                        menu_running = False 
                    
  #Made the loading code an if loop
  def load_data(self):
        self.game_folder = path.dirname(__file__)

        #Level 1
        if self.track_selected == 1:
            self.map = Map(path.join(self.game_folder, TRACK1))
            self.game_timer.cd = 42 
            self.track_open = True 
            self.player_active = True
        #level 2
        elif self.track_selected == 2:
            self.map = Map(path.join(self.game_folder, TRACK2))
            self.game_timer.cd = 28
            self.track_open = True 
            self.player_active = True
        #level 3
        elif self.track_selected == 3:
            self.map = Map(path.join(self.game_folder, TRACK3))
            self.game_timer.cd = 23
            self.track_open = True 
            self.player_active = True
        #level4
        elif self.track_selected == 4:
            self.map = Map(path.join(self.game_folder, TRACK4))
            self.game_timer.cd = 21
            self.track_open = True 
            self.player_active = True
        #Tutorial
        elif self.track_selected == 100:
            self.map = Map(path.join(self.game_folder, TRACK0))
            self.game_timer.cd = 21
            self.track_open = True 
            self.player_active = True
            
   # this is where the game creates the stuff you see and hear
  def new(self): 
      self.load_data()
      # print(self.map.data)
      # create the all sprites group to allow for batch updates and draw methods
      self.all_sprites = pg.sprite.Group()
      self.all_walls = pg.sprite.Group()
      self.all_powerups = pg.sprite.Group()
      self.all_coins = pg.sprite.Group()
      self.all_finishes = pg.sprite.Group()
    
      # code to create sprites
      if self.track_open:
        for row, tiles in enumerate(self.map.data):
          # print(row)
          for col, tile in enumerate(tiles):
            # print(col)
            if tile == "W":
              Wall(self, col, row)
            elif tile == "M":
              Mob(self, col, row)
            elif tile == "U":
              Powerup(self, col, row)
            elif tile == "C":
              Coin(self, col, row)
            elif tile == "P":
              self.player = Player(self, col, row)
            elif tile == "F":
              Finish(self, col, row)
  #reloads everything to reset
  def reset_game(self):
    self.current_time = 0  
    self.game_timer.current_time = 0
    self.load_data()  
    self.new()  
  
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
          self.running = False
          if self.score < self.highscore:
            with open(path.join(self.game_folder, HS_FILE), 'w') as f:
              f.write(str(self.score))                   
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
              self.reset_game()
            elif event.key == pg.K_e:
             self.playing = False  # Exit the current game loop
             self.main_menu()   
                

  # process
  # this is where the game updates the game state
  def update(self):
    
    # the timer counts down only if the player isn't finished 
    if self.player and hasattr(self.player, 'finished') and not self.player.finished: 
      self.game_timer.ticking()
      self.current_time = self.game_timer.get_current_time() 


    # update all the sprites
    if self.track_open:
      self.all_sprites.update()

    # kills all sprites if countdown hits 0
    if self.track_open:
      if self.game_timer.cd < 1:
        for s in  self.all_sprites:
          s.kill()  


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
    if self.track_open:
      if self.playing:
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

    #self.draw_text(self.screen, str(self.player.coin_count), 24, WHITE, 1000, 30)
    #self.draw_text(self.screen, str(self.player.speed), 24, WHITE, 1000, 30)

    #Drawing FPS
    #self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)

    # draws countdown
    if self.track_open:
     self.draw_text(self.screen, str(self.game_timer.get_countdown()), 24, WHITE, WIDTH/30, HEIGHT/30)
    

    # will say well done if player finishes
    if self.player:
      if self.player.finished:
        self.draw_text(self.screen, "WELL DONE", 24, WHITE, WIDTH/2, HEIGHT/2)

    # will say game over if timer hits 0
    if self.track_open:
      if self.game_timer.cd < 1:
        self.draw_text(self.screen, "GAME OVER", 24, WHITE, WIDTH/2, HEIGHT/2)

    if self.track_open:
      self.draw_text(self.screen, "High Score: " + str(self.highscore), 24, WHITE, WIDTH/2, HEIGHT/12)
      self.draw_text(self.screen, "Current Score: " + str(self.current_time), 24, WHITE, WIDTH/2, HEIGHT/24)

    #code for text in the tutorial
    if self.track_open:
      if self.track_selected == 100:
        self.draw_text(self.screen, "Speed Boost--->", 24, WHITE, WIDTH/2 - 240, HEIGHT/2 - 70)
        self.draw_text(self.screen, "Finish--->", 24, WHITE, WIDTH/2 - 95, HEIGHT/2 - 155)
        self.draw_text(self.screen, "W, A, S, D to move", 24, WHITE, WIDTH/2 - 408, HEIGHT/2 - 25)
        self.draw_text(self.screen, "Get to the finish", 24, WHITE, 200, 170)
        self.draw_text(self.screen, "before the coundown reaches 0", 24, WHITE, 200, 200)
        self.draw_text(self.screen, " and press R to reset", 24, WHITE, 200, 230)
        #self.draw_text(self.screen, "Press E to go back to Main Menu", 24, WHITE, 860, 720)
        self.draw_text(self.screen, "<---Countdown", 24, WHITE, 120, 25)
               
    pg.display.flip()

if __name__ == "__main__":
  # instantiate
  g = Game()
  g.main_menu()
  if g.track_selected:
    g.new()
    g.run()
 