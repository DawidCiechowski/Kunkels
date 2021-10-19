from typing import List

from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class Metadata:
    data_version: str
    match_id: str
    participants: List[str]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class StatPerk:
    defense: int
    flex: int
    offense: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class Selection:
    perk: int
    var1: int
    var2: int
    var3: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class Style:
    description: str
    selections: List[Selection]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class Perk:
    stat_perks: StatPerk
    styles: List[Style]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class Participant:
    assists: int
    baron_kills: int
    bounty_level: int
    champ_experience: int
    champ_level: int
    champion_id: int
    champion_name: str
    champion_transform: int
    consumables_purchased: int
    damage_dealt_to_buildings: int
    damage_dealt_to_objectives: int
    damage_dealt_to_turrets: int
    damage_self_mitigated: int
    deaths: int
    detector_wards_placed: int
    double_kills: int
    dragon_kills: int
    first_blood_assist: bool
    first_blood_kill: bool
    first_tower_assist: bool
    first_tower_kill: bool
    game_ended_in_early_surrender: bool
    game_ended_in_surrender: bool
    gold_earned: int
    gold_spent: int
    individual_position: str
    inhibitor_kills: int
    inhibitor_takedowns: int
    inhibitors_lost: int
    item0: int
    item1: int
    item2: int
    item3: int
    item4: int
    item5: int
    item6: int
    items_purchased: int
    killing_sprees: int
    kills: int
    lane: str
    largest_critical_strike: int
    largest_killing_spree: int
    largest_multi_kill: int
    longest_time_spent_living: int
    magic_damage_dealt: int
    magic_damage_dealt_to_champions: int
    magic_damage_taken: int
    neutral_minions_killed: int
    nexus_kills: int
    nexus_lost: int
    nexus_takedowns: int
    objectives_stolen: int
    objectives_stolen_assists: int
    participant_id: int
    penta_kills: int
    perks: Perk
    physical_damage_dealt: int
    physical_damage_dealt_to_champions: int
    physical_damage_taken: int
    profile_icon: int
    puuid: str
    quadra_kills: int
    riot_id_name: str
    riot_id_tagline: str
    role: str
    sight_wards_bought_in_game: int
    spell1_casts: int
    spell2_casts: int
    spell3_casts: int
    spell4_casts: int
    summoner1_casts: int
    summoner1_id: int
    summoner2_casts: int
    summoner2_id: int
    summoner_id: str
    summoner_level: int
    summoner_name: str
    team_early_surrendered: bool
    team_id: int
    team_position: int
    time_c_cing_others: int
    time_played: int
    total_damage_dealt: int
    total_damage_dealt_to_champions: int
    total_damage_shielded_on_teammates: int
    total_damage_taken: int
    total_heal: int
    total_heals_on_teammates: int
    total_minions_killed: int
    total_time_c_c_dealt: int
    total_time_spent_dead: int
    total_units_healed: int
    triple_kills: int
    true_damage_dealt: int
    true_damage_dealt_to_champions: int
    true_damage_taken: int
    turret_kills: int
    turret_takedowns: int
    turrets_lost: int
    unreal_kills: int
    vision_score: int
    vision_wards_bought_in_game: int
    wards_killed: int
    wards_placed: int
    win: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class Ban:
    champion_id: int
    pick_turn: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class Objective:
    first: bool
    kills: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class Objectives:
    baron: Objective
    champion: Objective
    dragon: Objective
    inhibitor: Objective
    rift_herald: Objective
    tower: Objective


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class Team:
    bans: List[Ban]
    objectives: Objectives
    team_id: int
    win: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class Info:
    game_creation: int
    game_duration: int
    game_end_timestamp: int
    game_id: int
    game_mode: str
    game_name: str
    game_start_timestamp: int
    game_type: str
    game_version: str
    map_id: int
    participants: List[Participant]
    platform_id: str
    queue_id: int
    teams: List[Team]


@dataclass_json
@dataclass()
class Match:
    metadata: Metadata
    info: Info


@dataclass_json
@dataclass()
class Matches:
    matches: List[str]
