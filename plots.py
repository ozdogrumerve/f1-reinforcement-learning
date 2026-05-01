import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os
from config import LOG_DIR

plt.rcParams.update({
    "text.color": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
})

def load_log():
    path = os.path.join(LOG_DIR, "training_log.csv")
    if not os.path.exists(path):
        print(f"❌ Log bulunamadı: {path}")
        return None
    return pd.read_csv(path)

def moving_average(data, window=50):
    return data.rolling(window=window, min_periods=1).mean()

def plot_all():
    df = load_log()
    if df is None:
        return

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("F1 Q-Learning — Eğitim Analizi", fontsize=16, fontweight="bold")
    fig.patch.set_facecolor("#1a1a2e")

    for ax in axes.flat:
        ax.set_facecolor("#16213e")
        ax.tick_params(colors="white", labelcolor="white", which="both")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")
        ax.xaxis.set_tick_params(labelcolor="white")
        ax.yaxis.set_tick_params(labelcolor="white")
        for spine in ax.spines.values():
            spine.set_edgecolor("#666")

    # ── 1. Episode vs Reward ───────────────────────
    ax = axes[0, 0]
    ax.plot(df["episode"], df["total_reward"],
            color="#aaaaaa", alpha=0.4, linewidth=0.8, label="Ham")
    ax.plot(df["episode"], moving_average(df["total_reward"]),
            color="#e94560", linewidth=2, label="Ort. (50 ep)")
    ax.axhline(y=-36, color="#cccccc", linestyle="--",
               linewidth=1, label="Baseline (-36)")
    ax.set_title("Episode → Total Reward")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Reward")
    ax.legend(facecolor="#1a1a2e", labelcolor="white", fontsize=8)

    # ── 2. Episode vs Steps ────────────────────────
    ax = axes[0, 1]
    ax.plot(df["episode"], df["steps"],
            color="#7eb8f7", alpha=0.5, linewidth=0.8)
    ax.plot(df["episode"], moving_average(df["steps"]),
            color="#53d8fb", linewidth=2)
    ax.fill_between(df["episode"],
                    moving_average(df["steps"]),
                    alpha=0.25, color="#53d8fb")
    ax.set_title("Episode → Survival Steps")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Steps")

    # ── 3. Episode vs Checkpoint ───────────────────
    ax = axes[1, 0]
    ax.bar(df["episode"], df["checkpoints"],
           color="#e94560", alpha=0.7, width=1.5)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.set_title("Episode → Max Checkpoint")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Checkpoint")

    # ── 4. Epsilon Decay ──────────────────────────
    ax = axes[1, 1]
    ax.plot(df["episode"], df["epsilon"],
            color="#53d8fb", linewidth=2)
    ax.fill_between(df["episode"], df["epsilon"],
                    alpha=0.20, color="#53d8fb")
    ax.set_title("Epsilon Decay (Keşif → Sömürü)")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Epsilon")

    plt.tight_layout()

    out_path = os.path.join(LOG_DIR, "training_plots.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print(f"✅ Grafik kaydedildi: {out_path}")
    plt.show()

if __name__ == "__main__":
    plot_all()