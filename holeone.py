# holeone.py
import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from green import Green
from ball import Ball
from collisions import CollisionManager

class HoleOne:
    def __init__(self, display, gameStateManager, running, current_hole, total_strokes, stroke_font, button_font):
        self.display = display
        self.gameStateManager = gameStateManager
        self.running = running
        self.total_strokes = total_strokes
        self.stroke_font = stroke_font
        self.current_hole = current_hole
        self.button_font = button_font
        self.current_strokes = 0
        self.green = Green(self.display, 700, (SCREEN_HEIGHT - 100), 575, 75)
        self.ball = Ball(self.display, self.green)
        self.collision_manager = CollisionManager(self.green)
        self.setup_obstacles()

    def draw_text(self, text, font, text_color, x, y, screen):
        rendered_text = font.render(text, True, text_color)
        text_rect = rendered_text.get_frect(topleft=(x, y))
        screen.blit(rendered_text, text_rect)

    def setup_obstacles(self):
        # Add tree obstacle
        self.tree = pygame.image.load('images/tree.png').convert_alpha()
        self.tree_rect = self.tree.get_frect(center=(800, (SCREEN_HEIGHT / 2) - 30))
        self.collision_manager.add_obstacle(self.tree_rect, "tree", "rectangle")

        # Add pond obstacle with smaller collision box
        self.pond_image = pygame.image.load('images/pond.png').convert_alpha()
        self.pond_rect = self.pond_image.get_frect(center=(500, SCREEN_HEIGHT - 300))
        self.pond_collision_rect = self.pond_rect.inflate(-self.pond_rect.width * 0.05, -self.pond_rect.height * 0.45)
        self.pond_collision_rect.move_ip(0, 30)
        self.collision_manager.add_obstacle(self.pond_collision_rect, "pond", shape="oval")

        # Add green edges
        self.green.add_edges_to_collision_manager(self.collision_manager)

        # Add hole collision
        self.collision_manager.add_obstacle(self.green.get_hole_rect(), "pond", shape="hole")


    def run(self, dt):
        self.display.fill('white')
        self.current_hole[0] = 'hole_one'
        self.draw_text('Hole One', self.button_font, 'black', 0, 0, self.display)
        self.draw_text('Strokes: ' + (str(self.current_strokes)), self.stroke_font, 'black', 0, 50, self.display)
        self.draw_text('Total Strokes: ' + str(self.total_strokes[0]), self.stroke_font, 'black', 0, 75, self.display)

        self.green.draw_green()

        self.display.blit(self.pond_image, self.pond_rect)
        self.display.blit(self.tree, self.tree_rect)

        for event in pygame.event.get():
            self.ball.handle_event(event)
            if (event.type == pygame.QUIT):
                self.running[0] = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.gameStateManager.set_state('home_screen')

        self.ball.update(dt)
        self.collision_manager.check_collisions(self.ball)
        self.ball.draw()


        if self.collision_manager.is_hole_over():
            self.collision_manager.reset_hole_over()
            self.gameStateManager.set_state('round_over')
        else:
            if self.collision_manager.is_penalty_stroke():
                self.current_strokes += 2
                self.total_strokes[0] += 2
                self.collision_manager.reset_penalty_stroke()
                self.ball.reset_stroke_made()
            elif self.ball.is_stroke_made():
                self.current_strokes += 1
                self.total_strokes[0] += 1
                self.ball.reset_stroke_made()

        pygame.display.flip()