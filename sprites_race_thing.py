#This file was created by: Kyle Suhendra

import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
from os import path

SPRITESHEET = 'carspritesheet.png'

dir = path.dirname(__file__)
img_dir = path.join(dir, "images")
# sets up file with multiple images...
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height, scale):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width*scale, height*scale))
        return image
    
vec = pg.math.Vector2

# create the player class with a superclass of Sprite
class Player(Sprite):
    # this initializes the properties of the player class including the x y location, and the game parameter so that the the player can interact logically with
    # other elements in the game...
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.load_images()
        self.image = self.standing_image
        self.rect = self.image.get_rect()
        self.rect.x = x*TILESIZE
        self.rect.y = y*TILESIZE
        self.pos = vec(self.rect.x, self.rect.y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 1
        self.max_speed = 10
        self.coin_count = 0
        self.finish_count = 0
        self.finished = False
        self.direction = 1

    def load_images(self):
        self.image_up = self.spritesheet.get_image(0, 0, 16, 16, 1)     # Up image
        self.image_right = self.spritesheet.get_image(32, 0, 16, 16, 1)  # Right image
        self.image_down = self.spritesheet.get_image(48, 0, 16, 16, 1)   # Down image
        self.image_left = self.spritesheet.get_image(16, 0, 16, 16, 1)   # Left image
        self.standing_image = self.image_up 

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vel.y -= self.speed
            self.image = self.image_up
        if keys[pg.K_a]:
            self.vel.x -= self.speed
            self.image = self.image_left
        if keys[pg.K_s]:
            self.vel.y += self.speed
            self.image = self.image_down
        if keys[pg.K_d]:
            self.vel.x += self.speed
            self.image = self.image_right
        #if keys[pg.K_SPACE]:
            #self.jump()

    def jump(self):
        print("im trying to jump")
        print(self.vel.y)
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
            print('still trying to jump...')
            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
            #     print("Collided on x axis")
            # else:
            #     print("not working...for hits")
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.vel.y = 0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False
        
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                keys = pg.key.get_pressed()
                if keys[pg.K_a]:
                    self.vel.x -= 40
                if keys[pg.K_d]:
                    self.vel.x += 40
                if keys[pg.K_s]:
                    self.vel.y += 40
                if keys[pg.K_w]:
                    self.vel.y -= 40
                print("I've gotten a powerup!")
            if str(hits[0].__class__.__name__) == "Coin":
                print("I got a coin!!!")
                self.coin_count += 1
            if str(hits[0].__class__.__name__) == "Finish":
                print("I finished!!!")
                self.finished = True
                self.finish_count += 1
            
                
    
    def update(self):
        #self.acc = vec(0, GRAVITY)
        self.acc = vec (0,0)
        self.get_keys()
        
        #self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
        #applies friction
        self.acc.x += self.vel.x * FRICTION
        self.acc.y += self.vel.y * FRICTION
        self.vel += self.acc

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc

        #sets max speed for car
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        if self.vel.x > self.max_speed:
            self.vel.x = self.max_speed

        if self.vel.y > self.max_speed:
            self.vel.y = self.max_speed

        self.rect.x = self.pos.x
        self.collide_with_walls('x')

        self.rect.y = self.pos.y
        self.collide_with_walls('y')
       
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_finishes, True)

# added Mob - moving objects
# it is a child class of Sprite
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 25

    def update(self):
        self.rect.x += self.speed
        # self.rect.y += self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.rect.y += 32
        if self.rect.y > HEIGHT:
            self.rect.y = 0

        if self.rect.colliderect(self.game.player):
            self.speed *= -1

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Finish(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_finishes
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(NEON)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
