# homescreen.py
import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from button import Button

class RoundOver:
    def __init__(self,display, gameStateManager, running, current_hole, large_font, button_font):
        self.display = display
        self.gameStateManager = gameStateManager
        self.running = running
        self.current_hole = current_hole
        self.large_font = large_font
        self.button_font = button_font
        
    def draw_text(self, text, font, text_color, x, y, screen):
        rendered_text = font.render(text, True, text_color)
        text_rect = rendered_text.get_frect(center=(x, y))
        screen.blit(rendered_text, text_rect)

    def run(self, dt):
        self.display.fill('dark green')

        self.draw_text('Round Over', self.large_font, 'white', SCREEN_WIDTH / 2, 75, self.display)

        menu_button = Button(self.display, 'dark green', ((SCREEN_WIDTH/2) - 150), 200, 275, 75, 'Main menu', self.button_font)
        play_again_button = Button(self.display, 'dark green', ((SCREEN_WIDTH/2) - 150), 300, 275, 75, 'Play again', self.button_font)
        exit_button = Button(self.display, 'dark green', ((SCREEN_WIDTH/2) - 150), 400, 275, 75, 'Exit', self.button_font)
        menu_button.draw()
        play_again_button.draw()
        exit_button.draw()

        if menu_button.is_clicked():
            self.gameStateManager.set_state('home_screen')

        if play_again_button.is_clicked():
            self.gameStateManager.set_state('hole_one')

        if exit_button.is_clicked():
            self.running[0] = False