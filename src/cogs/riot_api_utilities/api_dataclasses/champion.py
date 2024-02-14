from os import name
from typing import Dict, List 

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class Stats:
    hp: int
    hpperlevel: int
    mp: int
    mpperlevel: int
    movespeed: int
    armor: int
    armorperlevel: int
    spellblock: int
    spellblockperlevel: int
    attackrange: int
    hpregen: int
    hpregenperlevel: int
    mpregen: int
    mpregenperlevel: int
    crit: int
    critperlevel: int
    attackdamage: int
    attackdamageperlevel: int
    attackspeedperlevel: int
    attackspeed: int


@dataclass_json
@dataclass
class Image:
    full: str
    sprite: str
    group: str
    x: int
    y: int
    w: int
    h: int


@dataclass_json
@dataclass
class Info:
    attack: int
    defense: int
    magic: int
    difficulty: int


@dataclass_json
@dataclass
class Champion:
    version: str
    id: str
    key: str
    name: str
    title: str
    blurb: str
    info: Info
    image: Image
    tags: List[str]
    partype: str
    stats: Stats


@dataclass_json
@dataclass
class ChampionData:
    type: str
    data_format: str = field(metadata=config(field_name="format"))
    version: str
    data: Dict[str, Champion]


from pathlib import Path
import json

with open(f"{Path(__file__).parent}/champion_data.json", encoding='utf8') as f:
    champions = json.load(f)

champions_data = ChampionData.from_dict(champions)

__all__ = ["champion_data"]
