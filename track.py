import pygame
import math

class Track:
    def __init__(self):
        # 1. Profesyonel F1 Pist Yerleşimi (Teknik şikan ve kavşak hissi veren bölümler)
        # Bu noktalar Catmull-Rom spline ile pürüzsüzleştirilecek.
        self.raw_points = [
            (500, 150), (850, 150), (920, 300), (800, 500), 
            (600, 450), (450, 600), (250, 600), (120, 450), 
            (150, 200), (300, 120)
        ]
        
        # Fiziksel ve Görsel Parametreler
        self.track_width = 115
        self.checkpoint_margin = 65
        
        # Premium Renk Paleti (Gece Yarışı Estetiği)
        self.COLOR_GRASS = (25, 60, 25)        # Koyu doğal yeşil
        self.COLOR_SAND = (180, 160, 100)      # Gravel trap (kum havuzu)
        self.COLOR_ASPHALT = (35, 35, 38)      # F1 Asfaltı
        self.COLOR_RACING_LINE = (25, 25, 28)  # Aşınmış kauçuk izi (yarış çizgisi)
        self.COLOR_LINE = (220, 220, 220)      # Beyaz sınır çizgileri
        self.COLOR_KERB_RED = (190, 20, 20)    # Yarış kırmızısı
        self.COLOR_KERB_WHITE = (245, 245, 245) # Saf beyaz
        
        # Pürüzsüzleştirme (Spline)
        # Subdivisions artırılarak virajlar kusursuz ve akışkan hale getirildi.
        self.subdivisions = 35
        self.center_points = self._generate_smooth_path(self.raw_points, subdivisions=self.subdivisions)
        
        if not pygame.font.get_init(): pygame.font.init()
        self.font = pygame.font.SysFont("Verdana", 16, bold=True)
        
        self.outer_boundary = []
        self.inner_boundary = []
        self.cp_lines = []
        self._setup_geometry()
        
        # RL Verileri
        self.checkpoint_count = len(self.raw_points)
        self.start_x, self.start_y = self.center_points[0]
        
        # Başlangıç açısı hesaplama (İlk düzlüğe doğru)
        dx = self.raw_points[1][0] - self.raw_points[0][0]
        dy = self.raw_points[1][1] - self.raw_points[0][1]
        self.start_angle = math.degrees(math.atan2(-dy, dx))

    def _generate_smooth_path(self, points, subdivisions):
        """Catmull-Rom Spline ile akışkan ve hatasız bir yol üretir."""
        smooth = []
        n = len(points)
        for i in range(n):
            p0, p1, p2, p3 = points[(i-1)%n], points[i], points[(i+1)%n], points[(i+2)%n]
            for j in range(subdivisions):
                t = j / subdivisions
                t2, t3 = t*t, t*t*t
                # Spline katsayıları
                f1 = -0.5*t3 + t2 - 0.5*t
                f2 = 1.5*t3 - 2.5*t2 + 1.0
                f3 = -1.5*t3 + 2.0*t2 + 0.5*t
                f4 = 0.5*t3 - 0.5*t2
                smooth.append((p0[0]*f1 + p1[0]*f2 + p2[0]*f3 + p3[0]*f4,
                               p0[1]*f1 + p1[1]*f2 + p2[1]*f3 + p3[1]*f4))
        return smooth

    def _setup_geometry(self):
        """Pist sınırlarını ve checkpoint hatlarını matematiksel olarak hesaplar."""
        self.outer_boundary, self.inner_boundary, self.cp_lines = [], [], []
        for i in range(len(self.center_points)):
            p1 = pygame.math.Vector2(self.center_points[i])
            p2 = pygame.math.Vector2(self.center_points[(i+1)%len(self.center_points)])
            direction = (p2 - p1).normalize() if p1 != p2 else pygame.math.Vector2(1, 0)
            normal = pygame.math.Vector2(-direction.y, direction.x)
            
            self.outer_boundary.append(p1 + normal * (self.track_width / 2))
            self.inner_boundary.append(p1 - normal * (self.track_width / 2))
            
            # Checkpointleri ana waypointler üzerine yerleştir
            if i % self.subdivisions == 0:
                self.cp_lines.append((self.outer_boundary[-1], self.inner_boundary[-1]))

    def draw(self, screen):
        # 1. Katman: Çim Zemin
        screen.fill(self.COLOR_GRASS)
        
        # 2. Katman: Gravel Traps (Kum Havuzları - Virajların dışına estetik yerleşim)
        sand_locs = [(780, 120, 220, 180), (80, 380, 180, 250), (450, 580, 300, 150)]
        for pos in sand_locs:
            pygame.draw.ellipse(screen, self.COLOR_SAND, pos)

        num_pts = len(self.center_points)
        
        # 3. Katman: Asfalt ve Yarış Çizgisi (Kusursuz segment birleştirme)
        for i in range(num_pts):
            next_i = (i + 1) % num_pts
            # Ana Asfalt
            pygame.draw.polygon(screen, self.COLOR_ASPHALT, [
                self.outer_boundary[i], self.outer_boundary[next_i], 
                self.inner_boundary[next_i], self.inner_boundary[i]
            ])
            # Yarış Çizgisi (Kauçuk aşınma izi)
            r_out = self.center_points[i] + (pygame.math.Vector2(self.outer_boundary[i]) - self.center_points[i]) * 0.25
            r_in = self.center_points[i] + (pygame.math.Vector2(self.inner_boundary[i]) - self.center_points[i]) * 0.25
            r_out_n = self.center_points[next_i] + (pygame.math.Vector2(self.outer_boundary[next_i]) - self.center_points[next_i]) * 0.25
            r_in_n = self.center_points[next_i] + (pygame.math.Vector2(self.inner_boundary[next_i]) - self.center_points[next_i]) * 0.25
            pygame.draw.polygon(screen, self.COLOR_RACING_LINE, [r_out, r_out_n, r_in_n, r_in])

        # 4. Katman: Kerbler ve Sınır Çizgileri
        for i in range(num_pts):
            next_i = (i + 1) % num_pts
            kerb_color = self.COLOR_KERB_RED if (i // 6) % 2 == 0 else self.COLOR_KERB_WHITE
            
            # Beyaz sınır çizgileri
            pygame.draw.line(screen, self.COLOR_LINE, self.outer_boundary[i], self.outer_boundary[next_i], 2)
            pygame.draw.line(screen, self.COLOR_LINE, self.inner_boundary[i], self.inner_boundary[next_i], 2)
            
            # Kalın Yarış Kerbleri (Hafif dışa taşan 3D hissi)
            pygame.draw.line(screen, kerb_color, self.outer_boundary[i], self.outer_boundary[next_i], 6)
            pygame.draw.line(screen, kerb_color, self.inner_boundary[i], self.inner_boundary[next_i], 6)

        # 5. Katman: Checkpointler ve Numaralar
        for i, (p_out, p_in) in enumerate(self.cp_lines):
            if i != 0:
                pygame.draw.line(screen, (80, 80, 80), p_out, p_in, 1)
                txt = self.font.render(str(i), True, (160, 160, 160))
                screen.blit(txt, (p_out.x + 10, p_out.y - 10))

        # 6. Profesyonel Damalı Start/Finish Çizgisi
        s_out, s_in = self.cp_lines[0]
        pygame.draw.line(screen, (255, 255, 255), s_out, s_in, 14)
        for step in range(0, 100, 20):
            p1 = pygame.math.Vector2(s_in).lerp(s_out, step/100)
            p2 = pygame.math.Vector2(s_in).lerp(s_out, (step+10)/100)
            pygame.draw.line(screen, (20, 20, 20), p1, p2, 14)

    def is_on_track(self, x, y):
        """Mesafe tabanlı yüksek kararlılıklı kontrol (RL için kritik)."""
        min_dist = float('inf')
        # Daha hızlı ve pürüzsüz kontrol için her 2 noktada bir bak
        for i in range(0, len(self.center_points), 2):
            p1, p2 = self.center_points[i], self.center_points[(i+1)%len(self.center_points)]
            dist = self._point_to_segment_dist((x, y), p1, p2)
            if dist < min_dist: min_dist = dist
        return min_dist < (self.track_width / 2)

    def check_corners(self, corners):
        """Arabanın 4 köşesini de kontrol eder."""
        for c in corners:
            if not self.is_on_track(c[0], c[1]): return True
        return False

    def check_checkpoint(self, x, y, next_checkpoint_index):
        """Checkpoint geçiş kontrolü (Parametre hatası giderildi)."""
        if next_checkpoint_index >= len(self.raw_points): return False
        target = self.raw_points[next_checkpoint_index]
        return math.hypot(x - target[0], y - target[1]) < self.checkpoint_margin

    def _point_to_segment_dist(self, p, s1, s2):
        """Bir noktanın bir doğru parçasına olan en kısa mesafesi."""
        px, py = p
        x1, y1 = s1
        x2, y2 = s2
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0: return math.hypot(px-x1, py-y1)
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx*dx + dy*dy)))
        return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1250, 900))
    pygame.display.set_caption("F1 Pro Series - Racing Circuit")
    track = Track()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
        track.draw(screen)
        pygame.display.flip()
        clock.tick(60)