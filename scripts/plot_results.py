"""Draw the reported ARCHER2 runtimes from the audited scalar records."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
PAPER = "#11202b"
PANEL = "#172b38"
INK = "#e9f1ee"
MUTED = "#a9bfca"
TEAL = "#55d7bd"
GOLD = "#ffc482"


def main():
    with (ROOT / "data/archer2-records.csv").open(newline="") as file:
        records = list(csv.DictReader(file))
    strong = [r for r in records if r["series"] == "strong"]
    weak = [r for r in records if r["series"] == "weak"]
    placement = [r for r in records if r["series"] == "placement"]
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 6.25), facecolor=PAPER,
                             gridspec_kw={"width_ratios": [1.12, 1.12, 1]})
    fig.subplots_adjust(left=.065, right=.965, bottom=.245, top=.735, wspace=.34)
    fig.text(.065, .905, "MPI sandpile on ARCHER2", color=INK, weight="bold", size=28)
    fig.text(.065, .842, "Historical timings for 655,360 fixed iterations per run", color=MUTED, size=13)
    for ax in axes:
        ax.set_facecolor(PANEL)
        ax.spines[:].set_visible(False)
        ax.tick_params(colors=MUTED, length=0, pad=7)
        ax.grid(axis="y", color=MUTED, alpha=.23, linewidth=.6)
        ax.set_axisbelow(True)
        ax.set_ylabel("Reported runtime (s)", color=MUTED)

    ax = axes[0]
    strong_ranks = [int(r["ranks"]) for r in strong]
    strong_times = [float(r["runtime_seconds"]) for r in strong]
    ax.plot(strong_ranks, strong_times, "o-", color=TEAL, markersize=5)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_ylim(14, 1250)
    ax.set_yticks([20, 50, 100, 200, 500, 1000], ["20", "50", "100", "200", "500", "1,000"])
    ax.set_ylabel("Reported runtime (s, log scale)", color=MUTED)
    ax.set_xticks(strong_ranks, [str(n) for n in strong_ranks])
    ax.set_xlabel("MPI ranks", color=MUTED)
    ax.set_title("Fixed 512 × 512 grid", loc="left", color=INK, weight="bold", pad=13, fontsize=12)
    ax.annotate(f"{strong_times[0]:.1f} s", (strong_ranks[0], strong_times[0]), xytext=(8, 2),
                textcoords="offset points", color=INK, fontsize=9)
    ax.annotate(f"{strong_times[-1]:.1f} s", (strong_ranks[-1], strong_times[-1]), xytext=(-2, 17),
                textcoords="offset points", ha="right", color=INK, fontsize=9)

    ax = axes[1]
    weak_ranks = [int(r["ranks"]) for r in weak]
    weak_times = [float(r["runtime_seconds"]) for r in weak]
    ax.plot(weak_ranks, weak_times, "o-", color=GOLD, markersize=5)
    ax.set_xscale("log", base=2)
    ax.set_xticks(weak_ranks, [str(n) for n in weak_ranks])
    ax.set_ylim(0, 244)
    ax.set_yticks([0, 50, 100, 150, 200])
    ax.set_xlabel("MPI ranks", color=MUTED)
    ax.set_title("Varying global grid", loc="left", color=INK, weight="bold", pad=13, fontsize=12)
    ax.annotate("+12.5% cells per rank", (32, weak_times[weak_ranks.index(32)]), xytext=(-7, 10),
                textcoords="offset points", ha="right", color=INK, fontsize=9)

    ax = axes[2]
    places = [int(r["nodes"]) for r in placement]
    times = [float(r["runtime_seconds"]) for r in placement]
    ax.bar(places, times, width=.5, color=GOLD, alpha=.85)
    ax.set_xticks(places, ["1 node", "2 nodes"])
    ax.set_ylim(0, 315)
    ax.set_yticks([0, 60, 120, 180, 240, 300])
    ax.set_title("128 ranks, two placements", loc="left", color=INK, weight="bold", pad=13, fontsize=12)
    for p, elapsed in zip(places, times):
        ax.text(p, elapsed + 8, f"{elapsed:.1f} s", color=INK, ha="center", fontsize=9)

    fig.text(.065, .125, "Each mark is one saved timing. Grid dimensions and input counts come from the run logs.",
             color=MUTED, size=11)
    fig.text(.065, .076, "The varying-grid and placement inputs differ from the saved source. Both placement runs ended above stable height.",
             color=MUTED, size=11)
    fig.savefig(ROOT / "figures/archer2-timings.png", dpi=170,
                metadata={"Software": "MPI Sandpile Study"})
    plt.close(fig)


if __name__ == "__main__":
    main()
