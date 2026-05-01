import math
from config import SENSOR_COUNT, SENSOR_MAX_RANGE, SENSOR_ANGLES

class SensorSystem:
    def __init__(self):
        self.readings = [SENSOR_MAX_RANGE] * SENSOR_COUNT
        # Her ışının son nokta koordinatları (çizim için)
        self.endpoints = [(0, 0)] * SENSOR_COUNT

    def update(self, car_x, car_y, car_angle, track):
        for i, offset_angle in enumerate(SENSOR_ANGLES):
            angle_rad = math.radians(car_angle + offset_angle)
            dist, endpoint = self._cast_ray(
                car_x, car_y, angle_rad, track
            )
            self.readings[i]  = dist
            self.endpoints[i] = endpoint

    def get_normalized(self):
        """0.0 - 1.0 arası normalize edilmiş mesafeler."""
        return [r / SENSOR_MAX_RANGE for r in self.readings]

    def _cast_ray(self, x, y, angle_rad, track):
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        # 1'er piksel yerine 3'er piksel atla → 3x hızlı
        for dist in range(1, SENSOR_MAX_RANGE + 1, 3):
            px = x + cos_a * dist
            py = y + sin_a * dist
            if not track.is_on_track(px, py):
                return dist, (px, py)

        end_x = x + cos_a * SENSOR_MAX_RANGE
        end_y = y + sin_a * SENSOR_MAX_RANGE
        return SENSOR_MAX_RANGE, (end_x, end_y)

    def draw(self, screen, car_x, car_y):
        import pygame
        for i, endpoint in enumerate(self.endpoints):
            ratio = self.readings[i] / SENSOR_MAX_RANGE
            r = int(255 * (1 - ratio))
            g = int(255 * ratio)
            color = (r, g, 0)

            pygame.draw.line(
                screen, color,
                (int(car_x), int(car_y)),
                (int(endpoint[0]), int(endpoint[1])), 1
            )