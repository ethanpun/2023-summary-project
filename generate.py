import random

from data import Room
from enemies import Boss, Springtrap


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


def maze() -> Room:
    generator = MazeGenerator()
    start_room = generator.start_room()
    generator.generate(start_room)
    return start_room


class MazeGenerator:
    """Encapsulates data necessary for generating a set of
    connected rooms.

    Attributes:
    - total_rooms: int

    Methods:
    + start_room() -> Room
      returns the starting room of the maze
    + generate(room, n: int) -> None
      Generate the maze, starting from the given room
    """
    def __init__(self) -> None:
        self.total_rooms = 0
        start_room = Room(number=self.total_rooms)
        self._start_room = start_room

    def add_room(self, room: Room, direction: str, boss: "Boss | None" = None) -> Room:
        """Add a new room to the given room
        in the given direction.
        Return the new room.
        """
        assert direction in 'wasd'
        self.total_rooms += 1
        next_room = Room(number=self.total_rooms, boss=boss)
        room.link(direction, next_room)
        return next_room

    def start_room(self) -> Room:
        """Returns the entrance (start room)"""
        return self._start_room

    def generate(self, room: Room, n: int = 2, depth=0) -> None:
        """Add n rooms to room, recursively"""
        if room is self.start_room():
            # First room only has one direction, w
            next_room = self.add_room(room, 'w')
            self.generate(
                next_room,
                n=random.randint(2, 3),
                depth=depth + 1
            )
        elif self.total_rooms < 10 and depth < 3:
            # Normal Room
            for _ in range(n):
                # List of directions without a linked room
                unlinked_dirs = [dir_ for dir_, room in room._paths.items() if room is None]
                direction = random.choice(unlinked_dirs)
                # TODO: populate boss separately
                if room.number == 7:
                    next_room = self.add_room(room, direction, boss=Springtrap())
                else:
                    next_room = self.add_room(room, direction)
                self.generate(
                    next_room,
                    n=random.randint(2, 3),
                    depth=depth + 1
                )