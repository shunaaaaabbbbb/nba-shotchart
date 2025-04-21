import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from src.app.utils.court import draw_court


def plot_shotchart(shots_df: pd.DataFrame, title: str) -> Figure:
    """ショットチャートを描画する関数

    Args:
        shots_df (pd.DataFrame): ショットチャートのデータフレーム
        title (str): グラフのタイトル

    Returns:
        Figure: 描画されたグラフのfigure
    """

    fig, ax = plt.subplots(figsize=(12, 11))
    draw_court(ax)

    made_shots = shots_df[shots_df["SHOT_MADE_FLAG"] == 1]
    ax.scatter(
        -1 * made_shots["LOC_X"],
        made_shots["LOC_Y"],
        c="#3498db",
        alpha=0.7,
        s=100,
        marker="o",
        edgecolors="black",
        label="Made",
    )

    missed_shots = shots_df[shots_df["SHOT_MADE_FLAG"] == 0]
    ax.scatter(
        -1 * missed_shots["LOC_X"],
        missed_shots["LOC_Y"],
        c="red",
        alpha=0.7,
        s=100,
        marker="x",
        linewidths=2,
        label="Missed",
    )

    ax.legend(loc="upper right")
    ax.set_title(title, fontsize=20)

    return fig
