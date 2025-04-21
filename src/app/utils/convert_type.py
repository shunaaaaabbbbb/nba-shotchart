import pandas as pd


def convert_str_to_datetime(df: pd.DataFrame, date_columns: list) -> pd.DataFrame:
    """
    データフレームの日付文字列カラムをdatetime型に変換する関数

    Args:
        df (pandas.DataFrame): 変換対象のデータフレーム
        date_columns (list): 変換する日付カラム名のリスト

    Returns:
        pandas.DataFrame: 日付カラムが変換されたデータフレーム
    """
    df_copy = df.copy()

    for col in date_columns:
        if col in df_copy.columns:
            df_copy[col] = pd.to_datetime(df_copy[col])

    return df_copy
