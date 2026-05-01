# ── Ekran ──────────────────────────────────────────
SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 700
FPS           = 60
HEADLESS      = False   # Eğitimde True yap → hız artar

# ── Araba ──────────────────────────────────────────
CAR_SPEED_MAX    = 6
CAR_ACCELERATION = 0.3
CAR_FRICTION     = 0.05
CAR_TURN_SPEED   = 3      # derece / frame

# ── Sensör ─────────────────────────────────────────
SENSOR_COUNT     = 5
SENSOR_MAX_RANGE = 200    # piksel
SENSOR_ANGLES    = [-60, -30, 0, 30, 60]  # arabaya göre derece

# ── Ortam ──────────────────────────────────────────
MAX_STEPS_PER_EPISODE = 2000

# ── Reward ─────────────────────────────────────────
REWARD_ALIVE        =  1
REWARD_CHECKPOINT   =  20
REWARD_CRASH        = -100
REWARD_SLOW         = -1
REWARD_FORWARD      =  2
REWARD_BACKWARD     = -5

# ── Q-Learning ─────────────────────────────────────
LEARNING_RATE  = 0.1
GAMMA          = 0.95
EPSILON_START  = 1.0
EPSILON_END    = 0.05
EPSILON_DECAY  = 0.995

# ── Eğitim ─────────────────────────────────────────
MAX_EPISODES   = 1000
SAVE_INTERVAL  = 100      # her 100 episode'da Q-table kaydet

# ── Dosya Yolları ───────────────────────────────────
MODEL_DIR = "models/"
LOG_DIR   = "logs/"