import json
import random
import time

from enemies import BB, GB, Enemy, Springtrap
import text

class Item:
    """Encapsulates items in the game."""
    def __init__(self,
                 name: str,
                 description: str,
                 effect: str,
                 consumable: bool,
                 type: "str | None" = None,
                 heal: "int | None" = None,
                 damage: "int | None" = None) -> None:
        self.name = name
        self.description = description
        self.effect = effect
        self.consumable = consumable
        self.type = type
        self.heal = heal
        self.damage = damage

    def __repr__(self) -> str:
        return ("Item("
                f"name={self.name}, "
                f"description={self.description}, "
                f"effect={self.effect}, "
                f"consumable={self.consumable}, "
                f"type={self.type}, "
                f"heal={self.heal}, "
                f"damage={self.damage})")

    def report(self) -> str:
        """Return a simple item report.
        Primarily for use in inventory display.
        """
        return (
            f'Item : {self.name}  /'
            f'\t Description : {self.description}  /'
            f'\t Effect : {self.effect}  /'
        f'\t Consumable : {self.consumable}'
        )
        

#Inventory and Items
all_items = []
with open("items.json", "r") as f:
    for record in json.load(f):
        all_items.append(Item(**record))


class Inventory:
    """Class with methods for managing inventory.

    Methods:
    items() -> tuple[Item]
    add_item(item) -> bool
    remove_item(item) -> bool
    """
    def __init__(self) -> None:
        self._data: list[Item] = []

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def items(self) -> tuple["Item", ...]:
        """Returns a tuple of all items in the inventory."""
        return tuple(self._data)

    def add_item(self, item: "Item") -> bool:
        """Add an item to inventory.
        Return True if successful, False otherwise.
        """
        assert isinstance(item, Item)
        self._data.append(item)
        return True

    def remove_item(self, item: "Item") -> bool:
        """Remove an item from inventory.
        Return True if successful, False otherwise.
        """
        assert isinstance(item, Item)
        if item not in self._data:
            return False
        self._data.remove(item)
        return True


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
            if next_rooms[i] is not None:
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
        """User moves to next room. Depending on the input, move to room above, below, left or right. Also, check if next room for given input exists.
        """
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
        """
        Returns the current room
        """
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
        """
        Return the boss.
        """
        return self.boss


class Tile:
    def __init__(self):
        self.item: "Item | None" = None
        self.enemies: list[Enemy] = []

    def __repr__(self) -> str:
        return f"Tile(item={self.item}, enemies={self.enemies})"

    def is_empty(self) -> bool:
        return not (self.item or self.enemies)

    def set_item(self, item: Item) -> None:
        assert isinstance(item, Item)
        self.item = item

    def add_enemy(self, enemy: Enemy) -> None:
        assert isinstance(enemy, Enemy)
        self.enemies.append(enemy)

    def clear_all(self) -> None:
        self.item = None
        self.enemies.clear()


class Grid:
    def __init__(self, type, x, y):
        self.type = type
        self.grid = [
            [
                Tile()
                for _ in range(5)
            ]
            for _ in range(5)
        ]
        if type == 'normal':
        #Spawning creatures
            i = 0
            while i < 5:
                x = random.randint(0, 4)
                y = random.randint(0, 4)
                if self.get_tile(x, y).is_empty():
                    enemy_count = random.randint(1, 3)
                    for _ in range(enemy_count):
                        Enemy_ = random.choice([GB, BB])
                        self.get_tile(x, y).add_enemy(Enemy_())
                    i = i + 1
            k = 0
        #Spawning items
            while k < 5:
                x = random.randint(0, 4)
                y = random.randint(0, 4)
                if self.get_tile(x, y).is_empty():
                    random_item = random.choice(all_items)
                    self.get_tile(x, y).set_item(random_item)
                    k = k + 1
        self.coordinates = [x, y]

    def get_tile(self, x: int, y: int):
        assert 0 <= x < 5
        assert 0 <= y < 5
        return self.grid[x][y]
        
    def get_position(self) -> list:
        """Return user position"""
        return self.coordinates

    def prompt_movement(self) -> str:
        """Prompt the user for a movement and return the direction to move.
        Also, to view inventory, user types open inventory
        """
        options = ['w', 'a', 's', 'd', 'inventory']
        index = text.prompt_valid_choice(
            options=options,
            inline=True,
            cancel=False,
            prelude="Type 'wasd' to move, open the inventory by typing 'inventory'",
            prompt="Type an action"
        )
        # print('--------------------------------------------------------')
        assert index is not None
        return options[index]
        
    def move(self, position : list):
        """Update user position and coordinates in the room"""
        self.coordinates = position
    
    def is_encounter(self) -> bool:
        """Return true if user coordinates are currently on a creature tile."""
        x, y = self.get_position()
        return bool(self.get_tile(x, y).enemies)

    def get_enemies(self):
        """Return the enemies on that tile."""
        x, y = self.get_position()
        return self.get_tile(x, y).enemies

    def is_item(self):
        """Return true if user coordinates are currently on a item tile."""
        x, y = self.get_position()
        return bool(self.get_tile(x, y).item)
            
    def get_item(self) -> Item:
        """If user is on an item tile, return the item on that tile"""
        x, y = self.get_position()
        item = self.get_tile(x, y).item
        assert item is not None
        return item
        
    def clear_tile(self):
        """After a defeating a creature or picking up an item, remove it from the grid"""
        x, y = self.get_position()
        self.get_tile(x, y).clear_all()


with open("characters.json", "r") as f:
    char_info = json.load(f)


def info(name: str):
    """Displays information of the playable characters"""
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
    """Prompts the user to select a character to play as"""
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
    """Plays the end sequence after Glitchtrap is defeated"""
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

