import pygame
import time
import math

class Ball:
    def __init__(self, display, green):
        self.display = display
        self.green = green
        self.ball = pygame.image.load('images/ball.png').convert_alpha()
        self.arrow = pygame.image.load('images/arrow.png').convert_alpha()
        self.ball_rect = self.ball.get_rect(center=self.green.get_tee_box_rect().center)
        self.arrow_rect = self.arrow.get_rect(center=self.ball_rect.center)
        self.x = float(self.ball_rect.centerx)  # Floating-point x position
        self.y = float(self.ball_rect.centery)  # Floating-point y position
        self.velocity = 0.0  # Initial velocity
        self.velocity_x = 0.0  # Velocity component in x direction
        self.velocity_y = 0.0  # Velocity component in y direction
        self.angle = 0  # Angle in degrees
        self.is_moving = False
        self.start_time = None
        self.key_held = False
        self.add_stroke = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.is_moving:  # Only allow rotation when the ball isn't moving
                if event.key == pygame.K_LEFT:
                    self.angle += 5  # Rotate left by 5 degrees
                elif event.key == pygame.K_RIGHT:
                    self.angle -= 5  # Rotate right by 5 degrees

            if event.key == pygame.K_UP:
                if not self.is_moving and not self.key_held:
                    self.start_time = time.time()
                    self.key_held = True

        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            if self.key_held:
                self.calculate_velocity()
                self.add_stroke = True
                self.key_held = False

    def calculate_velocity(self):
        if self.start_time is not None:
            hold_duration = time.time() - self.start_time
            self.velocity = min(hold_duration * 200, 500)  # Max velocity cap
            angle_rad = math.radians(self.angle)
            self.velocity_x = self.velocity * math.sin(angle_rad)
            self.velocity_y = -self.velocity * math.cos(angle_rad)
            self.is_moving = True
            self.start_time = None  # Reset start_time for the next use

    def update(self, dt):
        if self.is_moving:
            # Update ball position using velocity components
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt

            # Update the rect position
            self.ball_rect.center = (round(self.x), round(self.y))

            # Apply deceleration
            deceleration = 50
            speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            if speed > 0:
                decel_factor = max(0, speed - deceleration * dt) / speed
                self.velocity_x *= decel_factor
                self.velocity_y *= decel_factor

                # Stop the ball if velocity is very small
                if abs(self.velocity_x) < 1 and abs(self.velocity_y) < 1:
                    self.velocity_x = 0
                    self.velocity_y = 0
                    self.is_moving = False

        # Update arrow position and rotation
        self.update_arrow_position()

    def update_arrow_position(self):
        offset_distance = -25  # Distance of arrow from ball center

        # Convert angle to radians for offset calculation
        angle_rad = math.radians(self.angle)
        offset_x = offset_distance * math.sin(angle_rad)
        offset_y = -offset_distance * math.cos(angle_rad)

        # Position the arrow relative to the ball
        arrow_pos = (self.x + offset_x, self.y + offset_y)
        self.arrow_rotated = pygame.transform.rotate(self.arrow, -self.angle)
        self.arrow_rotated_rect = self.arrow_rotated.get_rect(center=arrow_pos)

    def draw(self):
        self.display.blit(self.ball, self.ball_rect)
        self.display.blit(self.arrow_rotated, self.arrow_rotated_rect)

    def reset_ball_moving(self):
        self.ball_is_moving = False
        
    def reset_stroke_made(self):
        self.add_stroke = False

    def is_stroke_made(self):
        return self.add_stroke