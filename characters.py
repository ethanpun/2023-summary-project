import random

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
    target(str): Prompts the user to select a target
    prompt_check(str): Allows user to check the stats of party or enemy
    prompt_attack(): Prompts the user to choose an attack to use
    attack(str): Attacks a target using one of its attacks
    passive(str): Increases damage by a multiplier under certain conditions
    add_status(str): Adds status to a character 
    remove_status(str): Removes status from a character
    has_status(str): If character has status, returns True, else returns False. 
    get_stats(str): Displays a character's stats
     
    """
    def __init__(self, name, status=None, health=100, inventory=None):
        self.name = name
        self.health = health
        self.status = status if status is not None else []
        self.item_equipped = None
        self.inventory = inventory

    def display_inventory(self):
        """Displays a character's inventory"""
        print("Inventory:")
        if self.inventory.is_empty():
            print("You don't have any items currently.")
        else:
            for item in self.inventory.items():
                name = item['name']
                description = item['description']
                effect = item['effect']
                consumable = item['consumable']
                print(f'Item : {name}  /\t Description : {description}  /\t Effect : {effect}  /\t Consumable : {consumable}')

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

    def use_item(self, item):
        """Uses a selected item in the player's inventory"""
        for it in self.inventory.items():
            if it['name'] == item:
                if not it['consumable']:  # If item can't be consumed
                    print("You can't consume this item.")
                    return False
                if it['type'] == 'healing':  # If item is healing
                    self.heal(it['heal'])
                    self.inventory.remove_item(it)
                    return True
                elif it['type'] == 'weapon':  # If item is weapon
                    if self.items_equipped != None:
                        print('You already have a weapon equipped.')
                        return False
                    else:
                        self.items_equipped.append(it)
                        name = it['name']
                        print(f'{self.name} has equipped {name}.')
                        self.inventory.remove_item(it)
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

    def target(self, enemies):
        """Prompts the user to select a target"""
        print('To target enemies, input a number, with the leftmost enemy being 1.')
        i = 1
        for enemy in enemies:
            print(f"{i}. {enemy.name} / HP : {enemy.health}")
            i += 1
        print('')
        target = input('Choose an enemy to target: ')
        print('')
        return target

    def prompt_check(self):
        """Allows user to check the stats of party or enemy"""
        print("Type 'enemy' to see enemy stats, 'party' to see party stats, 'back' to cancel this action.")
        check = input("Choose to check enemy or party stats: ")
        print('')
        return check.lower()

    def prompt_attack(self):
        """Prompts the user to choose an attack to use.
        Subclasses must implement this method.
        """
        raise NotImplementedError

    def attack(self, target, atk):
        """Attacks a target using one of its attacks"""
        damage = 0
        damage += self.passive(target)
        if self.item_equipped != None:
            damage += self.item_equipped['damage']
        if atk == '1':
            print(f'Freddy used Mic Toss on {target.name}!')
            if combat.accuracy(90, self, target) == True:
                damage += 15
                print(f"{target.name} took {damage} damage!")
                target.take_damage(damage)
            else:
                print('The attack missed!')
        if atk == '2':
            print(f'Freddy used Sing on {target.name}!')
            if combat.accuracy(40, self, target) == True:
                target.add_status('Sleeping', 2)
            else:
                print('The attack missed!')
        if atk == '3':
            print(f'Freddy used The Bite on {target.name}!')
            if combat.accuracy(19, self, target) == True:
                damage += 87
                print(f"{target.name} took {damage} damage!")
                target.take_damage(damage)
            else:
                print('The attack missed!')
        print('\n')

    def passive(self, target):
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
    prompt_attack(): Prompts the user to choose an attack to use
    attack(str): Attacks a target using one of its attacks
    passive(str): Increases damage if target is asleep  
    """
    def __init__(self, status=None, health=100, inventory=None):
        self.name = 'Freddy Fazbear'
        self.health = health
        self.status = status if status is not None else []
        self.item_equipped = None
        
    def prompt_attack(self):
        """
        Prompts the user to choose an attack to use
        """
        print(f"{self.name}'s Attacks:'")
        print('1. Mic Toss  90 acc  15 dmg')
        print('2. Sing  40 acc - dmg')
        print('3. The Bite  19 acc 87 dmg')
        print("Type 'back' to cancel the attack. Use the numbers corresponding to each ability to attack.")
        atk = input("Select an attack to use: ")
        print('')
        return atk.lower()

    def attack(self, target, atk):
        """
        Attacks a target using one of its attacks
        """
        damage = 0
        damage += self.passive(target)
        if self.item_equipped != None:
            damage += self.item_equipped['damage']
        if atk == '1':
            print(f'Freddy used Mic Toss on {target.name}!')
            if combat.accuracy(90, self, target) == True:
                damage += 15
                print(f"{target.name} took {damage} damage!")
                target.take_damage(damage)
            else:
                print('The attack missed!')
        if atk == '2':
            print(f'Freddy used Sing on {target.name}!')
            if combat.accuracy(40, self, target) == True:
                target.add_status('Sleeping', 2)
            else:
                print('The attack missed!')
        if atk == '3':
            print(f'Freddy used The Bite on {target.name}!')
            if combat.accuracy(19, self, target) == True:
                damage += 87
                print(f"{target.name} took {damage} damage!")
                target.take_damage(damage)
            else:
                print('The attack missed!')
        print('\n')

            
    def passive(self, target):
        """
        Increases damage if target is asleep
        """
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
    prompt_attack(): Prompts the user to choose an attack to use
    attack(str): Attacks a target using one of its attacks
    passive(str): Increases damage by a multiplier of 1 to 10 if target has resonance
    """
    def __init__(self, status=None, health=100, inventory=None):
        self.name = 'Bonnie'
        self.health = health
        self.status = status if status is not None else []
        self.item_equipped = None
        
    def prompt_attack(self):
        """
        Prompts the user to choose an attack to use
        """
        print(f"{self.name}'s attacks:'")
        print('1. Rift  90 acc  15 dmg')
        print('2. Guitar crash  40 acc 10 dmg')
        print("3. Rock 'n' Roll  25 acc 25*n dmg, n ranges from 1 to 5.")
        print("Type 'back' to cancel the attack. Use the numbers corresponding to each ability to attack.")
        atk = input("Select an attack to use: ")
        print('')
        return atk.lower()

    def attack(self, target, atk):
        """
        Attacks a target using one of its attacks
        """
        damage = 0
        damage += self.passive(target)
        if self.item_equipped != None:
            damage += self.item_equipped['damage']
        if atk == '1':
            print(f'{self.name} used Rift on {target.name}!')
            if combat.accuracy(90, self, target) == True:
                damage += 15
                print(f"{target.name} took {damage} damage!")
                target.take_damage(damage)
            else:
                print('The attack missed!')
        if atk == '2':
            print(f'{self.name} used Guitar Crash on {target.name}!')
            if combat.accuracy(40, self, target) == True:
                damage += 10
                self.heal(10)
                print(f"{target.name} took {damage} damage!")
                target.add_status('Resonance', 3)
                target.take_damage(damage)
                print(f"{self.name}'s attack leaves a resonating aura around {target.name}!")
            else:
                print('The attack missed!')
        if atk == '3':
            print(f"{self.name} used Rock 'n' Roll on {target.name}!")
            if combat.accuracy(40, self, target) == True:
                hits = random.randint(1, 5)
                damage += 25*hits
                print(f'{target.name} was hit {hits} times!')
                print(f"{target.name} took {damage} damage!")
                target.take_damage(damage)
            else:
                print('The attack missed!')
        print('\n')
            
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
    def __init__(self, status=None, health=100, inventory=None):
        self.name = 'Foxy'
        self.health = health
        self.status = status if status is not None else []
        self.item_equipped = None
        
    def prompt_attack(self):
        print(f"{self.name}'s attacks:'")
        print('1. Yar-Har  90 acc  15 dmg')
        print('2. Harvest Moon  - acc - dmg')
        print("3. Death Grip  25 acc 125 dmg")
        print("Type 'back' to cancel the attack. Use the numbers corresponding to each ability to attack.")
        atk = input("Select an attack to use: ")
        print('')
        return atk.lower()

    def attack(self, target, atk):
        """
        Prompts the user to choose an attack to use
        """
        damage = 0
        if self.item_equipped != None:
            damage += self.item_equipped['damage']
        if atk == '1':
            print(f'{self.name} used Yar-Har on {target.name}!')
            if combat.accuracy(90, self, target) == True:
                damage += 15
                damage += self.passive(damage)
                if self.has_status('Nightfall'):
                    damage += 15
                    self.heal(20)
                    print(f"{self.name} leeched {target.name}'s health!")
                print(f"{target.name} took {damage} damage!")
                target.take_damage(damage)
            else:
                print('The attack missed!')
        if atk == '2':
            print(f'{self.name} used Harvest Moon!')
            print(f"{self.name}'s attack and accuracy rose!")
            self.add_status('Nightfall', 5)
        if atk == '3':
            print(f"{self.name} used Death Grip on {target.name}!")
            if combat.accuracy(25, self, target) == True:
                damage += 125
                damage += self.passive(damage)
                if self.has_status('Nightfall'):
                    damage += 15
                    self.heal(20)    
                    print(f"{self.name} leeched {target.name}'s health!")
                print(f"{target.name} took {damage} damage!")
                target.take_damage(damage)
            else:
                print('The attack missed!')
        print('\n')
            
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
    def __init__(self, status=None, health=100, inventory=None, cupcake=None):
        self.name = 'Chica'
        self.health = health
        self.status = status if status is not None else []
        self.item_equipped = None
        self.cupcake = cupcake
        
    def prompt_attack(self):
        """
        Prompts the user to choose an attack to use
        """
        print(f"{self.name}'s attacks:'")
        print('1. Pizza slice  90 acc  15 dmg')
        print('2. Cupcake decoy  - acc - dmg')
        print("3. Devour  69 acc 30 dmg")
        print("Type 'back' to cancel the attack. Use the numbers corresponding to each ability to attack.")
        atk = input("Select an attack to use: ")
        print('')
        return atk.lower()

    def attack(self, target, atk):
        """
        Attacks a target using one of its attacks
        """
        damage = 0
        self.passive(target)
        if self.item_equipped != None:
            damage += self.item_equipped['damage']
        if atk == '1':
            print(f'{self.name} used Pizza slice on {target.name}!')
            if combat.accuracy(90, self, target) == True:
                damage += 15
                print(f"{target.name} took {damage} damage!")
                target.take_damage(damage)
            else:
                print('The attack missed!')
        if atk == '2':
            if self.cupcake != None:
                print(f'{self.name} used Cupcake decoy!')
                print(f'{self.name} placed a cupcake in place of her.')
                self.cupcake = 50
            else:
                print('There is already a cupcake in place!')
        if atk == '3':
            print(f"{self.name} used Devour on {target.name}!")
            if combat.accuracy(40, self, target) == True:
                if self.cupcake > 0:
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
        print('\n')

            
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
