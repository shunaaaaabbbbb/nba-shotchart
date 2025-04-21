from typing import Dict

import pandas as pd
from nba_api.stats.endpoints import commonplayerinfo, shotchartdetail
from nba_api.stats.static import players


class NBAService:
    @staticmethod
    def get_all_active_players_name() -> list[str]:
        all_players = players.get_players()
        all_active_players = [p for p in all_players if p["is_active"] is True]
        all_active_player_names = [p["full_name"] for p in all_active_players]

        return all_active_player_names

    @staticmethod
    def get_player_id_by_name(player_name) -> int:
        """名前から選手情報を取得"""
        selected_player = players.find_players_by_full_name(player_name)

        return selected_player[0]["id"]

    @staticmethod
    def get_shot_chart_detail(player_id: int, season: str, season_type: str) -> pd.DataFrame:
        """
        選手のショットチャートデータを取得
        """
        shot_chart_detail = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=player_id,
            season_nullable=season,
            season_type_all_star=season_type,
            context_measure_simple="FGA",
        )
        shots_df = shot_chart_detail.get_data_frames()[0]

        return shots_df

    @staticmethod
    def get_player_info(player_id: int) -> Dict:
        """
        選手の詳細情報を取得
        """
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        info_df = player_info.get_data_frames()[0]
        info_dict = info_df.iloc[0].to_dict()

        return info_dict
