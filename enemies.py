import random
import time

from attacks import Attack
import attacks
import combat
from common import Combatant


class Enemy(Combatant):
    """Base class for all enemies

    Methods:
    display_turn(): Displays the characters turn 
    get_stats(str): Displays a characters stats
    attack(target): Attacks a target using one of its attacks
    """

    def __init__(self,
                 name: str,
                 health: int,
                 attacks: list[attacks.Attack]):
        super().__init__(name, health)
        self.attacks = attacks

    def display_turn(self):
        """Displays the characters turn"""
        print('--------------------------------------------------------')
        print(f"It is {self.name}'s turn.")

    def get_stats(self):
        """Displays a characters stats"""
        print(f"{self.name}'s stats")
        print(f"HP: {self.health} / 100")
        if all(status is None for status in self.status.values()):
            print('Status: No statuses.')
        else:
            for name, status in self.status.items():
                if status is None:
                    continue
                print(f'Status : {name} , Description : {status.description} , Turns Remaining : {status.count}\n')

    def select_attack(self) -> Attack:
        """Select an attack to use in combat"""
        attack = random.choice(self.attacks)
        return attack

    def get_attack_damage(self, target: Combatant, attack: Attack, damage: int = 0) -> int:
        """Determines the damage to be dealt to target by attack, and returns it."""
        if not attack.damage:
            return 0
        if attack.repeats:
            lower, upper = attack.repeats
            hits = random.randint(lower, upper)
        else:
            hits = 1
        damage += attack.damage * hits
        return damage

    def attack(self, target: Combatant) -> bool:
        """Attacks a target using one of its attacks.
        Returns True if the attack succeeded, otherwise False.
        """
        attack = self.select_attack()
        if not attack:
            print(f"{self.name} has no attacks available!")
            return False

        print(f"{self.name} used {attack.name} on {target.name}!")
        
        # If attack has accuracy, determine if attack misses
        if attack.accuracy and not combat.accuracy(attack.accuracy, self, target):
            print('The attack missed!')
            return False
        # Attack hits
        damage = self.get_attack_damage(target, attack)
        print(f"{target.name} took {damage} damage!")
        target.take_damage(damage)
        print('\n')
        return True


class Boss(Enemy):
    """Base class for bosses.

    Attributes:
    next_phase (Boss | None)
      The next phase of the boss

    Methods:
    encounter(): Displays dialogue when encountering boss
    """
    next_phase: "type[Boss] | None" = None

    def encounter(self) -> None:
        raise NotImplementedError


class GB(Enemy):
    """Basic common enemy found roaming the rooms."""

    def __init__(self, health=50):
        super().__init__(
            'Glitch Bunny',
            health,
            [
                attacks.get("Bash"),
                attacks.get("Ram"),
            ],
        )


class BB(Enemy):
    """Basic common enemy found roaming the rooms."""
    def __init__(self, health=75):
        super().__init__(
            'Balloon Boy',
            health,
            [
                attacks.get("Twirl"),
                attacks.get("Balloon Entanglement"),
            ],
        )


class Springtrap(Boss):
    """The boss that the player has to defeat in order to win."""
    def __init__(self, health=250):
        super().__init__(
            'Springtrap',
            health,
            [
                attacks.get("Phantom Mirage"),
                attacks.get("Decaying Grasp"),
                attacks.get("Eternal Torment"),
            ],
        )
        self.next_phase = Glitchtrap

    def encounter(self) -> None:
        """Plays dialogue when encountering Springtrap, notifying the player."""
        print('You notice the pungent smell of decaying matter.')
        time.sleep(2)
        print(
            'Then, you hear the clanking of metal wires and robotic movement.')
        time.sleep(2)
        print(
            'Finally, you see a haunted amalgamation of wires and memories emerge from the shadows.'
        )
        time.sleep(3)
        print('Springtrap.')

    def get_attack_damage(self, target: Combatant, attack: Attack, damage: int = 0) -> int:
        damage = self.get_attack_damage(target, attack)
        if target.has_status('Infiltrated'):
            damage = combat.infiltrated(damage)
        return damage


class Glitchtrap(Boss):
    """Phase 2 of Springtrap that once defeated will finish the game."""

    def __init__(self, health=275):
        super().__init__(
            'Glitchtrap',
            health,
            [
                attacks.get("Corrupt"),
                attacks.get("Digital Infiltration"),
                attacks.get("System Overload"),
                attacks.get("Pixel Blast"),
            ],
        )

    def encounter(self) -> None:
        """Turns Springtrap into Glitchtrap, initialising phase 2"""
        print('Or has he?')
        time.sleep(2)
        print(
            'Springtrap: Did you really think this would be enough to finish me?'
        )
        time.sleep(2)
        print(
            'Springtrap: I am the embodiment of your fears and uncertainties, now merged and given form.'
        )
        time.sleep(3)
        print('Springtrap: A glitch in the system, a fracture in reality. Witness the merging of two worlds.')
        time.sleep(3)
        print(
            'You watch as the decaying bunny is encapsulated in digital code, turning him into another bunny with stitches running down his sides as he chuckles.'
        )
        time.sleep(5)
        print('Glitchtrap: The time of reckoning, has begun.')

    def select_attack(self) -> Attack | str:
        """Select an attack to use in combat"""
        attack = combat.dice_roll({
            self.attacks[0]: 28,
            self.attacks[1]: 17,
            self.attacks[2]: 14,
            self.attacks[3]: 40,
            "Griddy": 1
        })
        return attack

    def get_attack_damage(self, target: Combatant, attack: Attack, damage: int = 0) -> int:
        damage = self.get_attack_damage(target, attack)
        if target.has_status('Infiltrated'):
            damage = combat.infiltrated(damage)
        return damage

    def attack(self, target: Combatant, attack: Attack):
        print(f"{self.name} attacks {target.name}!")
        if attack == "Griddy":
            print(f'{self.name} hit the Griddy!') 
            print(f'{target.name} was traumatised and stared in disgust.')
            return True
        if not attack:
            print(f"{self.name} has no attacks available!")
            return
        damage = 0
        print(f"{self.name} used {attack.name} on {target.name}!")
        # If attack has accuracy, determine if attack misses
        if attack.accuracy and not combat.accuracy(attack.accuracy, self, target):
            print('The attack missed!')
            return False
        # Attack hits
        if attack.damage:
            if attack.repeats:
                lower, upper = attack.repeats
                hits = random.randint(lower, upper)
                print(f'{target.name} was hit {hits} times!')
            else:
                hits = 1
            damage += attack.damage * hits
            
            print(f"{target.name} took {damage} damage!")
            target.take_damage(damage)
        print('\n')

    
