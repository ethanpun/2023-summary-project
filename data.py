import json
import random
import time

import text
from enemies import BB, GB, Enemy, Springtrap


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


def opp(direction: str) -> str:
    """Return the opposite direction character"""
    if direction == 'w':
        return 's'
    elif direction == 's':
        return 'w'
    elif direction == 'a':
        return 'd'
    elif direction == 'd':
        return 'a'
    raise ValueError("Invalid direction {direction!r}")


class Room:
    def __init__(self,
                 boss=None,
                 x=2,
                 y=2,
                 number=0):
        self.boss = boss
        self.number = number
        self._paths: dict[str, "Room | None"] = {
            'w': None,
            'a': None,
            's': None,
            'd': None
        }
        self.grid = Grid(x=x, y=y)
        if not boss:
            populate_enemy(self.grid, 5)
            populate_item(self.grid, 5)
        
    def display_room(self):
        print(f"Room {self.number}")

    def link(self, direction: str, room: "Room") -> None:
        assert direction in self._paths
        assert isinstance(room, Room)
        if self._paths[direction] is room:
            # Already connected
            return
        self._paths[direction] = room
        if room._paths[opp(direction)] is None:
            room.link(opp(direction), self)

    def next_room(self, next: str) -> 'Room | None':
        """User moves to next room. Depending on the input, move to room above, below,
        left or right.
        """
        assert next.islower()
        assert next in self._paths
        return self._paths[next]
        
    def is_boss(self):
        if self.boss:
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


def random_coord(n: int) -> tuple[int, int]:
    x = random.randint(0, n)
    y = random.randint(0, n)
    return x, y

def populate_item(grid: "Grid", n: int) -> None:
    """Populate the grid with items randomly, n times"""
    if n == 0:
        return
    x, y = random_coord(4)
    while not grid.get_tile(x, y).is_empty():
        x, y = random_coord(4)
    random_item = random.choice(all_items)
    grid.get_tile(x, y).set_item(random_item)
    populate_item(grid, n - 1)

def populate_enemy(grid: "Grid", n: int) -> None:
    """Populate the grid with enemies randomly, n times"""
    if n == 0:
        return
    x, y = random_coord(4)
    while not grid.get_tile(x, y).is_empty():
        x, y = random_coord(4)
    Enemy_ = random.choice([GB, BB])
    grid.get_tile(x, y).add_enemy(Enemy_())
    populate_enemy(grid, n - 1)


class Grid:
    def __init__(self, x, y):
        self.grid = [
            [
                Tile()
                for _ in range(5)
            ]
            for _ in range(5)
        ]

    def get_tile(self, x: int, y: int):
        assert 0 <= x < 5
        assert 0 <= y < 5
        return self.grid[x][y]

    def spawn(self, x: int, y: int, thing: "Enemy | Item") -> None:
        if isinstance(thing, Item):
            self.get_tile(x, y).set_item(thing)
        elif isinstance(thing, Enemy):
            self.get_tile(x, y).add_enemy(thing)

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

    def is_edge(self, coord: tuple[int, int], direction: str) -> bool:
        """Returns True if the coord is at the edge of the
        grid in the given direction, False otherwise.
        """
        x, y = coord
        if direction == 'w':
            return x > 0
        if direction == 'a':
            return y > 0
        if direction == 's':
            return x < 4
        if direction == 'd':
            return y < 4
        raise AssertionError  # invalid direction
    
    def is_exit(self, coord: tuple[int, int], direction: str) -> bool:
        """Returns True if the coord is at the edge of the
        grid in the given direction, False otherwise.
        """
        if direction == 'w':
            return coord == (0, 2)
        if direction == 'a':
            return coord == (2, 0)
        if direction == 's':
            return coord == (4, 2)
        if direction == 'd':
            return coord == (2, 4)
        raise AssertionError  # invalid direction

    def is_encounter(self, coord: tuple[int, int]) -> bool:
        """Return true if user coordinates are currently on a creature tile."""
        x, y = coord
        return bool(self.get_tile(x, y).enemies)

    def get_enemies(self, coord: tuple[int, int]):
        """Return the enemies on that tile."""
        x, y = coord
        return self.get_tile(x, y).enemies

    def is_item(self, coord: tuple[int, int]):
        """Return true if user coordinates are currently on a item tile."""
        x, y = coord
        return bool(self.get_tile(x, y).item)
            
    def get_item(self, coord: tuple[int, int]) -> Item:
        """If user is on an item tile, return the item on that tile"""
        x, y = coord
        item = self.get_tile(x, y).item
        assert item is not None
        return item
        
    def clear_tile(self, coord: tuple[int, int]):
        """After a defeating a creature or picking up an item, remove it from the grid"""
        x, y = coord
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

