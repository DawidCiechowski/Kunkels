from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Summoner:
    id: str
    account_id: str
    puuid: str
    name: str
    profile_icon_id: str
    revision_date: int
    summoner_level: int
