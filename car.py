import pygame
import math

# Not: CAR_SPEED_MAX, CAR_ACCELERATION, CAR_FRICTION, CAR_TURN_SPEED 
# değerlerinin config.py dosyasında tanımlı olduğu varsayılmıştır.

class Car:
    def __init__(self, x, y, angle=0):
        self.x = float(x)
        self.y = float(y)
        self.angle = float(angle)  # 0 = Sağa bakıyor (Derece)
        self.speed = 0.0
        self.alive = True

        # --- Fiziksel Boyutlar (Görsel ölçekle uyumlu) ---
        self.width = 15   # Tekerlekler dahil toplam genişlik
        self.height = 35  # Burundan arka kanada toplam uzunluk
        
        # Profesyonel Renk Paleti
        self.COLOR_BODY = (220, 10, 10)      # Canlı F1 Kırmızısı
        self.COLOR_OUTLINE = (0, 0, 0)      # Keskin dış hatlar
        self.COLOR_WHEEL = (25, 25, 25)     # Lastik siyahı
        self.COLOR_WING = (45, 45, 45)      # Kanat/Karbon fiber rengi
        self.COLOR_HALO = (240, 240, 240)   # Kask/Halo beyazı
        self.COLOR_ACCENT = (255, 255, 255) # Detay çizgileri

    def accelerate(self):
        from config import CAR_ACCELERATION, CAR_SPEED_MAX
        self.speed = min(self.speed + CAR_ACCELERATION, CAR_SPEED_MAX)

    def brake(self):
        from config import CAR_ACCELERATION, CAR_SPEED_MAX
        self.speed = max(self.speed - CAR_ACCELERATION, -CAR_SPEED_MAX / 2)

    def turn_left(self):
        from config import CAR_TURN_SPEED
        self.angle -= CAR_TURN_SPEED

    def turn_right(self):
        from config import CAR_TURN_SPEED
        self.angle += CAR_TURN_SPEED

    def update(self):
        from config import CAR_FRICTION
        # Sürtünme dinamiği
        if self.speed > 0:
            self.speed = max(self.speed - CAR_FRICTION, 0)
        elif self.speed < 0:
            self.speed = min(self.speed + CAR_FRICTION, 0)

        # Pozisyon güncelleme
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

    def reset(self, x, y, angle=0):
        self.x = float(x)
        self.y = float(y)
        self.angle = float(angle)
        self.speed = 0.0
        self.alive = True

    def _get_rotated_point(self, local_x, local_y):
        """Lokal (merkez 0,0) koordinatı dünya koordinatına çevirir."""
        rad = math.radians(self.angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        rx = self.x + (local_x * cos_a - local_y * sin_a)
        ry = self.y + (local_x * sin_a + local_y * cos_a)
        return (rx, ry)

    def get_corners(self):
        """Çarpışma algılama için aracın dış hitbox noktaları."""
        # Görsel araç 75 birim, ancak hitbox biraz daha dar tutulabilir
        h, w = 35, 12 
        return [
            self._get_rotated_point(h, w),
            self._get_rotated_point(h, -w),
            self._get_rotated_point(-h, -w),
            self._get_rotated_point(-h, w)
        ]

    def _draw_rotated_poly(self, screen, color, points, outline=True):
        """Lokal noktaları döndürüp ekrana çizer."""
        world_points = [self._get_rotated_point(p[0], p[1]) for p in points]
        pygame.draw.polygon(screen, color, world_points)
        if outline:
            pygame.draw.polygon(screen, self.COLOR_OUTLINE, world_points, 2)

    def draw(self, screen):
        if not self.alive:
            return

        # 1. ARKA KANAT (En alt katman)
        rear_wing = [(-30, -18), (-30, 18), (-42, 18), (-42, -18)]
        self._draw_rotated_poly(screen, self.COLOR_WING, rear_wing)
        # Arka kanat destekleri
        self._draw_rotated_poly(screen, self.COLOR_BODY, [(-25, -5), (-30, -5), (-30, 5), (-25, 5)], False)

        # 2. TEKERLEKLER (Geniş ve belirgin)
        # Ön Tekerlekler
        self._draw_rotated_poly(screen, self.COLOR_WHEEL, [(22, 11), (22, 20), (5, 20), (5, 11)])
        self._draw_rotated_poly(screen, self.COLOR_WHEEL, [(22, -11), (22, -20), (5, -20), (5, -11)])
        # Arka Tekerlekler (Daha geniş)
        self._draw_rotated_poly(screen, self.COLOR_WHEEL, [(-15, 12), (-15, 23), (-35, 23), (-35, 12)])
        self._draw_rotated_poly(screen, self.COLOR_WHEEL, [(-15, -12), (-15, -23), (-35, -23), (-35, -12)])

        # 3. ÖN KANAT
        # Ana plaka
        front_wing = [(40, -20), (40, 20), (30, 20), (30, -20)]
        self._draw_rotated_poly(screen, self.COLOR_WING, front_wing)
        # Kanat kenar plakaları (Endplates)
        self._draw_rotated_poly(screen, self.COLOR_WING, [(42, 18), (42, 21), (30, 21), (30, 18)], False)
        self._draw_rotated_poly(screen, self.COLOR_WING, [(42, -18), (42, -21), (30, -21), (30, -18)], False)

        # 4. ANA GÖVDE (Aerodinamik F1 Şasisi)
        # Burun -> Sidepods -> Motor Kapağı
        body_points = [
            (40, 0),    # Burun ucu
            (30, 4),    # Burun genişleme
            (10, 6),    # Ön gövde
            (-5, 13),   # Sağ Sidepod dış
            (-25, 12),  # Sağ Sidepod arka
            (-30, 7),   # Arka gövde sağ
            (-30, -7),  # Arka gövde sol
            (-25, -12), # Sol Sidepod arka
            (-5, -13),  # Sol Sidepod dış
            (10, -6),   # Ön gövde sol
            (30, -4)    # Burun sol
        ]
        self._draw_rotated_poly(screen, self.COLOR_BODY, body_points)

        # 5. KOKPİT VE HALO
        # Kokpit boşluğu
        cockpit = [(2, -4), (8, -3), (12, 0), (8, 3), (2, 4), (-10, 0)]
        self._draw_rotated_poly(screen, self.COLOR_OUTLINE, cockpit, False)
        # Sürücü Kaskı (Halo)
        self._draw_rotated_poly(screen, self.COLOR_HALO, [(2, -2), (6, -1), (8, 0), (6, 1), (2, 2), (-2, 0)])

        # 6. GÖRSEL DETAYLAR (Yarış çizgileri)
        stripe = [(30, -1), (30, 1), (15, 1), (15, -1)]
        self._draw_rotated_poly(screen, self.COLOR_ACCENT, stripe, False)
        
        # 7. BURUN ÇİZGİSİ (Yön belirteci olarak)
        nose_tip = self._get_rotated_point(40, 0)
        center = (self.x, self.y)
        pygame.draw.line(screen, self.COLOR_ACCENT, center, nose_tip, 1)