import random
import time

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

    def attack(self, target: Combatant):
        """Attacks a target using one of its attacks.
        """
        attack = random.choice(self.attacks)
        if not attack:
            print(f"{self.name} has no attacks available!")
            return
        if combat.accuracy(attack.accuracy, self, target):
            print(f"{self.name} used {attack.name} on {target.name}!")
            damage = attack.damage
            if target.has_status('Infiltrated'):
                damage = combat.infiltrated(damage)
            target.take_damage(damage)
            print(f'{target.name} took {damage} damage.')
        else:
            print('The attack missed!')
        print('\n')


class Boss(Enemy):
    """Base class for bosses.

    Attributes:
    next_phase (Boss | None)
      The next phase of the boss

    Methods:
    encounter(): Displays dialogue when encountering boss
    """
    next_phase: "Boss | None" = None

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

    def attack(self, target: "Character"):
        print(f"{self.name} attacks {target.name}!")
        n = random.randint(1, 3)
        if n == '1':
            print(f'{self.name} used Phantom Mirage!')
            self.add_status('Phantom')
            damage = 7
            if target.has_status('Infiltrated'):
                damage = combat.infiltrated(damage)            
            target.take_damage(damage)
            print(f'{target.name} took {damage} damage.')
        if n == '2':
            if combat.accuracy(40, self, target) == True:
                print(f'{self.name} used Decaying Grasp on {target.name}!')
                damage = 30
                if target.has_status('Infiltrated'):
                    damage = combat.infiltrated(damage)
                target.take_damage(damage)
                print(f'{target.name} took {damage} damage.')
            else:
                print('The attack missed!')
        if n == '3':
            if combat.accuracy(15, self, target) == True:
                print(f'{self.name} used Eternal Torment on {target.name}!')
                damage = 60
                if target.has_status('Infiltrated'):
                    damage = combat.infiltrated(damage)
                target.take_damage(damage)
                print(f'{target.name} took {damage} damage.')
            else:
                print('The attack missed!')
        print('\n')


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

    def attack(self, target):
        print(f"{self.name} attacks {target.name}!")
        n = random.randint(1, 100)
        if n > 30 and n < 60: #28% chance to use this attack
            print(f'{self.name} used Corrupt on {target.name}!')
            if combat.accuracy(50, self, target) == True:   
                damage = 20
                if target.has_status('Infiltrated'):
                    damage = combat.infiltrated(damage)
                target.take_damage(damage)
                print(f"{target.name} took {damage} damage!")
                target.add_status('Corrupted')
                print(f"{target.name} is corrupted!")
            else:
                print('The attack missed!')
        if n > 15 and n < 31: #17% chance to use this attack
            print(f'{self.name} used Digital Infiltration on {target.name}!')
            if combat.accuracy(30, self, target) == True:
                target.add_status('Infiltrated')
                print(f"{self.name} infiltrated {target.name}'s system!")
            else:
                print('The attack missed!')
        if n >= 2 and n < 16: #14% chance to use this attack
            print(f'{self.name} used System Overload on {target.name}!')
            if combat.accuracy(40, self, target) == True:
                damage = 40
                if target.has_status('Infiltrated'):
                    damage = combat.infiltrated(damage)
                target.take_damage(self.damage) 
                print(f"{target.name} took {damage} damage!")
            else:
                print('The attack missed!')
        if n >= 60: #40% chance to use this attack
            print(f'{self.name} used Pixel Blast on {target.name}!')
            if combat.accuracy(70, self, target) == True:
                damage = 15
                if target.has_status('Infiltrated'):
                    damage = combat.infiltrated(damage)
                target.take_damage(self.damage)
                print(f"{target.name} took {damage} damage!")
            else:
                print('The attack missed!')
        if n == 1:  #1% chance to use this attack
            print(f'{self.name} hit the Griddy!') 
            print(f'{target.name} was traumatised and stared in disgust.')
        print('\n')

    
