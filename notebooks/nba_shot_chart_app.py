import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib.patches import Arc, Circle, Rectangle
from nba_api.stats.endpoints import commonplayerinfo, shotchartdetail
from nba_api.stats.static import players

st.set_page_config(page_title="NBA ショットチャート分析", page_icon="🏀", layout="wide")
st.title("🏀 NBA ショットチャート分析")
st.sidebar.header("設定")


# バスケットコートを描画する関数
def draw_court(ax=None, color: str = "black", lw: int = 2):
    """バスケットコートを描画する

    Args:
        ax (_type_, optional): Matplotlibの軸オブジェクト. Defaults to None.
        color (str, optional): コートの線の色. Defaults to 'black'.
        lw (int, optional): コートの線の太さ. Defaults to 2.

    Returns:
        matplotlib.axes.Axes: 描画されたコートのある軸オブジェクト
    """
    # 新しいAxesオブジェクトが指定されていない場合は作成
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 11))

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


# ショットチャートを描画する関数
def plot_shotchart(shots_df: pd.DataFrame, title: str, color_by_success: bool = True):
    """
    ショットチャートを描画する関数

    Parameters
    ----------
    shots_df : pandas.DataFrame
        ショットデータ
    title : str, default "Shot Chart"
        グラフのタイトル
    color_by_success : bool, default True
        成功・失敗で色分けするかどうか

    Returns
    -------
    fig : matplotlib Figure
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
    # ax.set_title("Timberwolves Shot Chart Against Lakers \n 2024-25 Playoffs", fontsize=20)

    return fig


# ゾーンでフィルタリングする関数
def filter_shots_by_zone(shots_df, shot_zone_basic=None, shot_zone_area=None, shot_zone_range=None):
    """
    ショットをゾーンでフィルタリングする関数
    """
    filtered_df = shots_df.copy()

    if shot_zone_basic and shot_zone_basic != "All":
        filtered_df = filtered_df[filtered_df["SHOT_ZONE_BASIC"] == shot_zone_basic]

    if shot_zone_area and shot_zone_area != "All":
        filtered_df = filtered_df[filtered_df["SHOT_ZONE_AREA"] == shot_zone_area]

    if shot_zone_range and shot_zone_range != "All":
        filtered_df = filtered_df[filtered_df["SHOT_ZONE_RANGE"] == shot_zone_range]

    return filtered_df


# 選手のショットチャートデータを取得する関数
def get_player_shotchart_data(player_id, season, season_type="Regular Season"):
    """
    選手のショットチャートデータを取得
    """
    try:
        shot_data = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=player_id,
            # player_id=0,
            # team_id =1610612750,
            season_nullable=season,
            season_type_all_star=season_type,
            context_measure_simple="FGA",
            # opponent_team_id=1610612747,
        )

        shots_df = shot_data.get_data_frames()[0]
        return shots_df
    except Exception as e:
        st.error(f"データの取得中にエラーが発生しました: {e}")
        return pd.DataFrame()


# 選手の詳細情報を取得する関数
def get_player_info(player_id):
    """
    選手の詳細情報を取得
    """
    try:
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        info_df = player_info.get_data_frames()[0]
        return info_df.iloc[0].to_dict() if not info_df.empty else {}
    except Exception as e:
        st.error(f"選手情報の取得中にエラーが発生しました: {e}")
        return {}


# 選手選択コンポーネント
def player_selection_component():
    """
    選手選択コンポーネント

    Returns
    -------
    player_id : int
        選択された選手のID
    """
    all_players = players.get_players()
    active_players = [p for p in all_players if p.get("is_active", False)]

    active_player_names = [f"{p['full_name']}" for p in active_players]
    active_player_ids = [p["id"] for p in active_players]

    selected_player_name = st.sidebar.selectbox("選手を選択", active_player_names)
    selected_index = active_player_names.index(selected_player_name)

    return active_player_ids[selected_index]


def date_range_selector():
    """日付範囲選択コンポーネント"""
    st.sidebar.subheader("日付範囲フィルター")

    start_date = None
    end_date = None

    is_apply_date_filter = st.sidebar.checkbox("日付範囲でフィルタリング", value=False)

    if is_apply_date_filter:
        today = datetime.date.today()

        season_start = today - datetime.timedelta(days=1)
        start_date = st.sidebar.date_input(
            "開始日",
            value=season_start,
        )

        season_end = today
        end_date = st.sidebar.date_input(
            "終了日",
            value=season_end,
        )

        st.sidebar.info(
            f"選択期間: {start_date.strftime('%Y/%m/%d')} ～ {end_date.strftime('%Y/%m/%d')}"
        )

    return is_apply_date_filter, start_date, end_date


def filter_shots_by_date(shots_df, is_apply_date_filter, start_date=None, end_date=None):
    """
    ショットを日付でフィルタリングする関数

    Args:
        shots_df (pandas.DataFrame): ショットデータ
        is_apply_date_filter (bool): 日付フィルターを使用するか
        start_date (datetime.date, optional): 開始日
        end_date (datetime.date, optional): 終了日

    Returns:
        pandas.DataFrame: フィルタリングされたショットデータ
    """
    if not is_apply_date_filter or start_date is None or end_date is None:
        return shots_df

    if "GAME_DATE" in shots_df.columns:
        shots_df["GAME_DATE"] = pd.to_datetime(shots_df["GAME_DATE"])

        # 日付範囲でフィルタリング
        filtered_df = shots_df[
            (shots_df["GAME_DATE"].dt.date >= start_date)
            & (shots_df["GAME_DATE"].dt.date <= end_date)
        ]

        return filtered_df

    return shots_df


# メイン処理
def main():
    player_id = player_selection_component()
    if not player_id:
        st.info("左側のサイドバーから選手を選択してください。")
        return

    # シーズン選択
    seasons = [
        "2024-25",
        "2023-24",
        "2022-23",
        "2021-22",
        "2020-21",
        "2019-20",
        "2018-19",
        "2017-18",
        "2016-17",
        "2015-16",
        "2014-15",
    ]
    selected_season = st.sidebar.selectbox("シーズンを選択", seasons, index=0)

    # シーズンタイプ選択
    season_types = ["Regular Season", "Playoffs", "Pre Season", "All Star"]
    selected_season_type = st.sidebar.selectbox("シーズンタイプを選択", season_types)

    # 選手情報を取得
    player_info = get_player_info(player_id)

    # 選手情報の表示
    if player_info:
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            st.image(
                f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png",
                use_container_width=True,
                caption=player_info.get("DISPLAY_FIRST_LAST", "Player"),
            )

        with col2:
            st.subheader(player_info.get("DISPLAY_FIRST_LAST", ""))
            st.write(
                f"チーム: {player_info.get('TEAM_CITY', '')} {player_info.get('TEAM_NAME', '')}"
            )
            st.write(f"ポジション: {player_info.get('POSITION', '')}")
            st.write(
                f"身長: {player_info.get('HEIGHT', '')} | 体重: {player_info.get('WEIGHT', '')} lbs"
            )
            st.write(f"生年月日: {player_info.get('BIRTHDATE')[:10]}")
            st.write(f"出身: {player_info.get('COUNTRY', '')}")
            st.write(f"経験: {player_info.get('SEASON_EXP', '')} 年")

    # データ取得中の表示
    with st.spinner("ショットデータを取得中..."):
        shots_df = get_player_shotchart_data(player_id, selected_season, selected_season_type)

    if shots_df.empty:
        st.warning(
            f"選択したシーズン ({selected_season}) とシーズンタイプ ({selected_season_type}) のショットデータが見つかりませんでした。"  # noqa: E501
        )
        return

    # ショットゾーンのフィルタリング
    st.sidebar.subheader("ショットゾーンフィルター")

    # 基本ゾーンのユニークな値を取得
    shot_zone_basic_values = ["All"] + sorted(shots_df["SHOT_ZONE_BASIC"].unique().tolist())
    selected_shot_zone_basic = st.sidebar.selectbox("基本ゾーン", shot_zone_basic_values)

    # エリアゾーンのユニークな値を取得
    shot_zone_area_values = ["All"] + sorted(shots_df["SHOT_ZONE_AREA"].unique().tolist())
    selected_shot_zone_area = st.sidebar.selectbox("エリアゾーン", shot_zone_area_values)

    # レンジゾーンのユニークな値を取得
    shot_zone_range_values = ["All"] + sorted(shots_df["SHOT_ZONE_RANGE"].unique().tolist())
    selected_shot_zone_range = st.sidebar.selectbox("レンジゾーン", shot_zone_range_values)

    # フィルタリング
    filtered_shots = filter_shots_by_zone(
        shots_df, selected_shot_zone_basic, selected_shot_zone_area, selected_shot_zone_range
    )

    # 日付範囲選択
    is_apply_date_filter, start_date, end_date = date_range_selector()
    # 日付でフィルタリング（新しい部分）
    filtered_shots = filter_shots_by_date(
        filtered_shots, is_apply_date_filter, start_date, end_date
    )

    with st.sidebar.expander("詳細な設定"):
        st.write("詳細オプション")

    # ショットチャートの描画
    player_name = player_info.get("DISPLAY_FIRST_LAST", "Player")
    chart_title = f"{player_name} Shot Chart\n{selected_season} {selected_season_type}"

    if player_info:
        if not filtered_shots.empty:
            with col3:
                fig = plot_shotchart(filtered_shots, title=chart_title)
                st.pyplot(fig)

                # 成功率の統計を表示
                made_shots_count = filtered_shots["SHOT_MADE_FLAG"].sum()
                total_shots = len(filtered_shots)
                success_rate = made_shots_count / total_shots * 100 if total_shots > 0 else 0

                st.metric(
                    "シュート成功率", f"{success_rate:.2f}%", f"{made_shots_count}/{total_shots}"
                )

        # ゾーン別の成功率を分析
        st.subheader("ゾーン別の成功率")
        zone_stats = (
            filtered_shots.groupby("SHOT_ZONE_BASIC")
            .agg(
                {
                    "SHOT_MADE_FLAG": ["sum", "count"],
                }
            )
            .reset_index()
        )
        st.write(zone_stats)
        zone_stats.columns = ["ZONE", "MADE", "TOTAL"]
        zone_stats["SUCCESS_RATE"] = zone_stats["MADE"] / zone_stats["TOTAL"] * 100

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(zone_stats["ZONE"], zone_stats["SUCCESS_RATE"])

        # バーに値を表示
        for bar, made, total in zip(bars, zone_stats["MADE"], zone_stats["TOTAL"]):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 1,
                f"{height:.1f}% ({made}/{total})",
                ha="center",
                va="bottom",
                rotation=0,
            )

        ax.set_title(f"{player_name} - Shot Success Rate by Zone ({selected_season})", fontsize=16)
        ax.set_xlabel("Zone", fontsize=14)
        ax.set_ylabel("Success Rate (%)", fontsize=14)
        plt.xticks(rotation=45, ha="right")
        ax.set_ylim(0, 100)
        plt.tight_layout()

        st.pyplot(fig)

        # データテーブル
        st.subheader("ショットデータテーブル")
        st.dataframe(filtered_shots)
    else:
        st.warning("選択した条件に一致するショットがありません。")


if __name__ == "__main__":
    main()
