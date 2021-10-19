from typing import Tuple

import requests

from api_dataclasses.match import Match
from api_dataclasses.match_timeline import MatchTimeline
from api_dataclasses.summoner import Summoner


class RiotApi:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
            "Accept-Language": "en-US,en-GB;q=0.9,en;q=0.8,pl-PL;q=0.7,pl;q=0.6",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": f"{self.api_token}",
        }

    def summoner_search(self, summoners_name: str) -> Summoner:
        url = f"https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoners_name}"

        return Summoner.from_dict(requests.get(url, headers=self.headers).json())

    def __get_last_match_id(self, summoners_puuid) -> str:
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoners_puuid}/ids?start=0&count=1"
        return requests.get(url, headers=self.headers).json()[0]

    def __get_match_data(self, summoners_puuid, last: bool = False) -> Match:
        if last:
            match_id = self.__get_last_match_id(summoners_puuid)
        else:
            pass

        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"

        return Match.from_dict(requests.get(url, headers=self.headers).json())

    def __get_match_timeline(
        self, summoners_puuid: str, last: bool = False
    ) -> MatchTimeline:
        if last:
            match_id = self.__get_last_match_id(summoners_puuid)
        else:
            pass

        url = (
            f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
        )

        return MatchTimeline.from_dict(requests.get(url, headers=self.headers).json())

    def summoners_last_game(self, summoners_name: str) -> Tuple[Match, MatchTimeline]:
        summoner = self.summoner_search(summoners_name)

        return self.__get_match_data(summoner.puuid, True), self.__get_match_timeline(
            summoner.puuid, True
        )
