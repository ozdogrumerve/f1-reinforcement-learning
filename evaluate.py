import pygame
import sys
from environment import Environment
from q_learning_agent import QLearningAgent
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MODEL_DIR
import os

def evaluate(model_file="q_table_best.pkl", episodes=5):
    # Görsel mod açık
    env   = Environment(headless=False)
    agent = QLearningAgent()

    # Modeli yükle
    if not agent.load(model_file):
        print("❌ Model bulunamadı, önce train.py çalıştır.")
        return

    # Değerlendirme modunda epsilon = 0 (rastgele hareket yok)
    agent.epsilon = 0.0

    font = pygame.font.SysFont("Arial", 18)

    print(f"\n🏁 Değerlendirme başlıyor — {episodes} episode")
    print(f"   Model: {model_file}")
    print(f"   Epsilon: {agent.epsilon} (tam öğrenilmiş davranış)\n")

    total_rewards    = []
    total_checkpoints = []
    total_laps       = []

    for episode in range(1, episodes + 1):
        state    = env.reset()
        done     = False
        ep_reward = 0

        while not done:
            # Event kontrolü (pencere kapatma)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            action                         = agent.choose_action(state)
            state, reward, done, info      = env.step(action)
            ep_reward                     += reward

            # Çizim
            env.track.draw(env.screen)
            env.car.draw(env.screen)
            env.sensors.draw(env.screen, env.car.x, env.car.y)

            # HUD
            hud = [
                f"Episode : {episode}/{episodes}",
                f"Reward  : {ep_reward:.1f}",
                f"Steps   : {info['steps']}",
                f"Checkpoint: {info['checkpoint']}/{env.track.checkpoint_count}",
                f"Lap     : {info['lap']}",
                f"Hız     : {info['speed']:.2f}",
                f"[Q] Çıkış",
            ]
            for i, line in enumerate(hud):
                surf = font.render(line, True, (255, 255, 255))
                env.screen.blit(surf, (10, 10 + i * 22))

            pygame.display.flip()
            env.clock.tick(FPS)

        total_rewards.append(ep_reward)
        total_checkpoints.append(info["checkpoint"])
        total_laps.append(info["lap"])

        print(
            f"Episode {episode} | "
            f"Reward: {ep_reward:8.1f} | "
            f"Checkpoint: {info['checkpoint']} | "
            f"Lap: {info['lap']}"
        )

    print(f"\n📊 Özet:")
    print(f"   Ort. Reward    : {sum(total_rewards)/len(total_rewards):.1f}")
    print(f"   En iyi Reward  : {max(total_rewards):.1f}")
    print(f"   Ort. Checkpoint: {sum(total_checkpoints)/len(total_checkpoints):.1f}")
    print(f"   Toplam Tur     : {sum(total_laps)}")

    pygame.quit()

if __name__ == "__main__":
    evaluate(model_file="models/q_table_best.pkl", episodes=5)