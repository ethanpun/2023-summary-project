"""common.py

Module containing classes used throughout the game.
This module should not import other game modules.
"""

import json


#Status
statuses = []
with open("statuses.json", "r") as f:
    statusdata = {
        record["name"]: record
        for record in json.load(f)
    }
    statuses = list(statusdata.keys())


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

    def update(self) -> None:
        """Updates character state at end of turn."""
        for name, status in self.status.items():
            if status is None:
                continue
            status.update()
            if status.count == 0:
                self.status[name] = None
