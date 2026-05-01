import os
from environment import Environment
from q_learning_agent import QLearningAgent
from config import (
    MAX_EPISODES, SAVE_INTERVAL,
    LOG_DIR, MODEL_DIR
)

def train():
    env   = Environment(headless=True)
    agent = QLearningAgent()

    # Daha önce kaydedilmiş model varsa yükle
    agent.load()

    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, "training_log.csv")

    # Log dosyası başlığı
    with open(log_path, "w") as f:
        f.write("episode,total_reward,steps,checkpoints,laps,epsilon\n")

    best_reward = float("-inf")

    print("🏁 Eğitim başlıyor...\n")

    for episode in range(1, MAX_EPISODES + 1):
        state = env.reset()
        done  = False

        ep_reward     = 0
        ep_steps      = 0
        ep_checkpoint = 0

        while not done:
            action                         = agent.choose_action(state)
            next_state, reward, done, info = env.step(action)
            agent.update(state, action, reward, next_state, done)
            state       = next_state
            ep_reward  += reward
            ep_steps   += 1

        ep_checkpoint = info["checkpoint"]
        ep_laps       = info["lap"]

        agent.decay_epsilon()

        # ── Periyodik kayıt ───────────────────────────
        if episode % SAVE_INTERVAL == 0:
            agent.save(f"q_table_ep{episode}.pkl")

        # ── En iyi modeli kaydet ───────────────────────
        if ep_reward > best_reward:
            best_reward = ep_reward
            agent.save("q_table_best.pkl")

        # ── Log ───────────────────────────────────────
        with open(log_path, "a") as f:
            f.write(f"{episode},{ep_reward:.1f},{ep_steps},"
                    f"{ep_checkpoint},{ep_laps},{agent.epsilon:.4f}\n")

        # ── Terminal çıktısı ──────────────────────────
        if episode % 10 == 0:
            print(
                f"Episode {episode:4d} | "
                f"Reward: {ep_reward:7.1f} | "
                f"Steps: {ep_steps:4d} | "
                f"Checkpoint: {ep_checkpoint} | "
                f"Epsilon: {agent.epsilon:.3f} | "
                f"Q-states: {len(agent.q_table)}"
            )

    print(f"\n✅ Eğitim tamamlandı!")
    print(f"   En iyi reward : {best_reward:.1f}")
    print(f"   Q-table boyutu: {len(agent.q_table)}")
    agent.save("q_table_final.pkl")

if __name__ == "__main__":
    train()