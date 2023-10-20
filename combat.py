import random

from common import Combatant


def dice_check(success: int) -> bool:
    """Roll a dice to check success.

    Arguments
    ---------
    - success: int
      The chance of success, from 0 to 100.

    Return: True if successful, False if unsuccessful.
    """
    return random.randint(0, 100) <= success


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
    return dice_check(accuracy)


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


class Party:
    """A group of combatants on the same side"""
    def __init__(self, members: list[Combatant]):
        # Do not reference members argument directly
        # to avoid inadvertent mutation
        self._members = []
        for member in members:
            self._members.append(member)

    def append(self, member: Combatant) -> bool:
        """Add combatant to party.
        Return True if successful, otherwise False
        """
        self._members.append(member)
        return True

    def is_defeated(self) -> bool:
        """Return True if all party members are defeated"""
        return all(member.is_defeated() for member in self._members)

    def members(self) -> list[Combatant]:
        """Return a list of all party members"""
        return self._members.copy()

    def remove(self, name: str) -> bool:
        """Remove first member with given name.
        Return True if successful, otherwise False
        """
        for i, member in self._members:
            if member.name == name:
                del self._members[i]
                return True
        return False

    
