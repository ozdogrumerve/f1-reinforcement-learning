import pygame
import math
from config import (
    CAR_SPEED_MAX, CAR_ACCELERATION,
    CAR_FRICTION, CAR_TURN_SPEED
)

class Car:
    def __init__(self, x, y, angle=0):
        self.x      = float(x)
        self.y      = float(y)
        self.angle  = float(angle)  # 0 = sağa bakıyor, derece cinsinden
        self.speed  = 0.0
        self.alive  = True

        # Görsel
        self.width  = 20
        self.height = 35
        self.color  = (220, 50, 50)

    # ── Hareket ────────────────────────────────────────
    def accelerate(self):
        self.speed = min(self.speed + CAR_ACCELERATION, CAR_SPEED_MAX)

    def brake(self):
        self.speed = max(self.speed - CAR_ACCELERATION, -CAR_SPEED_MAX / 2)

    def turn_left(self):
        self.angle -= CAR_TURN_SPEED

    def turn_right(self):
        self.angle += CAR_TURN_SPEED

    def update(self):
        # Sürtünme
        if self.speed > 0:
            self.speed = max(self.speed - CAR_FRICTION, 0)
        elif self.speed < 0:
            self.speed = min(self.speed + CAR_FRICTION, 0)

        # Pozisyon güncelle
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

    def reset(self, x, y, angle=0):
        self.x      = float(x)
        self.y      = float(y)
        self.angle  = float(angle)
        self.speed  = 0.0
        self.alive  = True

    # ── Köşe noktaları (çarpışma & çizim için) ─────────
    def get_corners(self):
        rad = math.radians(self.angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        w, h = self.width / 2, self.height / 2

        corners = [
            (-w, -h), ( w, -h),
            ( w,  h), (-w,  h)
        ]
        rotated = []
        for cx, cy in corners:
            rx = self.x + cx * cos_a - cy * sin_a
            ry = self.y + cx * sin_a + cy * cos_a
            rotated.append((rx, ry))
        return rotated

    def get_rect(self):
        return pygame.Rect(self.x - self.width / 2,
                           self.y - self.height / 2,
                           self.width, self.height)

    # ── Çizim ──────────────────────────────────────────
    def draw(self, screen):
        corners = self.get_corners()
        pygame.draw.polygon(screen, self.color, corners)

        # Yön göstergesi (küçük çizgi, aracın önü)
        rad = math.radians(self.angle)
        front_x = self.x + math.cos(rad) * (self.height / 2 + 5)
        front_y = self.y + math.sin(rad) * (self.height / 2 + 5)
        pygame.draw.line(screen, (255, 255, 255),
                         (int(self.x), int(self.y)),
                         (int(front_x), int(front_y)), 2)