from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase, config


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Summoner:
    summonre_id: str = field(metadata=config(field_name="id"))
    account_id: str
    puuid: str
    name: str
    profile_icon_id: str
    revision_date: int
    summoner_level: int
