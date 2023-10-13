import json
from typing import Sequence


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


with open("attacks.json", "r") as f:
    all_attacks = {
        record["name"]: Attack(**record)
        for record in json.load(f)
    }

def get(name: str) -> Attack:
    """Returns an attack by name"""
    return all_attacks[name]