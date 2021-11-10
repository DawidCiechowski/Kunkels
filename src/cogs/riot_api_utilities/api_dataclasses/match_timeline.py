from typing import List, Optional

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase, config

from .match import Metadata


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Position:
    x: int
    y: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DamageStatistics:
    basic: bool
    magic_damage: int
    name: str
    participant_id: int
    physical_damage: int
    spell_name: str
    spell_slot: int
    true_damage: int
    damage_type: str = field(metadata=config(field_name="type"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Event:
    timestamp: int
    event_type: str = field(metadata=config(field_name="type"))
    real_timestamp: Optional[int] = None
    item_id: Optional[int] = None
    participant_id: Optional[int] = None
    level_up_type: Optional[str] = None
    skills_slots: Optional[int] = None
    ward_type: Optional[str] = None
    creator_id: Optional[int] = None
    level: Optional[int] = None
    assisting_participants_ids: Optional[List[int]] = None
    bounty: Optional[str] = None
    kill_streak_length: Optional[int] = None
    killer_id: Optional[int] = None
    position: Optional[Position] = None
    victim_damage_dealt: Optional[List[DamageStatistics]] = None
    victim_damage_received: Optional[List[DamageStatistics]] = None
    victim_id: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ChampionStats:
    ability_haste: int
    ability_power: int
    armor: int
    armor_pen: int
    armor_pen_percent: int
    attack_damage: int
    attack_speed: int
    bonus_armor_pen_percent: int
    bonus_magic_pen_percent: int
    cc_reduction: int
    cooldown_reduction: int
    health: int
    health_max: int
    health_regen: int
    lifesteal: int
    magic_pen: int
    magic_pen_percent: int
    magic_resist: int
    movement_speed: int
    omnivamp: int
    physical_vamp: int
    power: int
    power_max: int
    power_regen: int
    spell_vamp: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DamageStats:
    magic_damage_done: int
    magic_damage_done_to_champions: int
    magic_damage_taken: int
    physical_damage_done: int
    physical_damage_done_to_champions: int
    physical_damage_taken: int
    total_damage_done: int
    total_damage_done_to_champions: int
    total_damage_taken: int
    true_damage_done: int
    true_damage_done_to_champions: int
    true_damage_taken: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ParticipantFrame:
    champion_stats: ChampionStats
    current_gold: int
    damage_stats: DamageStats
    gold_per_second: int
    jungle_minions_killed: int
    level: int
    minions_killed: int
    participant_id: int
    position: Position
    time_enemy_spent_controlled: int
    xp: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ParticipantFrames:
    one: ParticipantFrame = field(metadata=config(field_name="1"))
    two: ParticipantFrame = field(metadata=config(field_name="2"))
    three: ParticipantFrame = field(metadata=config(field_name="3"))
    four: ParticipantFrame = field(metadata=config(field_name="4"))
    five: ParticipantFrame = field(metadata=config(field_name="5"))
    six: ParticipantFrame = field(metadata=config(field_name="6"))
    seven: ParticipantFrame = field(metadata=config(field_name="7"))
    eight: ParticipantFrame = field(metadata=config(field_name="8"))
    nine: ParticipantFrame = field(metadata=config(field_name="9"))
    ten: ParticipantFrame = field(metadata=config(field_name="10"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Frame:
    events: List[Event]
    participant_frames: ParticipantFrames
    timestamp: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Participant:
    participant_id: int
    puuid: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TimelineInfo:
    frame_interval: int
    frames: List[Frame]
    game_id: str
    participants: List[Participant]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MatchTimeline:
    metadata: Metadata
    info: TimelineInfo
