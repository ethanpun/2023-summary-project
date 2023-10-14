import json
import random


#accuracy
def accuracy(accuracy, attacker, target):
    """
    Determines whether an attack hits the opponent.
    Can be changed by buffs or debuffs (statuses)
    """
    if target.has_status('Phantom'):
        accuracy -= 10
    if attacker.has_status('Nightfall'):
        accuracy += 20
    if accuracy <= 0:
        return False
    elif accuracy >= 100:
        return True
    hit = random.choice([True] * accuracy + [False] * (100 - accuracy))
    if hit:
        return True
    else:
        return False


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


#Status
statuses = []
with open("statuses.json", "r") as f:
    statusdata = {
        record["name"]: record
        for record in json.load(f)
    }
    statuses = list(statusdata.keys())


def new_status(name: str) -> Status:
    """Returns a new instance of the requested status"""
    # ** operator unpacks dict data into keyword arguments
    return Status(**statusdata[name])


def infiltrated(damage):
    """
    Increases the damage taken by 10%
    """
    return abs(damage * 110 / 100)


def instinct(damage):
    """
    Increases damage dealt by 30%
    """
    return abs(damage * 130 / 100)

#Win and lose conditions
def is_defeat(players: list) -> bool:
    """
    Returns True if user lost, else returns False
    """
    if len(players) == 0:
        return True
    return False

def is_victory(enemies: list) -> bool:
    """
    Returns True if user won, else returns False
    """
    if len(enemies) == 0:
        return True
    return False
