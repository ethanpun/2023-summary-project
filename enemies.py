import random
import time

import attacks
import combat


class Enemy:
    """Base class for all enemies

    Attributes:
    name (str): Name of enemy
    status (list): Shows statuses currently inflicted.
    health (int): Max health of enemy

    Methods:
    attack(character)
    take_damage(x): Reduces health of character by x 
    is_defeated(): Returns True if characters health is less than 0, else return False
    display_turn(): Displays the characters turn
    add_status(str): Adds status to a character 
    remove_status(str): Removes status from a character
    has_status(str): If character has status, returns True, else returns False. 
    get_stats(str): Displays a characters stats
    attack(str): Attacks a target using one of its attacks 
    """

    def __init__(self,
                 name: str,
                 health: int,
                 attacks: list[attacks.Attack],
                 status=None):
        self.name = name
        self.health = health
        self.max_health = health
        self.attacks = attacks
        self.status = status if status is not None else []

    def take_damage(self, damage: int):
        """Reduces health based on damage done"""
        self.health -= damage

    def is_defeated(self):
        """Returns True if characters health is less than 0, else return False"""
        if self.health <= 0:
            return True
        return False

    def display_turn(self):
        """Displays the characters turn"""
        print('--------------------------------------------------------')
        print(f"It is {self.name}'s turn.")

    def add_status(self, status, turns):
        """Adds status to a character"""
        for st in combat.statuses:
            if st['name'] == status:
                temp = st.copy()
                temp['count'] = turns
                self.status.append(temp)

    def remove_status(self):
        """
        Removes status from a character
        """
        for st in self.status:
            st['count'] -= 1
            if st['count'] == 0:
                name = st['name']
                print(f'{self.name} is no longer {name}!')
                self.status.remove(st)

    def has_status(self, status):
        """
        If character has status, returns True, else returns False.
        """
        for st in self.status:
            print (st)
            if st['name'] == status:
                return True
        return False

    def get_stats(self):
        """Displays a characters stats"""
        print(f"{self.name}'s stats")
        print(f"HP: {self.health} / {self.max_health}")
        if self.status == []:
            print('Status: No statuses.')
        else:
            for st in self.status:
                name = st['name']
                description = st['description']
                turns = st['count']
                print(f'Status : {name}  /\t Description : {description}  /\t Turns Remaining : {turns}')

    def attack(self, target: "Character"):
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


class GB(Enemy):
    """Basic common enemy found roaming the rooms."""

    def __init__(self, status=None, health=50):
        super().__init__(
            'Glitch Bunny',
            health,
            [
                attacks.get("Bash"),
                attacks.get("Ram"),
            ],
            status
        )


class BB(Enemy):
    """Basic common enemy found roaming the rooms."""
    def __init__(self, status=None, health=75):
        super().__init__(
            'Balloon Boy',
            health,
            [
                attacks.get("Twirl"),
                attacks.get("Balloon Entanglement"),
            ],
            status
        )


class Springtrap(Enemy):
    """The boss that the player has to defeat in order to win.

    Methods:
    encounter(): Displays dialogue when encountering Springtrap
    """
    def __init__(self, status=None, health=250):
        super().__init__(
            'Springtrap',
            health,
            [
                attacks.get("Phantom Mirage"),
                attacks.get("Decaying Grasp"),
                attacks.get("Eternal Torment"),
            ],
            status
        )

    def encounter(self):
        """
        Plays dialogue when encountering Springtrap, notifying the player.
        """
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
            self.add_status('Phantom', 1)
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


class Glitchtrap(Enemy):
    """Phase 2 of Springtrap that once defeated will finish the game.
    
    Methods:
    spawn(): Turns Springtrap into Glitchtrap, initialising phase 2
    """

    def __init__(self, status=None, health=275):
        super().__init__(
            'Glitchtrap',
            health,
            [
                attacks.get("Corrupt"),
                attacks.get("Digital Infiltration"),
                attacks.get("System Overload"),
                attacks.get("Pixel Blast"),
            ]
            status)

    def spawn():
        """
        Turns Springtrap into Glitchtrap, initialising phase 2
        """
        if Springtrap.health <= 0:
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
                target.add_status('Corrupted', 1)
                print(f"{target.name} is corrupted!")
            else:
                print('The attack missed!')
        if n > 15 and n < 31: #17% chance to use this attack
            print(f'{self.name} used Digital Infiltration on {target.name}!')
            if combat.accuracy(30, self, target) == True:
                target.add_status('infiltrated', 1)
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

    
