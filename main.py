import pygame
import sys
import io

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from car import Car
from track import Track
from sensor import SensorSystem

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    pygame.init()

    # Oyunun kendi sabit çalışma alanı
    VIRTUAL_WIDTH = SCREEN_WIDTH
    VIRTUAL_HEIGHT = SCREEN_HEIGHT

    fullscreen = False
    screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("F1 Reinforcement Learning - Test")

    game_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    zoom = 1.0

    track = Track()
    car = Car(track.start_x, track.start_y, track.start_angle)
    sensors = SensorSystem()

    next_checkpoint = 0
    total_reward = 0
    laps = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if fullscreen:
                        fullscreen = False
                        screen = pygame.display.set_mode(
                            (VIRTUAL_WIDTH, VIRTUAL_HEIGHT),
                            pygame.RESIZABLE
                        )
                    else:
                        pygame.quit()
                        sys.exit()

                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)

                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    zoom = min(zoom + 0.1, 2.0)

                if event.key == pygame.K_MINUS:
                    zoom = max(zoom - 0.1, 0.5)

                if event.key == pygame.K_0:
                    zoom = 1.0

                if event.key == pygame.K_r:
                    car.reset(track.start_x, track.start_y, track.start_angle)
                    next_checkpoint = 0
                    total_reward = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            car.accelerate()
        if keys[pygame.K_DOWN]:
            car.brake()
        if keys[pygame.K_LEFT]:
            car.turn_left()
        if keys[pygame.K_RIGHT]:
            car.turn_right()

        car.update()
        sensors.update(car.x, car.y, car.angle, track)

        corners = car.get_corners()
        if track.check_corners(corners):
            total_reward += -100
            print(f"💥 Çarpışma! Toplam reward: {total_reward}")
            car.reset(track.start_x, track.start_y, track.start_angle)
            next_checkpoint = 0

        if track.check_checkpoint(car.x, car.y, next_checkpoint):
            total_reward += 20
            next_checkpoint += 1
            print(f"✅ Checkpoint {next_checkpoint} geçildi! Reward: {total_reward}")

            if next_checkpoint >= track.checkpoint_count:
                next_checkpoint = 0
                laps += 1
                print(f"🏁 Tur tamamlandı! Toplam tur: {laps}")

        game_surface.fill((0, 0, 0))

        track.draw(game_surface)
        car.draw(game_surface)
        sensors.draw(game_surface, car.x, car.y)

        hud_lines = [
            f"Hız: {car.speed:.2f}",
            f"Açı: {car.angle:.1f}°",
            f"Checkpoint: {next_checkpoint}/{track.checkpoint_count}",
            f"Tur: {laps}",
            f"Reward: {total_reward}",
            f"[R] Reset  [↑↓←→] Hareket",
            f"[F11] Fullscreen [ESC]  Pencere/Çıkış",
            f"Sensörler: {[f'{r:.0f}' for r in sensors.readings]}",
        ]

        screen_w, screen_h = screen.get_size()

        HUD_WIDTH = 260

        available_w = screen_w - HUD_WIDTH
        available_h = screen_h

        base_scale = min(available_w / VIRTUAL_WIDTH, available_h / VIRTUAL_HEIGHT)
        final_scale = base_scale * zoom

        scaled_w = int(VIRTUAL_WIDTH * final_scale)
        scaled_h = int(VIRTUAL_HEIGHT * final_scale)

        scaled_surface = pygame.transform.smoothscale(game_surface, (scaled_w, scaled_h))

        offset_x = HUD_WIDTH + (available_w - scaled_w) // 2
        offset_y = (screen_h - scaled_h) // 2

        screen.fill((10, 30, 10))

        # Sol HUD paneli
        pygame.draw.rect(screen, (15, 15, 18), (0, 0, HUD_WIDTH, screen_h))

        screen.blit(scaled_surface, (offset_x, offset_y))
        for i, line in enumerate(hud_lines):
            surf = font.render(line, True, (255, 255, 255))
            screen.blit(surf, (15, 20 + i * 28))
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()