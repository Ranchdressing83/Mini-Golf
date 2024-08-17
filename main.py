# main.py
import pygame
import sys
from gamestate import GameStateManager
from homescreen import HomeScreen
from holeone import HoleOne
from roundover import RoundOver


class Game:
    def __init__(self):
        pygame.init()
        self.running = [True]
        self.current_hole = ['home_screen']
        self.high_score = []
        self.total_strokes = [0]
        self.screen = pygame.display.set_mode((1280, 720))
        self.large_font = pygame.font.Font(None, 150)
        self.button_font = pygame.font.Font(None, 75)
        self.stroke_font = pygame.font.Font(None, 45)
        self.clock = pygame.time.Clock()
        self.gameStateManager = GameStateManager('home_screen')
        self.states = {
            'home_screen': HomeScreen(self.screen, self.gameStateManager, self.running, self.current_hole,self.large_font, self.button_font),
            'hole_one': HoleOne(self.screen, self.gameStateManager, self.running, self.current_hole, self.total_strokes, self.stroke_font, self.button_font),
            'round_over': RoundOver(self.screen, self.gameStateManager, self.running, self.current_hole,self.large_font, self.button_font)
        }

    def run(self):
        while self.running[0]:
            dt = self.clock.tick(60) / 1000  # Calculate the time passed since the last frame (in seconds)
            self.states[self.gameStateManager.get_state()].run(dt)

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    self.running[0] = False

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
