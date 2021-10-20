from typing import Optional, Any, List

from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Perks:
    perk_ids: List[int]
    perk_style: int
    perk_sub_style: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Participant:
    team_id: int
    spell1_id: int
    spell2_id: int
    champion_id: int
    profile_icon_id: int
    summoner_name: str
    bot: bool
    summoner_id: str
    game_customization_objects: List[Any]
    perks: Perks


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Observers:
    encryption_key: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Ban:
    champion_id: int
    team_id: int
    pick_turn: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SpectatorData:
    game_id: int
    map_id: int
    game_mode: str
    game_type: str
    game_queue_config_id: int
    participants: List[Participant]
    observers: Observers
    platform_id: str
    banned_champions: List[Ban]
    game_start_time: int
    game_length: int
