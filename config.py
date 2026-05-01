# ── Ekran ──────────────────────────────────────────
SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 700
FPS           = 60
HEADLESS      = True

# ── Araba ──────────────────────────────────────────
CAR_SPEED_MAX    = 6
CAR_ACCELERATION = 0.3
CAR_FRICTION     = 0.05
CAR_TURN_SPEED   = 3

# ── Sensör ─────────────────────────────────────────
SENSOR_COUNT     = 5
SENSOR_MAX_RANGE = 150
SENSOR_ANGLES    = [-60, -30, 0, 30, 60]

# ── Ortam ──────────────────────────────────────────
MAX_STEPS_PER_EPISODE = 2000

# ── Reward ─────────────────────────────────────────
REWARD_ALIVE        =  2
REWARD_CHECKPOINT   =  50
REWARD_CRASH        = -50
REWARD_SLOW         = -0.5
REWARD_FORWARD      =  3
REWARD_BACKWARD     = -2

# ── Q-Learning ─────────────────────────────────────
LEARNING_RATE  = 0.1
GAMMA          = 0.95
EPSILON_START  = 1.0
EPSILON_END    = 0.05
EPSILON_DECAY  = 0.998

# ── Eğitim ─────────────────────────────────────────
MAX_EPISODES   = 2000
SAVE_INTERVAL  = 100

# ── Dosya Yolları ───────────────────────────────────
MODEL_DIR = "models/"
LOG_DIR   = "logs/"