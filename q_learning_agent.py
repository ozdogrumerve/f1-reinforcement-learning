import numpy as np
import os
import pickle
from config import (
    LEARNING_RATE, GAMMA,
    EPSILON_START, EPSILON_END, EPSILON_DECAY,
    MODEL_DIR
)

# Sensör mesafelerini 3 kategoriye ayır
def discretize(value):
    """0.0-1.0 arası normalize değeri 3 kategoriye çevirir."""
    if value < 0.2:
        return 0   # çok yakın
    elif value < 0.5:
        return 1   # orta
    else:
        return 2   # uzak

def discretize_speed(value):
    """Hızı 3 kategoriye çevirir."""
    if value < 0.1:
        return 0    # yavaş / durgun
    elif value < 0.4:
        return 1     # orta hız
    else:
        return 2    # hızlı

class QLearningAgent:
    def __init__(self, action_count=5):
        self.action_count = action_count
        self.epsilon      = EPSILON_START

        # Q-table: (s0, s1, s2, s3, s4, hız) → 5 aksiyon
        # Her sensör 3 kategori, hız 3 kategori
        # Toplam state sayısı: 3^5 * 3 = 729
        self.q_table = {}

    # ── State'i anahtar'a çevir ────────────────────────
    def _state_to_key(self, state):
        sensors = [discretize(s) for s in state[:5]]
        speed   = discretize_speed(state[5])
        return tuple(sensors + [speed])

    # ── Q değerlerini al (yoksa oluştur) ──────────────
    def _get_q_values(self, key):
        if key not in self.q_table:
            self.q_table[key] = np.zeros(self.action_count)
        return self.q_table[key]

    # ── Aksiyon seç (epsilon-greedy) ──────────────────
    def choose_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.action_count)  # keşif
        key = self._state_to_key(state)
        return int(np.argmax(self._get_q_values(key)))   # sömürü

    # ── Q-table güncelle ──────────────────────────────
    def update(self, state, action, reward, next_state, done):
        key      = self._state_to_key(state)
        next_key = self._state_to_key(next_state)

        q_values      = self._get_q_values(key)
        next_q_values = self._get_q_values(next_key)

        if done:
            target = reward
        else:
            target = reward + GAMMA * np.max(next_q_values)

        q_values[action] += LEARNING_RATE * (target - q_values[action])

    # ── Epsilon güncelle ──────────────────────────────
    def decay_epsilon(self):
        self.epsilon = max(EPSILON_END, self.epsilon * EPSILON_DECAY)

    # ── Kaydet ────────────────────────────────────────
    def save(self, filename="q_table.pkl"):
        os.makedirs(MODEL_DIR, exist_ok=True)
        path = os.path.join(MODEL_DIR, filename)
        with open(path, "wb") as f:
            pickle.dump({
                "q_table": self.q_table,
                "epsilon": self.epsilon
            }, f)
        print(f"💾 Kaydedildi: {path} ({len(self.q_table)} state)")

    # ── Yükle ─────────────────────────────────────────
    def load(self, filename="q_table.pkl"):
        if os.path.dirname(filename):
            path = filename
        else:
            path = os.path.join(MODEL_DIR, filename)
            
        if not os.path.exists(path):
            print(f"⚠️  Model bulunamadı: {path}")
            return False
        with open(path, "rb") as f:
            data = pickle.load(f)
        self.q_table = data["q_table"]
        self.epsilon = data["epsilon"]
        print(f"✅ Yüklendi: {path} ({len(self.q_table)} state)")
        return True