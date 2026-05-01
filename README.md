# 🏎️ F1 Reinforcement Learning

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/ozdogrumerve/f1-reinforcement-learning?style=for-the-badge)](https://github.com/zeynpakn/f1-reinforcement-learning/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ozdogrumerve/f1-reinforcement-learning?style=for-the-badge)](https://github.com/zeynpakn/f1-reinforcement-learning/network)
[![GitHub issues](https://img.shields.io/github/issues/ozdogrumerve/f1-reinforcement-learning?style=for-the-badge)](https://github.com/zeynpakn/f1-reinforcement-learning/issues)

**Train an intelligent agent to master the art of Formula 1 racing through Q-Learning in a simulated 2D environment.**

</div>

## 🎬 Demo

<p align="center">
  <img src="Assets/record.gif" width="700"/>
</p>

## 📖 Overview

This project explores the application of Reinforcement Learning (RL) to autonomous racing. Specifically, it implements a Q-Learning agent designed to control a Formula 1 car within a custom 2D simulation environment built with Pygame. The goal is to train an AI driver that can navigate a race track efficiently, avoid obstacles, and optimize its lap times through trial and error, demonstrating the principles of state-action value learning.

This project is ideal for students and researchers interested in:
*   Understanding the practical implementation of Q-Learning.
*   Exploring agent-environment interaction in a game-like simulation.
*   Developing basic autonomous driving capabilities using machine learning.

## ✨ Features

-   **2D F1 Racing Simulation:** A custom-built Pygame environment for simulating car movement, track physics, and sensor input.
-   **Q-Learning Agent:** Implementation of a Q-Learning algorithm for the AI car to learn optimal driving policies.
-   **Modular Design:** Separate components for car physics (`car.py`), track definition (`track.py`), environment logic (`environment.py`), and the Q-learning algorithm (`q_learning_agent.py`).
-   **Configurable Parameters:** Easily adjust reinforcement learning hyperparameters and simulation settings via `config.py`.
-   **Sensor System:** The F1 car is equipped with a sensor system (`sensor.py`) to perceive its immediate surroundings and gather state information for the RL agent.
-   **Environment Testing:** Basic unit tests for critical environment functionalities (`test_env.py`) to ensure simulation correctness.
-   **Model Persistence:** Support for saving and loading trained Q-tables or neural network models (implied by `models/` directory).

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white) 
![NumPy](https://img.shields.io/badge/NumPy-1.26.4-purple?style=for-the-badge&logo=numpy&logoColor=white) 
![Pygame](https://img.shields.io/badge/Pygame-2.5.2-green?style=for-the-badge&logo=python&logoColor=white) 
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8.4-red?style=for-the-badge&logo=matplotlib&logoColor=white) 

</div>

**Core:**
*   Python: Primary programming language

**Machine Learning & Data Science:**
*   Numpy: Numerical computing for arrays and mathematical operations

**Simulation & Visualization:**
*   Pygame: 2D game development library for creating the simulation environment
*   Matplotlib: For creating static, animated, and interactive visualizations (e.g., training progress plots)

## 📁 Project Structure

```
f1-reinforcement-learning/
├── .gitignore               # Specifies intentionally untracked files to ignore
├── __pycache__/             # Python bytecode cache
├── models/                  # Directory for saving trained RL models (e.g., Q-tables)
├── car.py                   # Implements the F1 car agent's physics and state
├── config.py                # Centralized configuration parameters for the simulation and RL agent
├── environment.py           # Defines the 2D racing environment, state transitions, and reward system
├── evaluate.py              # (Empty) Placeholder for model evaluation script
├── main.py                  # Main entry point for running the simulation and training the agent
├── plots.py                 # (Empty) Placeholder for data plotting and visualization utilities
├── q_learning_agent.py      # Implements the Q-Learning algorithm and agent logic
├── requirements.txt         # Lists all Python dependencies
├── sensor.py                # Defines the car's sensor system for environment perception
├── test_env.py              # Contains unit tests for the environment setup and logic
└── track.py                 # Defines the racing track's geometry, checkpoints, and boundaries
```

## 🚀 Quick Start

### Prerequisites
Before you begin, ensure you have:
-   **Python 3.8+** installed on your system.
    
### 1. Set Up Environment
 
```bash
# Create a Python 3.10 virtual environment
py -3.10 -m venv rl_env
 
# Activate it
rl_env\Scripts\activate        # Windows
source rl_env/bin/activate     # macOS / Linux
 
# Install dependencies
pip install -r requirements.txt
```
 
### 2. Verify Everything Works
 
```bash
python test_env.py
```
 
You'll see 10 steps of environment interaction with reward values and Q-table growth. If it runs without errors, you're good to go.
 
## 🚀 Usage
 
### Manual Mode — Drive It Yourself
 
```bash
python main.py
```
 
| Key | Action |
|-----|--------|
| `↑` | Accelerate |
| `↓` | Brake |
| `← →` | Turn |
| `R` | Reset position |
 
### Training — Let the AI Learn
 
```bash
python train.py
```
 
Runs **2,000 episodes** in headless mode (no rendering = maximum speed). The agent explores the track, crashes a lot, and gradually figures out what it's doing.
 
- Saves a checkpoint every **100 episodes** → `models/q_table_ep{N}.pkl`
- Automatically keeps the **best model** ever → `models/q_table_best.pkl`
- Full training log → `logs/training_log.csv`
### Evaluation — Watch It Drive
 
```bash
python evaluate.py
```
 
Loads the best saved model and runs **5 visual episodes** with ε = 0 (pure exploitation, zero randomness). Watch what 2000 episodes of suffering produces.
 
Press `Q` to quit.
 
### The Reward Function
 
This is where the *real* design happens. The agent doesn't know what "driving" means — it only knows numbers. These numbers shape everything:
 
```
🏁 Pass a checkpoint      →  +50    (the main objective)
⚡ Moving fast forward    →  +5     (alive + forward bonus)
🐢 Moving slow            →  -0.5   (nudge to keep moving)
🔙 Going backwards        →  -2     (strong discouragement)
💥 Hitting a wall         →  -50    (terminal punishment)
```
 
> **Design note:** The +50 checkpoint reward is intentionally large. Without it, the agent learns to drive in circles avoiding walls — technically alive, strategically useless.
 
### Q-Learning Update Rule
 
At every step, the Q-table is updated via the Bellman equation:
 
```
Q(s, a)  ←  Q(s, a) + α · [ r + γ · max Q(s', a') − Q(s, a) ]
                             ↑           ↑
                          reward    discounted future value
```
 
## ⚙️ Configuration
 
Everything is tunable in `config.py`:
 
```python
# Car Physics
CAR_SPEED_MAX    = 6       # Max speed (px/frame)
CAR_ACCELERATION = 0.3     # Acceleration per frame
CAR_FRICTION     = 0.05    # Natural deceleration
 
# Sensors
SENSOR_COUNT     = 5
SENSOR_MAX_RANGE = 150     # Vision range (px)
SENSOR_ANGLES    = [-60, -30, 0, 30, 60]
 
# Q-Learning
LEARNING_RATE    = 0.1
GAMMA            = 0.95    # Future reward discount
EPSILON_DECAY    = 0.998   # Exploration decay per episode
 
# Training
MAX_EPISODES     = 2000
SAVE_INTERVAL    = 100
```

## 🔧 Development

### Running Tests
To ensure the environment and core logic are functioning as expected, you can run the provided tests:

```bash
python test_env.py
```

## 🙏 Acknowledgments

-   This project is a fork of [zeynpakn/f1-reinforcement-learning](https://github.com/zeynpakn/f1-reinforcement-learning). Special thanks to the original author for the foundational work.
-   The open-source community behind Python, Pygame, NumPy and Matplotlib for providing essential tools.

---

<div align="center">

**⭐ Star this repo if you find it helpful or interesting!**

Made with ❤️ by [Zeynep Akın](https://github.com/zeynpakn) & [Merve Özdoğru](https://github.com/ozdogrumerve) & [Hatice Kübra Ülke](https://github.com/hkubrau)
</div>

<div align="center">
Built with 🧠 Q-Learning · 💥 Countless crashes · ☕ Probably too much coffee
</div>