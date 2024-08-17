# green.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Green:
    def __init__(self, display, sizex, sizey, holex, holey):
        self.display = display
        self.sizex = sizex
        self.sizey = sizey
        self.holex = holex
        self.holey = holey
        self.green_rect = None
        self.tee_box_rect = None
        self.draw_green()

    def draw_green(self):
        # Create and draw green
        green = pygame.Surface((self.sizex, self.sizey))
        self.green_rect = green.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        green.fill(pygame.Color('forest green'))
        self.display.blit(green, self.green_rect)

        # Create and draw border
        edge_color = pygame.Color('brown')
        edge_thickness = 20  # Thickness of the hollow rectangle's edges
        pygame.draw.rect(self.display, edge_color, self.green_rect, edge_thickness)

        # Create and draw hole
        hole_radius = 25
        hole_center = (self.green_rect.left + self.holex, self.green_rect.top + self.holey)
        self.hole_rect = pygame.Rect(hole_center[0] - hole_radius, hole_center[1] - hole_radius, hole_radius * 2, hole_radius * 2)
        pygame.draw.circle(self.display, pygame.Color('white'), hole_center, hole_radius)

        # Create and draw tee box
        tee_box = pygame.Surface((75, 75))
        self.tee_box_rect = tee_box.get_rect(bottomleft=(self.green_rect.bottomleft[0] + 20, self.green_rect.bottomleft[1] - 20))
        tee_box.fill(pygame.Color('dark green'))
        self.display.blit(tee_box, self.tee_box_rect)

    def get_tee_box_rect(self):
        return self.tee_box_rect
    
    def get_hole_rect(self):
        return self.hole_rect
    

    def add_edges_to_collision_manager(self, collision_manager):
        edge_thickness = 20
        top_edge = pygame.Rect(self.green_rect.left, self.green_rect.top, self.green_rect.width, edge_thickness)
        bottom_edge = pygame.Rect(self.green_rect.left, self.green_rect.bottom - edge_thickness, self.green_rect.width, edge_thickness)
        left_edge = pygame.Rect(self.green_rect.left, self.green_rect.top, edge_thickness, self.green_rect.height)
        right_edge = pygame.Rect(self.green_rect.right - edge_thickness, self.green_rect.top, edge_thickness, self.green_rect.height)

        collision_manager.add_obstacle(top_edge, "edge", "rectangle")
        collision_manager.add_obstacle(bottom_edge, "edge", "rectangle")
        collision_manager.add_obstacle(left_edge, "edge", "rectangle")
        collision_manager.add_obstacle(right_edge, "edge", "rectangle")