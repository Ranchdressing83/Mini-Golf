import pygame

class Button:
    def __init__(self, screen, color, x, y, width, height, text='', font=None, text_color=(255, 255, 255)):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font if font else pygame.font.Font(None, 50)  # Default font size 50
        self.text_color = text_color

    def draw(self):
        # Draw the button rectangle
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
        
        if self.text != '':
            # Render the text
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            # Draw the text on the button
            self.screen.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]  # Detect left mouse button click
        return self.is_hovered(mouse_pos) and mouse_clicked