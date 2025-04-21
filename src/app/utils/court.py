import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Arc, Circle, Rectangle


def draw_court(ax: Axes = None, color: str = "black", lw: int = 2) -> Axes:
    """バスケットコートを描画する

    Args:
        ax (Axes, optional): Matplotlibの軸オブジェクト. Defaults to None.
        color (str, optional): コートの線の色. Defaults to 'black'.
        lw (int, optional): コートの線の太さ. Defaults to 2.

    Returns:
        Axes: 描画されたコートのある軸オブジェクト
    """
    # 新しいAxesオブジェクトが指定されていない場合は作成
    if ax is None:
        _, ax = plt.subplots(figsize=(12, 11))

    # コート要素を定義
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)
    paint = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    free_throw_top = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color)
    free_throw_bottom = Arc(
        (0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle="dashed"
    )
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # 全ての要素をAxesに追加
    court_elements = [
        hoop,
        backboard,
        paint,
        free_throw_top,
        free_throw_bottom,
        restricted,
        corner_three_a,
        corner_three_b,
        three_arc,
    ]

    for element in court_elements:
        ax.add_patch(element)

    # 表示範囲の設定
    ax.set_xlim(-250, 250)
    ax.set_ylim(-50, 400)

    # 軸を消す
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_aspect("equal")  # アスペクト比を等しくする（重要）

    return ax
