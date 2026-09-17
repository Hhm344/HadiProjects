"""
Create a system workflow diagram for the report and presentation.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(BASE_DIR, "figures", "workflow_diagram.png")


def make_box(ax, x, y, w, h, text, color):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                         linewidth=1.5, edgecolor="#333333",
                         facecolor=color, alpha=0.95)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=10, fontweight="bold", color="#1a1a1a", wrap=True)


def make_arrow(ax, x1, y1, x2, y2):
    arr = FancyArrowPatch((x1, y1), (x2, y2),
                          arrowstyle="->", mutation_scale=18,
                          linewidth=1.5, color="#444444")
    ax.add_patch(arr)


fig, ax = plt.subplots(figsize=(11, 5.5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 6)
ax.axis("off")

# Stage colors (light pastels)
c_data = "#D6EAF8"
c_pre = "#FCF3CF"
c_feat = "#FAD7A0"
c_split = "#F5CBA7"
c_train = "#A9DFBF"
c_eval = "#F1948A"
c_deploy = "#D7BDE2"

# Stages
make_box(ax, 0.1, 2.5, 1.6, 1.0, "Banking\nEmail\nDataset", c_data)
make_box(ax, 1.95, 2.5, 1.7, 1.0, "Data\nCleaning &\nPreprocessing", c_pre)
make_box(ax, 3.9, 2.5, 1.7, 1.0, "Feature\nExtraction\n(TF-IDF/Counts)", c_feat)
make_box(ax, 5.85, 2.5, 1.4, 1.0, "Train /\nTest\nSplit 80/20", c_split)

# Branches
make_box(ax, 7.55, 4.0, 1.8, 0.9, "Train Naive\nBayes (Proposed)", c_train)
make_box(ax, 7.55, 2.7, 1.8, 0.9, "Train Baselines\n(LR, SVM, DT)", c_train)
make_box(ax, 7.55, 1.4, 1.8, 0.9, "5-Fold Cross\nValidation", c_train)

make_box(ax, 9.55, 2.5, 1.3, 1.0, "Evaluate\n& Compare", c_eval)

# Arrows
make_arrow(ax, 1.7, 3.0, 1.95, 3.0)
make_arrow(ax, 3.65, 3.0, 3.9, 3.0)
make_arrow(ax, 5.6, 3.0, 5.85, 3.0)
make_arrow(ax, 7.25, 3.4, 7.55, 4.2)
make_arrow(ax, 7.25, 3.0, 7.55, 3.1)
make_arrow(ax, 7.25, 2.7, 7.55, 1.8)
make_arrow(ax, 9.35, 4.2, 9.55, 3.4)
make_arrow(ax, 9.35, 3.1, 9.55, 3.0)
make_arrow(ax, 9.35, 1.8, 9.55, 2.6)

ax.set_title("Proposed System Workflow: Phishing Email Detection in Banking Systems",
             fontsize=13, fontweight="bold", pad=12)

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=180, bbox_inches="tight")
print(f"Saved {OUT_PATH}")
