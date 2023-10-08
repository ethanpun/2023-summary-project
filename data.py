import random
import time
import json 

#Inventory and Items
with open("items.json", "r") as f:
    all_items = json.load(f)

player_inventory = []

def get_inventory():
    return player_inventory

def add_item(item):
    player_inventory.append(item)
    print(f'You obtained {item}.\n')

def display_inventory():
    print("Inventory:")
    if len(player_inventory) == 0:
        print("You don't have any items currently.")
    else:
        for item in player_inventory:
            for x in all_items:
                if x['name'] == item:
                    name = x['name']
                    description = item['description']
                    effect = item['effect']
                    consumable = item['consumable']
            print(f'Item : {name}  /\t Description : {description}  /\t Effect : {effect}  /\t Consumable : {consumable}')
    print('--------------------------------------------------------')
        

#Rooms
total_rooms = 0
def increment_total_rooms():
    global total_rooms
    return total_rooms + 1

def start_room():
    """Instantiates a spawn room"""
    current_room = Room(type = 'start')
    return current_room
    
class Room:
    def __init__(self, boss = None, type = 'normal', x = 2, y = 2, up = None, down = None, left = None, right = None, layer = 1, number = 0):
        #next rooms
        self.boss = boss
        self.type = type
        self.up = up
        self.down = down 
        self.right = right
        self.left = left
        self.layer = layer
        self.number = number
        connections = random.randint(2, 3)
        next_rooms = [self.up, self.down, self.left, self.right]
        ref_next_rooms = ['self.up', 'self.down', 'self.left', 'self.right']
        i = 0
        for _ in range(len(next_rooms)):
            if next_rooms[i] != None:
                next_rooms.pop(i)
                ref_next_rooms.pop(i)
                i -= 1
            i += 1
        if self.type == 'start':
            #Start Room
            self.up = Room(down = self, number = self.count_room())
        elif total_rooms < 10 and self.layer < 3:
            #Normal Room
            while connections != 0:
                next_room = random.randint(0, len(next_rooms) - 1)
                if ref_next_rooms[next_room] == 'self.up':
                    self.up = Room(down = self, layer=self.count_layer(), number = self.count_room())
                    increment_total_rooms()
                    next_rooms.pop(next_room)
                    ref_next_rooms.pop(next_room)
                elif ref_next_rooms[next_room] == 'self.down':
                    self.down = Room(up = self, layer=self.count_layer(), number = self.count_room())
                    increment_total_rooms()
                    next_rooms.pop(next_room)
                    ref_next_rooms.pop(next_room)
                elif ref_next_rooms[next_room] == 'self.left':
                    self.left = Room(right = self, layer=self.count_layer(), number = self.count_room())
                    increment_total_rooms()
                    next_rooms.pop(next_room)
                    ref_next_rooms.pop(next_room)
                elif ref_next_rooms[next_room] == 'self.right':
                    self.right = Room(left = self, layer=self.count_layer(), number = self.count_room())
                    increment_total_rooms()
                    next_rooms.pop(next_room)
                    ref_next_rooms.pop(next_room)
                connections -= 1
        #Boss Room
        if self.number == 7:
            next_room = random.randint(0, len(next_rooms) - 1)
            if ref_next_rooms[next_room] == 'self.up':
                self.up = Room(down = self, type = 'boss', boss = Springtrap(), layer=self.count_layer())
                next_rooms.pop(next_room)
                ref_next_rooms.pop(next_room)
            elif ref_next_rooms[next_room] == 'self.down':
                self.down = Room(up = self, type = 'boss', boss = Springtrap(), layer=self.count_layer(), )
                next_rooms.pop(next_room)
                ref_next_rooms.pop(next_room)
            elif ref_next_rooms[next_room] == 'self.left':
                self.left = Room(right = self, type = 'boss', boss = Springtrap(), layer=self.count_layer())
                next_rooms.pop(next_room)
                ref_next_rooms.pop(next_room)
            elif ref_next_rooms[next_room] == 'self.right':
                self.right = Room(left = self, type = 'boss', boss = Springtrap(), layer=self.count_layer())
                next_rooms.pop(next_room)
                ref_next_rooms.pop(next_room)
                
        self.grid = Grid(type = type, x = x, y = y)
        
    def display_room(self):
        print(f"Room {self.number}")


    def is_next_room(self, next : str) -> bool:
        if next == 'w':
            return self.up is not None
        elif next == 'a':
            return self.left is not None
        elif next == 's':
            return self.down is not None
        elif next == 'd':
            return self.right is not None
        else:
            print('It seems that this door is locked.')

    def next_room(self, next : str) -> 'Room':
        '''
        User moves to next room. Depending on the input, move to room above, below, left or right. Also, check if next room for given input exists.
        '''
        next = next.lower()
        if next == 'w':
            return self.up
        elif next == 's':
            return self.down
        elif next == 'a':
            return self.left
        elif next == 'd':
            return self.right
    def current_room(self) -> 'Room':
        '''
        Returns the current room
        '''
        return self

    def count_layer(self):
       return self.layer + 1

    def count_room(self):
        return self.number + 1
        
    def is_boss(self):
        if self.type == 'boss':
            return True
        return False

    def get_boss(self):
        '''
        Return the boss.
        '''
        return self.boss

class Grid:
    def __init__(self, type, x, y):
        self.type = type
        self.grid = [{0 : None, 1 : None, 2 : None, 3 : None, 4 : None},
                    {0 : None, 1 : None, 2 : None, 3 : None, 4 : None},
                    {0 : None, 1 : None, 2 : None, 3 : None, 4 : None},
                    {0 : None, 1 : None, 2 : None, 3 : None, 4 : None},
                    {0 : None, 1 : None, 2 : None, 3 : None, 4 : None}]
        if type == 'normal':
        #Spawning creatures
            i = 0
            while i < 5:
                tile_x_coord = random.randint(0, 4)
                tile_y_coord = random.randint(0, 4)
                if self.grid[tile_x_coord][tile_y_coord] == None:
                    enemy_count = random.randint(1, 3)
                    enemy_list = []
                    all_enemies = [GB(),BB()]
                    for _ in range(enemy_count):
                        enemy = random.randint(1, len(all_enemies))
                        if enemy == 1:
                            enemy_list.append(GB())
                        elif enemy == 2:
                            enemy_list.append(BB())
                    self.grid[tile_x_coord][tile_y_coord] = {'type' : 'creature', 'creatures' : enemy_list}
                    i = i + 1
            k = 0
        #Spawning items
            while k < 5:
                tile_x_coord = random.randint(0, 4)
                tile_y_coord = random.randint(0, 4)
                if self.grid[tile_x_coord][tile_y_coord] == None:
                    random_item = random.choice(all_items)
                    self.grid[tile_x_coord][tile_y_coord] = {'type' : 'item', 'item' : random_item}
                    k = k + 1
        self.coordinates = [x, y]

        
    def get_position(self) -> list:
        '''
        Return user position
        '''
        return self.coordinates
    def prompt_movement(self) -> str:
        '''
        Prompt the user for a movement and return the direction to move. Also, to view inventory, user types open inventory
        '''
        print("Type 'wasd' to move, open the inventory by typing 'inventory'")
        action = input('Type an action: ')
        print('--------------------------------------------------------')
        return action.lower()
        
    def move(self, position : list):
        '''
        Update user position and coordinates in the room
        '''
        self.coordinates = position
    
    def is_encounter(self):
        '''
        Return true if user coordinates are currently on a creature tile.
        '''
        if self.grid[self.get_position()[0]][self.get_position()[1]] == None:
            return False
        elif self.grid[self.get_position()[0]][self.get_position()[1]]['type'] == 'creature':
            return True
        return False

    def get_enemies(self):
        '''
        Return the enemies on that tile
        '''
        coordinates = self.get_position()
        return self.grid[coordinates[0]][coordinates[1]]['creatures']
    def is_item(self):
        '''
        Return true if user coordinates are currently on a item tile.
        '''
        if self.grid[self.get_position()[0]][self.get_position()[1]] == None:
            return False
        elif self.grid[self.get_position()[0]][self.get_position()[1]]['type'] == 'item':
            return True
        return False
            
    def get_item(self) -> str:
        '''
        If user is on an item tile, return the item on that tile
        '''
        return self.grid[self.get_position()[0]][self.get_position()[1]]['item']['name']
        
    def clear_tile(self):
        '''
        After a defeating a creature or picking up an item, remove it from the grid
        '''
        self.grid[self.get_position()[0]][self.get_position()[1]] = None



#Start
def start_menu():
    """
    Displays start menu 
    """
        def start_menu():
        print('Welcome to FNAF:Reckoning!')
        choice = input("Type 'Start' to begin: ")
        while choice.lower() != 'start':
            print("To begin the game, enter 'start'.")
            choice = input("Type 'Start' to begin: ")
        print('--------------------------------------------------------')


with open("characters.json", "r") as f:
    char_info = json.load(f)

def info(name: str):
    """
    Displays information of the playable characters
    """
    if name not in char_info:
        return
    character = char_info[name]
    print(f'HP: {character["HP"]}')
    print(f'Description: {character["Description"]}')
    print(f'Passive: {character["Passive"]}')
    print("Attacks:")
    for i, (attack, desc) in enumerate(
        character["Attacks"].items(),
        start=1
    ):
        print(f'{i}. {attack}: {desc}')
    print('--------------------------------------------------------')
    
def choose_character(player):
    """
    Prompts the user to select a character to play as
    """
    print('Characters:')
    for i,character in enumerate(char_info.values(), start=1):
        print(f'{i}. {character["Name"]}')
    cr = input(f"{player}, please select your character or enter 'skip' if you are ready to start the game: ")
    print('--------------------------------------------------------')
    cr = cr.lower()
    if cr == 'skip':
        return cr
    info(cr)
    is_select = input('Select ' + cr.capitalize() + ' as your character? Y/N: ')
    while is_select not in ['y', 'n']:
        is_select = is_select.lower()
        print("Enter 'y' or 'n' to proceed.")
        is_select = input('Select ' + cr.capitalize() + ' as your character? Y/N: ')
    if is_select.lower() == 'y':
        if cr == 'freddy' or cr == 'freddy fazbear':
            print(f'{player} has selected Freddy Fazbear.')
        elif cr == 'bonnie':
            print(f'{player} has selected Bonnie.')
        elif cr == 'chica':
            print(f'{player} has selected Chica.')
        elif cr == 'foxy':
            print(f'{player} has selected Foxy.')
        print('--------------------------------------------------------')
    if is_select.lower() == 'n':
        return choose_character(player)
    return cr
        
#End
def Ending():
    """
    Plays the end sequence after Glitchtrap is defeated
    """
    print('Glitchtrap: No! This cannot be!')
    time.sleep(2)
    print('Glitchtrap: I cannot be defeated by an animatronic!')
    time.sleep(2)
    print('Glitchtrap: You are a product of my creation, I cannot be defeated by the likes of you!')
    time.sleep(3)
    print('Glitchtrap: Whatever, I will find a way to come back,')
    time.sleep(2)
    print('Glitchtrap: I always do.')
    time.sleep(2)
    print('You then hear the blood-curling scream of the dying bunny, followed by the sight of the glitching bunny.')
    time.sleep(3)
    print('Finally, the virus disappears and the room falls into silence.')
    time.sleep(2)
    print('You finally reached the end, for now at least.')



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


#Status
    with open("statuses.json", "r") as f:
        statuses = json.load(f)


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
#Enemies


class GB:
    """
    Basic common enemy found roaming the rooms.

    Attributes:
    status (list): Shows statuses currently inflicted.
    health (int): Max health of character.

    Methods:
    take_damage(x): Reduces health of character by x 
    is_defeated(): Returns True if characters health is less than 0, else return False
    display_turn(): Displays the characters turn
    add_status(str): Adds status to a character 
    remove_status(str): Removes status from a character
    has_status(str): If character has status, returns True, else returns False. 
    get_stats(str): Displays a characters stats
    attack(str): Attacks a target using one of its attacks 
    """

    def __init__(self, status=None, health=50):
        self.name = 'Glitch Bunny'
        self.health = health
        self.status = status if status is not None else []

    def take_damage(self, damage: int):
        """
        Reduces health based on damage done 
        """
        self.health -= damage

    def is_defeated(self):
        """
        Returns True if characters health is less than 0, else return False
        """
        if self.health <= 0:
            return True
        return False

    def display_turn(self):
        """
        Displays the characters turn
        """
        print('--------------------------------------------------------')
        print(f"It is {self.name}'s turn.")

    def add_status(self, status, turns):
        """
        Adds status to a character 
        """
        for st in statuses:
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
        """
        Displays a characters stats
        """
        print(f"{self.name}'s stats")
        print(f"HP: {self.health} / 50")
        if self.status == []:
            print('Status: No statuses.')
        else:
            for st in self.status:
                name = st['name']
                description = st['description']
                turns = st['count']
                print(f'Status : {name}  /\t Description : {description}  /\t Turns Remaining : {turns}')

    def attack(self, target):
        """
        Attacks a target using one of its attacks 
        """
        n = random.randint(1, 100)
        if n < 50:
            if accuracy(50, self, target) == True:
                print(f"{self.name} used Bash on {target.name}!")
                damage = 10
                if target.has_status('Infiltrated'):
                    damage = infiltrated(damage)
                target.take_damage(damage)
                print(f'{target.name} took {damage} damage.')
            else:
                print('The attack missed!')
        else:
            if accuracy(50, self, target) == True:
                print(f"{self.name} used Ram on {target.name}!")
                damage = 15
                if target.has_status('Infiltrated'):
                    damage = infiltrated(damage)
                target.take_damage(damage)
                print(f'{target.name} took {damage} damage.')
            else:
                print('The attack missed!')
        print('\n')


class BB:
    """
    Basic common enemy found roaming the rooms.

    Attributes:
    status (list): Shows statuses currently inflicted.
    health (int): Max health of character.

    Methods:
    take_damage(x): Reduces health of character by x 
    is_defeated(): Returns True if characters health is less than 0, else return False
    display_turn(): Displays the characters turn
    add_status(str): Adds status to a character 
    remove_status(str): Removes status from a character
    has_status(str): If character has status, returns True, else returns False. 
    get_stats(str): Displays a characters stats
    attack(str): Attacks a target using one of its attacks 
    """
    def __init__(self, status=None, health=75):
        self.name = 'Balloon Boy'
        self.health = health
        self.status = status if status is not None else []

    def take_damage(self, damage: int):
        """
        Reduces health of character by x 
        """
        self.health -= damage

    def is_defeated(self):
        """
        Returns True if characters health is less than 0, else return False
        """
        if self.health <= 0:
            return True
        return False

    def display_turn(self):
        """
        Displays the characters turn
        """
        print('--------------------------------------------------------')
        print(f"It is {self.name}'s turn.")

    def add_status(self, status, turns):
        """
        Adds status to a character 
        """
        for st in statuses:
            if st['name'] == status:
                temp = st.copy()
                temp['count'] = turns
                self.status.append(temp)

    def remove_status(self):
        """
        Removes status from a character
        """
        for st in self.status:
            st['counter'] -= 1
            if st['counter'] == 0:
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
        """
        Displays a characters stats
        """
        print(f"{self.name}'s stats")
        print(f"HP: {self.health} / 75")
        if self.status == []:
            print('Status: No statuses.')
        else:
            for st in self.status:
                name = st['name']
                description = st['description']
                turns = st['count']
                print(
                    f'Status : {name}  /\t Description : {description}  /\t Turns Remaining : {turns}'
                )

    def attack(self, target):
        """
        Attacks a target using one of its attacks
        """
        n = random.randint(1, 100)
        if n < 50:
            if accuracy(50, self, target) == True:
                print(f"{self.name} used Twirl on {target.name}!")
                damage = 10
                if target.has_status('Infiltrated'):
                    damage = infiltrated(damage)
                target.take_damage(damage)
                print(f'{target.name} took {damage} damage.')
            else:
                print('The attack missed!')
        else:
            if accuracy(50, self, target) == True:
                print(f"{self.name} used Balloon Entanglement on {target.name}!")
                damage = 20
                if target.has_status('Infiltrated'):
                    damage = infiltrated(damage)
                target.take_damage(damage)
                print(f'{target.name} took {damage} damage.')
            else:
                print('The attack missed!')
        print('\n')


class Springtrap:
    """
    The boss that the player has to defeat in order to win.

    Attributes:
    status (list): Shows statuses currently inflicted.
    health (int): Max health of character.

    Methods:
    take_damage(x): Reduces health of character by x 
    is_defeated(): Returns True if characters health is less than 0, else return False
    display_turn(): Displays the characters turn
    add_status(str): Adds status to a character 
    remove_status(str): Removes status from a character
    has_status(str): If character has status, returns True, else returns False. 
    get_stats(str): Displays a characters stats
    encounter(): Displays dialogue when encountering Springtrap
    attack(str): Attacks a target using one of its attacks 
    """
    def __init__(self, status=None, health=250):
        self.name = 'Springtrap'
        self.health = health
        self.status = status if status is not None else []

    def take_damage(self, damage: int):
        """
        Reduces health of character by x
        """
        self.health -= damage

    def is_defeated(self):
        """
        Returns True if characters health is less than 0, else return False
        """
        if self.health <= 0:
            return True
        return False

    def display_turn(self):
        """
        Displays the characters turn
        """
        print('--------------------------------------------------------')
        print(f"It is {self.name}'s turn.")

    def add_status(self, status, turns):
        for st in statuses:
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
            if st['name'] == status:
                return True
        return False

    def get_stats(self):
        """
        Displays a characters stats
        """
        print(f"{self.name}'s stats")
        print(f"HP: {self.health} / 300")
        if self.status == []:
            print('Status: No statuses.')
        else:
            for st in self.status:
                name = st['name']
                description = st['description']
                turns = st['count']
                print(f'Status : {name}  /\t Description : {description}  /\t Turns Remaining : {turns}')

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

    def attack(self, target):
        """
        Attacks a target using one of its attacks
        """
        print(f"{self.name} attacks {target.name}!")
        n = random.randint(1, 3)
        if n == '1':
            print(f'{self.name} used Phantom Mirage!')
            self.add_status('Phantom', 1)
            damage = 7
            if target.has_status('Infiltrated'):
                damage = infiltrated(damage)            
            target.take_damage(damage)
            print(f'{target.name} took {damage} damage.')
        if n == '2':
            if accuracy(40, self, target) == True:
                print(f'{self.name} used Decaying Grasp on {target.name}!')
                damage = 30
                if target.has_status('Infiltrated'):
                    damage = infiltrated(damage)
                target.take_damage(damage)
                print(f'{target.name} took {damage} damage.')
            else:
                print('The attack missed!')
        if n == '3':
            if accuracy(15, self, target) == True:
                print(f'{self.name} used Eternal Torment on {target.name}!')
                damage = 60
                if target.has_status('Infiltrated'):
                    damage = infiltrated(damage)
                target.take_damage(damage)
                print(f'{target.name} took {damage} damage.')
            else:
                print('The attack missed!')
        print('\n')


class Glitchtrap:
    """
    Phase 2 of Springtrap that once defeated will finish the game

    Attributes:
    status (list): Shows statuses currently inflicted.
    health (int): Max health of character.

    Methods:
    take_damage(x): Reduces health of character by x 
    is_defeated(): Returns True if characters health is less than 0, else return False
    display_turn(): Displays the characters turn
    add_status(str): Adds status to a character 
    remove_status(str): Removes status from a character
    has_status(str): If character has status, returns True, else returns False. 
    get_stats(str): Displays a characters stats
    spawn(): Turns Springtrap into Glitchtrap, initialising phase 2
    attack(str): Attacks a target using one of its attacks 
    """

    def __init__(self, status=None, health=275):
        self.name = 'Glitchtrap'
        self.health = health
        self.status = status if status is not None else []

    def take_damage(self, damage: int):
        """
        Reduces health of character by x
        """
        self.health -= damage

    def is_defeated(self):
        """
        Returns True if characters health is less than 0, else return False
        """
        if self.health <= 0:
            return True
        return False

    def display_turn(self):
        """
        Displays the characters turn
        """
        print('--------------------------------------------------------')
        print(f"It is {self.name}'s turn.")

    def add_status(self, status, turns):
        """
        Adds status to a character
        """
        for st in statuses:
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
            if st['name'] == status:
                return True
        return False

    def get_stats(self):
        """
        Displays a characters stats
        """
        print(f"{self.name}'s stats")
        print(f"HP: {self.health} / 250")
        if self.status == []:
            print('Status: No statuses.')
        else:
            for st in self.status:
                name = st['name']
                description = st['description']
                turns = st['count']
                print(
                    f'Status : {name}  /\t Description : {description}  /\t Turns Remaining : {turns}'
                )

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
        """
        Attacks a target using one of its attacks
        """
        print(f"{self.name} attacks {target.name}!")
        n = random.randint(1, 100)
        if n > 30 and n < 60: #28% chance to use this attack
            print(f'{self.name} used Corrupt on {target.name}!')
            if accuracy(50, self, target) == True:   
                damage = 20
                if target.has_status('Infiltrated'):
                    damage = infiltrated(damage)
                target.take_damage(damage)
                print(f"{target.name} took {damage} damage!")
                target.add_status('Corrupted', 1)
                print(f"{target.name} is corrupted!")
            else:
                print('The attack missed!')
        if n > 15 and n < 31: #17% chance to use this attack
            print(f'{self.name} used Digital Infiltration on {target.name}!')
            if accuracy(30, self, target) == True:
                target.add_status('infiltrated', 1)
                print(f"{self.name} infiltrated {target.name}'s system!")
            else:
                print('The attack missed!')
        if n >= 2 and n < 16: #14% chance to use this attack
            print(f'{self.name} used System Overload on {target.name}!')
            if accuracy(40, self, target) == True:
                damage = 40
                if target.has_status('Infiltrated'):
                    damage = infiltrated(damage)
                target.take_damage(self.damage) 
                print(f"{target.name} took {damage} damage!")
            else:
                print('The attack missed!')
        if n >= 60: #40% chance to use this attack
            print(f'{self.name} used Pixel Blast on {target.name}!')
            if accuracy(70, self, target) == True:
                damage = 15
                if target.has_status('Infiltrated'):
                    damage = infiltrated(damage)
                target.take_damage(self.damage)
                print(f"{target.name} took {damage} damage!")
            else:
                print('The attack missed!')
        if n == 1:  #1% chance to use this attack
            print(f'{self.name} hit the Griddy!') 
            print(f'{target.name} was traumatised and stared in disgust.')
        print('\n')

    
