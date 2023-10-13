import random

import attacks
import combat
import data


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


class Character:
    """Base class for game characters.

    Attributes:
    name (str): The name of the character.
    status (list): Shows statuses currently inflicted.
    health (int): Max health of character.
    inventory (list): Shows items collected.
    item_equipped (dict): The currently equipped item.

    Methods:
    display_inventory(): Displays a character's inventory
    add_item(str): Adds items collected into the player's inventory
    is_use_item(): Confirms with the player whether they want to use the item
    use_item(str): Uses a selected item in the player's inventory
    heal(x): Restores a character's health by a certain amount.
    take_damage(x): Reduces health of character by x 
    is_defeated(): Returns True if character's health is less than 0, else return False
    display_turn(): Displays the character's turn
    prompt_action(str): Prompts the user for an action
    prompt_check(str): Allows user to check the stats of party or enemy
    prompt_attack(): Prompts the user to choose an attack to use
    attack(str): Attacks a target using one of its attacks
    passive(str): Increases damage by a multiplier under certain conditions
    add_status(str): Adds status to a character 
    remove_status(str): Removes status from a character
    has_status(str): If character has status, returns True, else returns False. 
    get_stats(str): Displays a character's stats
     
    """
    def __init__(self,
                 name: str,
                 health: int,
                 attacks: list["Attack"],
                 inventory: data.Inventory):
        self.name = name
        self.health = health
        self.attacks = attacks
        self.status = []
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
        is_use = input("Use an item? Y/N: ")
        is_use = is_use.lower()
        while is_use != 'y' and is_use != 'n':
            print("Type 'Y' or 'N'.")
            is_use = input("Use an item? Y/N: ")
        if is_use == 'n':
            return False
        elif is_use == 'y':
            return True

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

    def take_damage(self, damage_taken):
        """Reduces health of character by x"""
        self.health -= damage_taken

    def is_defeated(self):
        """Returns True if character's health is less than 0, else return False"""
        if self.health <= 0:
            return True
        return False

    def display_turn(self):
        """Displays the character's turn"""
        print('--------------------------------------------------------')
        print(f"It is {self.name}'s turn.\n")

    def prompt_action(self):
        """Prompts the user for an action"""
        print('Select one of the following actions:')
        print('1. Attack')
        print('2. Target')
        print('3. Stats')
        print('4. Item')
        dec = input('Please choose an action: ')
        print('')
        dec = dec.lower()
        return dec

    def prompt_check(self):
        """Allows user to check the stats of party or enemy"""
        print("Type 'enemy' to see enemy stats, 'party' to see party stats, 'back' to cancel this action.")
        check = input("Choose to check enemy or party stats: ")
        print('')
        return check.lower()

    def prompt_attack(self) -> str:
        """Prompts the user to choose an attack to use"""
        print(f"{self.name}'s Attacks:'")
        for i, attack in enumerate(self.attacks, start=1):
            print(f"{i}. {attack}")
        print("Type 'back' to cancel the attack. Use the numbers corresponding to each ability to attack.")
        atk = input("Select an attack to use: ")
        print('')
        return atk

    def attack(self, target: "Enemy", atk: str) -> bool:
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
            print(f"{target.name} took {damage} damage!")
            target.take_damage(damage)
        if attack.healing:
            self.heal(attack.healing)
        if attack.inflicts:
            status = combat.get_status(attack.inflicts)
            target.add_status(status.name, status.count)
            # Dirty hack for Resonance
            if status.name == "Resonance":
                print(f"{self.name}'s attack leaves a resonating aura around {target.name}!")
            # Dirty hack for Harvest Moon
            if status.name == "Harvest Moon":
                print(f"{self.name}'s attack and accuracy rose!")
        print('\n')
        return True

    def passive(self, target) -> int:
        """Subclasses must implement this method."""
        raise NotImplementedError

    def add_status(self, status, turns):
        """Adds status to a character"""
        for st in combat.statuses:
            if st['name'] == status:
                temp = st.copy()
                temp['count'] = turns
                self.status.append(temp)

    def remove_status(self):
        """Removes status from a character"""
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
            if st['name'] == status:
                return True
        return False

    def get_stats(self):
        """Displays a characters stats"""
        print(f"{self.name}'s stats")
        print(f"HP: {self.health} / 100")
        if self.status == []:
            print('Status: No statuses.')
        else:
            for st in self.status:
                name = st['name']
                description = st['description']
                turns = st['count']
                print(f'Status : {name} , Description : {description} , Turns Remaining : {turns}\n')



#Characters
class Freddy(Character):
    """
    Data for Freddy character that players can choose to play as.

    Attributes:
    status (list): Shows statuses currently inflicted.
    health (int): Max health of character.
    inventory(list): Shows items collected.

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
            
    def passive(self, target: "Enemy"):
        """Increases damage if target is asleep"""
        if target.has_status('Sleeping'):
            return 5
        else:
            return 0


class Bonnie(Character):
    """Data for Bonnie character that players can choose to play as.

    Attributes:
    status (list): Shows statuses currently inflicted.
    health (int): Max health of character.
    inventory(list): Shows items collected.

    Methods:
    passive(str): Increases damage by a multiplier of 1 to 10 if target has resonance
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
        """
        Increases damage by a multiplier of 1 to 10 if target has resonance
        """
        if target.has_status('Resonance'):
            multiplier = random.randint(1, 10)
            return multiplier
        else:
            return 0



class Foxy(Character):
    """
    Data for Foxy character that players can choose to play as.

    Attributes:
    status (list): Shows statuses currently inflicted.
    health (int): Max health of character.
    inventory(list): Shows items collected.

    Methods:
    prompt_attack(): Prompts the user to choose an attack to use
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
            damage = instinct(damage)
            return damage
        else:
            return 0



class Chica(Character):
    """
    Data for Chica character that players can choose to play as.

    Attributes:
    status (list): Shows statuses currently inflicted.
    health (int): Max health of character.
    inventory(list): Shows items collected.

    Methods:
    prompt_attack(): Prompts the user to choose an attack to use
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
        if self.cupcake != None:
            target.take_damage(20)
            print(f'The cupcake exploded and dealt 20 damage to {target.name}!')
        else:
            self.heal(10)
            print(f"The cupcake healed {self.name}'s HP!")
