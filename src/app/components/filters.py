from datetime import datetime

import pandas as pd

from app.utils.convert_type import convert_str_to_datetime


def filter_shots_by_zone(
    shots_df: pd.DataFrame,
    shot_zone_basic: str = None,
    shot_zone_area: str = None,
    shot_zone_range: str = None,
) -> pd.DataFrame:
    """ショットをゾーンでフィルタリングする関数

    Args:
        shots_df (pd.DataFrame): ショットチャートのデータフレーム
        shot_zone_basic (str, optional): 基本ゾーンの指定値. Defaults to None.
        shot_zone_area (str, optional): エリアゾーンの指定値 Defaults to None.
        shot_zone_range (str, optional): レンジゾーンの指定値. Defaults to None.

    Returns:
        pd.DataFrame: フィルター後のショットチャートのデータフレーム
    """
    filtered_df = shots_df.copy()

    if shot_zone_basic and shot_zone_basic != "All":
        filtered_df = filtered_df[filtered_df["SHOT_ZONE_BASIC"] == shot_zone_basic]

    if shot_zone_area and shot_zone_area != "All":
        filtered_df = filtered_df[filtered_df["SHOT_ZONE_AREA"] == shot_zone_area]

    if shot_zone_range and shot_zone_range != "All":
        filtered_df = filtered_df[filtered_df["SHOT_ZONE_RANGE"] == shot_zone_range]

    return filtered_df


def filter_shots_by_date(
    shots_df: pd.DataFrame, start_date: datetime, end_date: datetime
) -> pd.DataFrame:
    """
    ショットチャートを日付でフィルタリングする関数

    Args:
        shots_df (pandas.DataFrame): ショットチャートのデータフレーム
        start_date (datetime.date, optional): 開始日
        end_date (datetime.date, optional): 終了日

    Returns:
        pandas.DataFrame: フィルタリングされたショットデータ
    """
    shots_df = convert_str_to_datetime(df=shots_df, date_columns=["GAME_DATE"])

    # start_date～end_dateの期間を抽出
    filtered_df = shots_df[
        (shots_df["GAME_DATE"].dt.date >= start_date) & (shots_df["GAME_DATE"].dt.date <= end_date)
    ]
    return filtered_df
