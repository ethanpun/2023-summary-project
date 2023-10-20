import json

from common import Attack


with open("attacks.json", "r") as f:
    all_attacks = {
        record["name"]: Attack(**record)
        for record in json.load(f)
    }

def get(name: str) -> Attack:
    """Returns an attack by name"""
    return all_attacks[name]