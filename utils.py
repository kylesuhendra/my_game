import pygame as pg
from math import floor

class Timer():
    # sets all properties to zero when instantiated...
    def __init__(self, game):
        self.game = game
        self.current_time = 0
        self.event_time = 0
        self.cd = 0
        self.cu = 0

        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.countup()
        self.current_time = floor((pg.time.get_ticks())/1000)
        if self.cd > 0:
            self.countdown()

    # resets event time to zero - cooldown reset
    def get_countdown(self):
        return floor(self.cd)
    
    def countdown(self):
        if self.cd > 0:
            self.cd = self.cd - self.game.dt

    def get_countup(self):
        return floor(self.cu)
    
    def countup(self):
        self.cu = self.cu + self.game.dt

    # def event_reset(self):
    #     self.event_time = floor((self.game.clock.)/1000)

    # sets current time
    def get_current_time(self):
        # self.current_time = floor((pg.time.get_ticks())/1000)
        return self.current_time
    
    def reset(self):
        self.current_time = 0
        self.event_time = 0
        self.cd = 0
        self.cu = 0
