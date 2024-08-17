# collisions.py
import pygame
import math
from green import Green
from ball import Ball

class CollisionManager:
    def __init__(self, green):
        self.obstacles = []
        self.green = green
        self.penalty_stroke = False
        self.hole_over = False

    def add_obstacle(self, rect, type, shape = "rectangle"):
        self.obstacles.append({"rect": rect, "type": type, "shape": shape})


    def check_collisions(self, ball):
        for obstacle in self.obstacles:
            if ball.ball_rect.colliderect(obstacle["rect"]):
                self.handle_collision(ball, obstacle)

    def handle_collision(self, ball, obstacle):
        if obstacle["type"] == "edge":
            self.handle_edge_collision(ball, obstacle["rect"])
        elif obstacle["shape"] == "oval":
            self.handle_oval_collision(ball, obstacle["rect"])
        elif obstacle["shape"] == "hole":
            self.handle_hole_collision(ball, obstacle["rect"])
        elif obstacle["shape"] == "rectangle":
            self.handle_rectangle_collision(ball, obstacle["rect"])


    def handle_hole_collision(self, ball, hole_rect):
        # Calculate the center of the oval
        oval_center_x = hole_rect.centerx
        oval_center_y = hole_rect.centery
        radius_x = hole_rect.width / 2
        radius_y = hole_rect.height / 2

        # Calculate the vector from the center of the circle to the center of the ball
        dx = ball.ball_rect.centerx - oval_center_x
        dy = ball.ball_rect.centery - oval_center_y

        if (dx ** 2) / (radius_x ** 2) + (dy ** 2) / (radius_y ** 2) <= 1:
            ball.velocity_x = 5
            ball.velocity_y = 5
            tee_box_center = self.green.get_tee_box_rect().center
            ball.x, ball.y = tee_box_center
            ball.ball_rect.center = tee_box_center
            self.hole_over = True

    def handle_edge_collision(self, ball, edge_rect):
        # Calculate the overlap
        overlap = ball.ball_rect.clip(edge_rect)

        if overlap.width < overlap.height:
            # Collision from the side
            ball.velocity_x *= -0.8  # Reduce horizontal velocity and reverse direction
            if ball.ball_rect.centerx < edge_rect.centerx:
                ball.x = edge_rect.left - ball.ball_rect.width / 2
            else:
                ball.x = edge_rect.right + ball.ball_rect.width / 2
        else:
            # Collision from top/bottom
            ball.velocity_y *= -0.8  # Reduce vertical velocity and reverse direction
            if ball.ball_rect.centery < edge_rect.centery:
                ball.y = edge_rect.top - ball.ball_rect.height / 2
            else:
                ball.y = edge_rect.bottom + ball.ball_rect.height / 2

        # Update ball position
        ball.ball_rect.center = (round(ball.x), round(ball.y))

    def handle_rectangle_collision(self, ball, object_rect):
        # Calculate collision normal
        nx = ball.ball_rect.centerx - object_rect.centerx
        ny = ball.ball_rect.centery - object_rect.centery
        length = math.sqrt(nx**2 + ny**2)
        if length != 0:
            nx /= length
            ny /= length

        # Calculate relative velocity
        relative_velocity = (ball.velocity_x * nx + ball.velocity_y * ny)

        # Apply impulse
        impulse = 2 * relative_velocity
        ball.velocity_x -= impulse * nx * 0.8  # Reduce velocity by 20%
        ball.velocity_y -= impulse * ny * 0.8  # Reduce velocity by 20%

        # Move ball outside of the object
        while ball.ball_rect.colliderect(object_rect):
            ball.x += nx
            ball.y += ny
            ball.ball_rect.center = (round(ball.x), round(ball.y))

    def handle_oval_collision(self, ball, oval_rect):
        # Calculate the center of the oval
        oval_center_x = oval_rect.centerx
        oval_center_y = oval_rect.centery
        radius_x = oval_rect.width / 2
        radius_y = oval_rect.height / 2

        # Calculate the vector from the center of the oval to the center of the ball
        dx = ball.ball_rect.centerx - oval_center_x
        dy = ball.ball_rect.centery - oval_center_y

        # Check if the ball is colliding with the oval using the ellipse equation
        if (dx ** 2) / (radius_x ** 2) + (dy ** 2) / (radius_y ** 2) <= 1:
            self.penalty_stroke = True
            tee_box_center = self.green.get_tee_box_rect().center
            ball.x, ball.y = tee_box_center
            ball.ball_rect.center = tee_box_center
            ball.velocity_x = 5
            ball.velocity_y = 5

    def is_hole_over(self):
        return self.hole_over
    
    def reset_hole_over(self):
        self.hole_over = False

    def reset_penalty_stroke(self):
        self.penalty_stroke = False

    def is_penalty_stroke(self):
        return self.penalty_stroke