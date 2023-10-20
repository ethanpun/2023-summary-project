import random

from attacks import Attack
import attacks
import combat
from common import Combatant
import data
import text


class Character(Combatant):
    """Base class for game characters.

    Attributes:
    inventory (list): Shows items collected.
    item_equipped (dict): The currently equipped item.

    Methods:
    display_inventory(): Displays a character's inventory
    add_item(str): Adds items collected into the player's inventory
    is_use_item(): Confirms with the player whether they want to use the item
    use_item(str): Uses a selected item in the player's inventory
    heal(x): Restores a character's health by a certain amount.
    display_turn(): Displays the character's turn
    prompt_check(str): Allows user to check the stats of party or enemy
    prompt_attack(): Prompts the user to choose an attack to use
    attack(str): Attacks a target using one of its attacks
    get_stats(str): Displays a character's stats
     
    """
    def __init__(self,
                 name: str,
                 health: int,
                 attacks: list[Attack],
                 inventory: data.Inventory):
        self.name = name
        self.health = health
        self.attacks = attacks
        self.status: dict[str, "combat.Status | None"] = {
            status: None
            for status in combat.statuses
        }
        self.item_equipped = None
        self.inventory = inventory

    def display_inventory(self):
        """Displays a character's inventory"""
        print("Inventory:")
        if self.inventory.is_empty():
            print("You don't have any items currently.")
        else:
            for item in self.inventory.items():
                print(f'Item : {item.name}  /\t Description : {item.description}  /\t Effect : {item.effect}  /\t Consumable : {item.consumable}')

    def add_item(self, item: data.Item):
        """Adds items collected into the player's inventory"""
        for item in data.all_items:
            if item.name == item:
                self.inventory.add_item(item)

    def is_use_item(self):
        """Confirms with the player whether they want to use the item"""
        choice = text.prompt_valid_choice(
            ["Y", "N"],
            inline=True,
            prompt="Use an item?",
        )
        if choice == 0:
            return 'y'
        elif choice == 1:
            return 'n'

    def use_item(self, name: str):
        """Uses a selected item in the player's inventory"""
        for item in self.inventory.items():
            if item.name == item:
                if not item.consumable:  # If item can't be consumed
                    print("You can't consume this item.")
                    return False
                if item.type == 'healing':  # If item is healing
                    self.heal(item.heal)
                    self.inventory.remove_item(item)
                    return True
                elif item.type == 'weapon':  # If item is weapon
                    if self.items_equipped != None:
                        print('You already have a weapon equipped.')
                        return False
                    else:
                        self.items_equipped.append(item)
                        name = item.name
                        print(f'{self.name} has equipped {name}.')
                        self.inventory.remove_item(item)
                        return True
        print("You don't have this item.")
        return False

    def heal(self, amnt):
        """Restores a character's health by a certain amount."""
        self.health += amnt
        print(f"{self.name} healed {amnt} hp!")

    def display_turn(self):
        """Displays the character's turn"""
        print('--------------------------------------------------------')
        print(f"It is {self.name}'s turn.\n")

    def prompt_check(self):
        """Allows user to check the stats of party or enemy"""
        choice = text.prompt_valid_choice(
            ["Enemy", "Party"],
            cancel=True,
            prelude="You can check the following stats:",
            prompt="Choose stats to check",
        )
        if choice == 0:
            return "enemy"
        elif choice == 1:
            return "party"
        elif choice is None:
            return 'back'

    def prompt_attack(self) -> int | str:
        """Prompts the user to choose an attack to use"""
        choice = text.prompt_valid_choice(
            [a.name for a in self.attacks],
            cancel=True,
            prelude=f"{self.name}'s Attacks:",
            prompt="Select an attack to use",
        )
        return 'back' if choice is None else choice

    def attack(self, target: Combatant, atk: str) -> bool:
        """Attacks a target using one of its attacks.
        Returns True if the attack succeeded, otherwise False.
        """
        damage = 0
        damage += self.passive(target)
        if self.item_equipped:
            damage += self.item_equipped.damage
        assert atk in "123"
        attack = self.attacks[int(atk) - 1]
        print(f'{self.name} used {attack.name} on {target.name}!')
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
            if target.has_status('Infiltrated'):
                damage = combat.infiltrated(damage)
            print(f"{target.name} took {damage} damage!")
            target.take_damage(damage)
        if attack.healing:
            self.heal(attack.healing)
        if attack.inflicts:
            target.add_status(attack.inflicts)
            # Dirty hack for Resonance
            if attack.inflicts.name == "Resonance":
                print(f"{self.name}'s attack leaves a resonating aura around {target.name}!")
            # Dirty hack for Harvest Moon
            if attack.inflicts.name == "Harvest Moon":
                print(f"{self.name}'s attack and accuracy rose!")
        print('\n')
        return True

    def passive(self, target: Combatant) -> int:
        """Subclasses must implement this method."""
        raise NotImplementedError

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



#Characters
class Freddy(Character):
    """Data for Freddy character that players can choose to play as.

    Methods:
    passive(str): Increases damage if target is asleep  
    """
    def __init__(self,
                 health: int,
                 inventory: data.Inventory):
        super().__init__(
            'Freddy Fazbear',
            health,
            [
                attacks.get("Mic Toss"),
                attacks.get("Sing"),
                attacks.get("The Bite"),
            ],
            inventory
        )
            
    def passive(self, target: Combatant):
        """Increases damage if target is asleep"""
        if target.has_status('Sleeping'):
            return 5
        else:
            return 0


class Bonnie(Character):
    """Data for Bonnie character that players can choose to play as.

    Methods:
    passive(str): Increases damage by a multiplier of 1 to 10
                  if target has resonance
    """
    def __init__(self,
                 health: int,
                 inventory: data.Inventory):
        super().__init__(
            'Bonnie',
            health,
            [
                attacks.get("Rift"),
                attacks.get("Guitar Crash"),
                attacks.get("Rock 'n' Roll"),
            ],
            inventory
        )
            
    def passive(self, target):
        """Increases damage by a multiplier of 1 to 10
        if target has resonance
        """
        if target.has_status('Resonance'):
            multiplier = random.randint(1, 10)
            return multiplier
        else:
            return 0



class Foxy(Character):
    """Data for Foxy character that players can choose to play as.

    Methods:
    attack(str): Attacks a target using one of its attacks
    passive(str): Increases damage by 30% if Foxy has less than half health
    """
    def __init__(self,
                 health: int,
                 inventory: data.Inventory):
        super().__init__(
            'Foxy',
            health,
            [
                attacks.get("Yar-Har"),
                attacks.get("Harvest Moon"),
                attacks.get("Death Grip"),
            ],
            inventory
        )

    def attack(self, target, atk) -> bool:
        """
        Prompts the user to choose an attack to use
        """
        assert atk in "123"
        attack = self.attacks[int(atk) - 1]
        success = super().attack(target, atk)
        if not success:
            return success
        if attack.name == "Harvest Moon":
            return success
        damage = 0
        if self.has_status('Nightfall'):
            damage += 15
            self.heal(20)
            print(f"{self.name} leeched {target.name}'s health!")
            print(f"{target.name} took {damage} damage!")
            target.take_damage(damage)
        print('\n')
        return success
            
    def passive(self, damage):
        """
        Increases damage by 30% if Foxy has less than half health
        """
        if self.health < 50:
            damage = combat.instinct(damage)
            return damage
        else:
            return 0



class Chica(Character):
    """Data for Chica character that players can choose to play as.

    Attributes:
    inventory(list): Shows items collected.

    Methods:
    attack(str): Attacks a target using one of its attacks
    passive(str): If cupcake is present, heals Chica for 10 each turn. When cupcake is destroyed, deals 20 damage to targetted opponent
    """
    def __init__(self,
                 health: int,
                 inventory: data.Inventory):
        super().__init__(
            'Chica',
            health,
            [
                attacks.get("Pizza Slice"),
                attacks.get("Cupcake Decoy"),
                attacks.get("Devour"),
            ],
            inventory
        )
        self.cupcake = None

    def attack(self, target, atk):
        """
        Attacks a target using one of its attacks
        """
        assert atk in "123"
        attack = self.attacks[int(atk) - 1]
        if attack.name == "Cupcake Decoy":
            if self.cupcake:
                print(f'{self.name} used Cupcake decoy!')
                print(f'{self.name} placed a cupcake in place of her.')
                self.cupcake = 50
            else:
                print('There is already a cupcake in place!')
            print('\n')
            return True
        elif attack.name == "Devour":
            if combat.accuracy(40, self, target):
                damage = 0
                if self.cupcake and self.cupcake > 0:
                    damage += 125
                    print(f"{self.name} devoured the cupcake. Damage Increased.")
                    print(f"{target.name} took {damage} damage!")
                    self.cupcake = 0

                else:
                    damage += 30
                    print(f"{target.name} took {damage} damage!")
                target.take_damage(damage)
            else:
                print('The attack missed!')
                return False
            print('\n')
            return True
        else:
            return super().attack(target, atk)

            
    def passive(self, target):
        """
        If cupcake is present, heals Chica for 10 each turn. When cupcake is destroyed, deals 20 damage to targetted opponent
        """
        if self.cupcake is not None:
            target.take_damage(20)
            print(f'The cupcake exploded and dealt 20 damage to {target.name}!')
        else:
            self.heal(10)
            print(f"The cupcake healed {self.name}'s HP!")
