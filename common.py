"""common.py

Module containing classes used throughout the game.
This module should not import other game modules.
"""

import json
from typing import Sequence


#Status
statuses = []
with open("statuses.json", "r") as f:
    statusdata = {
        record["name"]: record
        for record in json.load(f)
    }
    statuses = list(statusdata.keys())


class Attack:
    """Encapsulates data for an attack."""
    def __init__(self,
                name: str,
                accuracy: "int | None" = None,
                damage: "int | None" = None,
                healing: "int | None" = None,
                repeats: Sequence[int] = (1, 1),
                inflicts: "str | None" = None):
        assert len(repeats) == 2
        min_, max_ = repeats
        assert isinstance(min_, int)
        assert isinstance(max_, int)
        assert min_ >= 0
        assert max_ >= min_
        self.name = name
        self.accuracy = accuracy
        self.damage = damage
        self.healing = healing
        self.inflicts = inflicts
        self.repeats = tuple(repeats)

    def __repr__(self) -> str:
        return f"Attack({self.name!r}, accuracy={self.accuracy}, damage={self.damage}, repeats={self.repeats!r}, inflicts={self.inflicts!r})"

    def __str__(self) -> str:
        if self.repeats:
            lower, upper = self.repeats
            return f"{self.name}  {self.accuracy} acc  {self.damage}*n dmg, n ranges from {lower} to {upper}"
        return f"{self.name}  {self.accuracy} acc  {self.damage} dmg"


class Status:
    """Encapsulates status data"""
    def __init__(self, name: str, description: str, count: int):
        self.name = name
        self.description = description
        self.count = count

    def __repr__(self) -> str:
        return f"Status({self.name}, {self.description}, {self.count})"

    def update(self) -> None:
        """Update status state at end of turn"""
        assert self.count >= 0
        self.count -= 1


def new_status(name: str) -> Status:
    """Returns a new instance of the requested status"""
    # ** operator unpacks dict data into keyword arguments
    return Status(**statusdata[name])


class Combatant:
    """Base class for game characters.

    Attributes:
    name (str): The name of the character.
    health (int): Health of character.
    max_health (int): Max health of character

    Methods:
    take_damage(x): Reduces health of combatant by x 
    is_defeated(): Returns True if combatant's health is less than 0, else return False
    add_status(str): Adds status to a combatant
    has_status(str): If combatant has status, returns True, else returns False.
    update(): Updates combatant state after one turn
    """
    attacks: list[Attack]
    def __init__(self,
         name: str,
         health: int,
    ):
        self.name = name
        self.health = health
        self.max_health = health
        self.status: dict[str, "Status | None"] = {
            status: None
            for status in statuses
        }

    def take_damage(self, damage: int):
        """Reduces health based on damage done"""
        self.health -= damage

    def is_defeated(self):
        """Returns True if characters health is less than 0, else return False"""
        if self.health <= 0:
            return True
        return False

    def add_status(self, status: "str | None") -> None:
        """Adds status to a character.
    Statuses are assumed not to stack.
    If character already has a given status,
    the existing status is replaced with a new one.
    (This may need to be customized with a keyword argument in future.)
    """
        if status is None:
            return
        self.status[status] = new_status(status)

    def has_status(self, status):
        """If character has status, returns True, else returns False."""
        return self.status[status] is not None

    def select_attack(self) -> Attack:
        """Select an attack to use in combat"""
        raise NotImplementedError

    def get_attack(self, name: "str | None") -> Attack:
        if not name:
            return self.attacks[0]
        for attack in self.attacks:
            if attack.name == name:
                return attack
        raise ValueError(f"{name}: no such attack")

    def attack(self, target: "Combatant", attack: Attack) -> bool:
        """Attacks a target using one of its attacks.
        Returns True if the attack succeeded, otherwise False.
        """
        raise NotImplementedError

    def select_target(self, combatants: list["Combatant"]) -> "Combatant":
        """Select a target to attack"""
        raise NotImplementedError

    def update(self) -> None:
        """Updates character state at end of turn."""
        for name, status in self.status.items():
            if status is None:
                continue
            status.update()
            if status.count == 0:
                self.status[name] = None
