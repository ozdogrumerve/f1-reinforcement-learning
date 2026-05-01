import pygame

class Track:
    def __init__(self):
        # ── Dış duvar (büyük dikdörtgen) ───────────────
        self.outer_wall = [
            (50,  50),
            (950, 50),
            (950, 650),
            (50,  650),
        ]

        # ── İç duvar (küçük dikdörtgen, ortada) ────────
        self.inner_wall = [
            (200, 180),
            (800, 180),
            (800, 520),
            (200, 520),
        ]

        # ── Checkpointler (başlangıçtan saat yönünde) ──
        # Her checkpoint: ((x1,y1), (x2,y2)) → bir çizgi
        self.checkpoints = [
            ((490, 50),  (490, 180)),   # üst düzlük
            ((950, 180), (800, 180)),   # sağ üst köşe
            ((950, 350), (800, 350)),   # sağ orta
            ((950, 520), (800, 520)),   # sağ alt köşe
            ((490, 520), (490, 650)),   # alt düzlük
            ((200, 520), (50,  520)),   # sol alt köşe
            ((200, 350), (50,  350)),   # sol orta
            ((200, 180), (50,  180)),   # sol üst köşe
        ]

        self.checkpoint_count = len(self.checkpoints)

        # ── Başlangıç pozisyonu ve açısı ───────────────
        self.start_x     = 490
        self.start_y     = 120
        self.start_angle = 0  
        
        # ── Renkler ────────────────────────────────────
        self.color_track      = (60,  60,  60)   # gri asfalt
        self.color_outer      = (30,  30,  30)   # koyu gri dış
        self.color_inner      = (34,  139, 34)   # yeşil iç alan
        self.color_checkpoint = (255, 255,  0)   # sarı checkpoint
        self.color_start      = (255, 255, 255)  # beyaz start

    # ── Çizim ──────────────────────────────────────────
    def draw(self, screen):
        # Arka plan (pist dışı)
        screen.fill((20, 20, 20))

        # Asfalt (dış polygon doldur)
        pygame.draw.polygon(screen, self.color_track, self.outer_wall)

        # İç alan (yeşil)
        pygame.draw.polygon(screen, self.color_inner, self.inner_wall)

        # Duvarlar
        pygame.draw.polygon(screen, self.color_outer, self.outer_wall, 4)
        pygame.draw.polygon(screen, self.color_outer, self.inner_wall, 4)

        # Checkpointler
        for i, (p1, p2) in enumerate(self.checkpoints):
            pygame.draw.line(screen, self.color_checkpoint, p1, p2, 2)

        # Start çizgisi
        pygame.draw.line(screen, self.color_start,
                         (450, 50), (450, 180), 3)

    # ── Çarpışma kontrolü ──────────────────────────────
    def is_on_track(self, x, y):
        # Önce basit rect kontrolü yap, polygon pahalı
        if x < 50 or x > 950 or y < 50 or y > 650:
            return False
        return (
            self._point_in_polygon(x, y, self.outer_wall) and
            not self._point_in_polygon(x, y, self.inner_wall)
        )
    
    def check_corners(self, corners):
        """Arabanın 4 köşesinden herhangi biri pist dışındaysa True döner."""
        for (cx, cy) in corners:
            if not self.is_on_track(cx, cy):
                return True
        return False

    # ── Checkpoint geçiş kontrolü ──────────────────────
    def check_checkpoint(self, x, y, next_checkpoint_index):
        if next_checkpoint_index >= self.checkpoint_count:
            return False
        p1, p2 = self.checkpoints[next_checkpoint_index]
        return self._point_near_line(x, y, p1, p2, threshold=18)

    # ── Yardımcı: Nokta polygon içinde mi? (Ray casting) 
    def _point_in_polygon(self, x, y, polygon):
        n       = len(polygon)
        inside  = False
        px, py  = x, y
        j       = n - 1
        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            if ((yi > py) != (yj > py) and
                    px < (xj - xi) * (py - yi) / (yj - yi + 1e-9) + xi):
                inside = not inside
            j = i
        return inside

    # ── Yardımcı: Nokta çizgiye yakın mı? ─────────────
    def _point_near_line(self, x, y, p1, p2, threshold=18):
        x1, y1 = p1
        x2, y2 = p2
        # Çizgi üzerindeki en yakın noktaya mesafe
        dx, dy  = x2 - x1, y2 - y1
        length  = (dx**2 + dy**2) ** 0.5
        if length == 0:
            return False
        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (length**2)))
        nearest_x = x1 + t * dx
        nearest_y = y1 + t * dy
        dist = ((x - nearest_x)**2 + (y - nearest_y)**2) ** 0.5
        return dist < threshold