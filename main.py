import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from car import Car
from track import Track

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("F1 Reinforcement Learning - Test")
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont("Arial", 18)

    track = Track()
    car   = Car(track.start_x, track.start_y, track.start_angle)

    next_checkpoint = 0
    total_reward    = 0
    laps            = 0

    while True:
        # ── Event ───────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:   # R → reset
                    car.reset(track.start_x, track.start_y, track.start_angle)
                    next_checkpoint = 0
                    total_reward    = 0

        # ── Klavye input ────────────────────────────────
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:    car.accelerate()
        if keys[pygame.K_DOWN]:  car.brake()
        if keys[pygame.K_LEFT]:  car.turn_left()
        if keys[pygame.K_RIGHT]: car.turn_right()

        # ── Güncelle ────────────────────────────────────
        car.update()

        # ── Çarpışma kontrolü ───────────────────────────
        corners = car.get_corners()
        if track.check_corners(corners):
            total_reward += -100
            print(f"💥 Çarpışma! Toplam reward: {total_reward}")
            car.reset(track.start_x, track.start_y, track.start_angle)
            next_checkpoint = 0

        # ── Checkpoint kontrolü ─────────────────────────
        if track.check_checkpoint(car.x, car.y, next_checkpoint):
            total_reward    += 20
            next_checkpoint += 1
            print(f"✅ Checkpoint {next_checkpoint} geçildi! Reward: {total_reward}")

            if next_checkpoint >= track.checkpoint_count:
                next_checkpoint = 0
                laps += 1
                print(f"🏁 Tur tamamlandı! Toplam tur: {laps}")

        # ── Çizim ───────────────────────────────────────
        track.draw(screen)
        car.draw(screen)

        # ── HUD ─────────────────────────────────────────
        hud_lines = [
            f"Hız: {car.speed:.2f}",
            f"Açı: {car.angle:.1f}°",
            f"Checkpoint: {next_checkpoint}/{track.checkpoint_count}",
            f"Tur: {laps}",
            f"Reward: {total_reward}",
            f"[R] Reset  [↑↓←→] Hareket",
        ]
        for i, line in enumerate(hud_lines):
            surf = font.render(line, True, (255, 255, 255))
            screen.blit(surf, (10, 10 + i * 22))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()