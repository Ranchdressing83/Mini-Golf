# homescreen.py
import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from button import Button

class HomeScreen:
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
        self.display.fill('white')
        
        # Load and position the background image
        background = pygame.image.load('images/background.png').convert_alpha()
        background_rect = background.get_frect(center=(SCREEN_WIDTH - 275, SCREEN_HEIGHT / 2))
        self.display.blit(background, background_rect)

        self.draw_text('Main Menu', self.large_font, (0, 0, 0), SCREEN_WIDTH / 2, 75, self.display)

        start_button = Button(self.display, 'black', 300, 200, 225, 75, 'Start', self.button_font)
        resume_button = Button(self.display, 'black', 300, 300, 225, 75, 'Resume', self.button_font)
        exit_button = Button(self.display, 'black', 300, 400, 225, 75, 'Exit', self.button_font)
        start_button.draw()
        resume_button.draw()
        exit_button.draw()

        if start_button.is_clicked():
            self.gameStateManager.set_state('hole_one')

        if resume_button.is_clicked():
            self.gameStateManager.set_state(self.current_hole[0])

        if exit_button.is_clicked():
            self.running[0] = False