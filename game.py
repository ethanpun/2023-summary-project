from itertools import zip_longest
import random
import time

import characters
from combat import Party
import data
import enemies
import generate
import text


ACTIONS = ["Attack", "Stats", "Item"]


class MUDGame:

    def __init__(self):
        # self.spawn = Room('home', up='closed')
        self.boss = enemies.Springtrap()
        self.current_room: data.Room = generate.maze()
        self.gameOver = False
        self.player1 = None
        self.player2 = None
        self.player3 = None
        self.player4 = None

    def set_player(self, player, character):
        if player == 'Player 1':
            self.player1 = character
        elif player == 'Player 2':
            self.player2 = character
        elif player == 'Player 3':
            self.player3 = character
        elif player == 'Player 4':
            self.player4 = character

    def action_check(self, actor: characters.Character) -> bool:
        """Prompt player for stats to check, and display requested stats"""
        check = actor.prompt_check()
        if check == 'back':
            return False
        elif check == 'enemy':
            enemy_list = self.current_room.grid.get_enemies()
            for enemy in enemy_list:
                enemy.get_stats()
        elif check == 'party':
            player_list = [
                player
                for player in (self.player1, self.player2, self.player3, self.player4)
                if player is not None
            ]
            for ally in player_list:
                ally.get_stats()
        return True

    def action_combat(self) -> None:
        """Initiate combat in current room"""
        self.current_room.display_room()
        print('Battle started.\n')
        #Determine turn order
        player_party = Party(
            [player
            for player in (self.player1, self.player2, self.player3, self.player4)
            if player is not None]
        )
        if self.current_room.is_boss():
            enemy_party = Party([self.boss])
            self.boss.encounter()
        else:
            enemy_party = Party(self.current_room.grid.get_enemies())
        turn_order = []
        for player, enemy in zip_longest(player_party.members(), enemy_party.members()):
            if player:
                 turn_order.append(player)
            if enemy:
                 turn_order.append(enemy)

        # Combat
        k = 0                        
        target = None
        while not (player_party.is_defeated() or enemy_party.is_defeated()):
            active_character = turn_order[(k % len(turn_order))]
            if active_character.is_defeated():
                k = (k + 1) % len(turn_order)
                continue
            if active_character.has_status('Sleeping'):
                print(f"{active_character.name} is asleep.")
                k = (k + 1) % len(turn_order)
                continue
            if active_character.has_status('Corrupted'):
                target = random.choice(turn_order)
                attack = active_character.get_attack()
                active_character.attack(target, attack)
                continue
            active_character.display_turn()
            if isinstance(active_character, enemies.Enemy):
                target = active_character.select_target(player_party.members())
                attack = active_character.get_attack()
                active_character.attack(target, attack)
            elif isinstance(active_character, characters.Character):
                choice = text.prompt_valid_choice(
                    ACTIONS,
                    prompt='Please choose an action',
                    errmsg='Select a valid action.',
                    prelude='Select one of the following actions:'
                )
                assert choice is not None
                action = ACTIONS[choice].lower()
                self.do_action(active_character, enemy_party, action)
            if active_character.is_defeated():
                print(f"{active_character.name} has died.")
            # Update character state
            else:
                active_character.update()
            # Upgrade boss if defeated
            for enemy in enemy_party.members():
                if isinstance(enemy, enemies.Boss) and enemy.is_defeated() and enemy.next_phase:
                    enemy_party.remove(enemy.name)
                    enemy_party.append(enemy.next_phase(enemy.name, enemy.health, enemy.attacks))
                    enemy.encounter()
            # Check if victory or defeat
            if player_party.is_defeated():
                self.gameOver = True
                print("Party defeated. Looks like you'll forgotten, just like the other animatronics down here who met their demise.")
                break
            elif enemy_party.is_defeated():
                print('Encounter survived.')
                self.current_room.grid.clear_tile()
                break
            # Next Turn
            k = (k + 1) % len(turn_order)

    def action_inventory(self) -> None:
        """Display common inventory"""
        assert self.player1 is not None
        self.player1.display_inventory()

    def action_item(self, actor: characters.Character) -> bool:
        """Prompt player for an item to use, and use it"""
        is_use = actor.is_use_item()
        if is_use == 'n':
            return False
        # Assume yes
        items = [
            item.report()
            for item in actor.inventory.items()
        ]
        choice = text.prompt_valid_choice(
            items,
            cancel=True,
            prompt="Choose an item to use",
            errmsg="Invalid item",
            prelude="Inventory:",
        )
        if not choice:
            return False
        item = items[choice]
        print('')
        used = actor.use_item(item)
        if not used:
            return False
        return True

    def action_move(self, move: str) -> bool:
        """Carry out the move in the given direction.
        Return True if entering next room, else False.
        """
        # entering next room
        if self.current_room.grid.get_position() == [
                0, 2
        ] and move == 'w' and self.current_room.next_room(move):
            self.current_room = self.current_room.next_room(move)
            self.current_room.grid.move([4, 2])
            next_room = True
        elif self.current_room.grid.get_position() == [
                2, 0
        ] and move == 'a' and self.current_room.next_room(move):
            self.current_room = self.current_room.next_room(move)
            self.current_room.grid.move([2, 4])
            next_room = True
        elif self.current_room.grid.get_position() == [
                4, 2
        ] and move == 's' and self.current_room.next_room(move):
            self.current_room = self.current_room.next_room(move)
            self.current_room.grid.move([0, 2])
            next_room = True
        elif self.current_room.grid.get_position() == [
                2, 4
        ] and move == 'd' and self.current_room.next_room(move):
            self.current_room = self.current_room.next_room(move)
            self.current_room.grid.move([2, 0])
            next_room = True

        # moving in current room
        elif move == 'w' and self.current_room.grid.get_position(
        )[0] != 0:
            current_position = self.current_room.grid.get_position()
            current_position[0] = current_position[0] - 1
            self.current_room.grid.move(current_position)
            next_room = False
        elif move == 's' and self.current_room.grid.get_position(
        )[0] != 4:
            current_position = self.current_room.grid.get_position()
            current_position[0] = current_position[0] + 1
            self.current_room.grid.move(current_position)
            next_room = False
        elif move == 'a' and self.current_room.grid.get_position(
        )[1] != 0:
            current_position = self.current_room.grid.get_position()
            current_position[1] = current_position[1] - 1
            self.current_room.grid.move(current_position)
            next_room = False
        elif move == 'd' and self.current_room.grid.get_position(
        )[1] != 4:
            current_position = self.current_room.grid.get_position()
            current_position[1] = current_position[1] + 1
            self.current_room.grid.move(current_position)
            next_room = False
        else:
            # unreachable; throw AssertionError if reached
            raise AssertionError
        return next_room

    def action_pickup(self) -> None:
        """Pick up items in current room"""
        if self.current_room.grid.is_item():
            item = self.current_room.grid.get_item()
            self.player1.add_item(item)
            self.current_room.grid.clear_tile()

    def do_action(self, actor: characters.Character, enemy_party, action) -> bool:
        """Carry out the selected action by the actor on the target.
        Return True if successfully carried out, False otherwise.
        (e.g. if player cancels action)
        """
        if action == 'attack':
            attack = actor.select_attack()
            if attack == 'back':
                return False
            target = actor.select_target(enemy_party)
            assert not isinstance(attack, str)
            actor.attack(target, attack)
        elif action == 'check':
            return self.action_check(actor)
        elif action.lower() == 'item':
            return self.action_item(actor)
        else:
            print(
                f'Please select a valid action. Got {action}.')
        return False

    def setup(self) -> None:
        common_inventory = data.Inventory()

        for player in ['Player 1', 'Player 2', 'Player 3', 'Player 4']:
            character = data.choose_character(player)
            valid_character_list = ['freddy', 'freddy fazbear', 'chica', 'bonnie', 'foxy', 'skip']
            if player == 'Player 1':
                valid_character_list.remove('skip')
            while character not in valid_character_list:
                print(
                    f"Please select a valid animatronic or finish party by entering 'skip'. Got {character}.\n"
                )
                character = data.choose_character(player)
            if character == 'freddy' or character == 'freddy fazbear':
                self.set_player(player, characters.Freddy(health=100, inventory=common_inventory))
            elif character == 'bonnie':
                self.set_player(player, characters.Bonnie(health=100, inventory=common_inventory))
            elif character == 'chica':
                self.set_player(player, characters.Chica(health=100, inventory=common_inventory))
            elif character == 'foxy':
                self.set_player(player, characters.Foxy(health=100, inventory=common_inventory))
            elif character == 'skip':
                break

    def run(self) -> None:
        print('The game will begin.\n')
        while not self.gameOver:
            if not self.current_room.grid.is_encounter():
                # Prompt movement
                self.current_room.display_room()
                move = self.current_room.grid.prompt_movement()
                if move == 'inventory':
                    # Opening inventory
                    self.action_inventory()
                else:
                    self.action_move(move)
                    # Picking up items
                    self.action_pickup()
    
            # Combat Start
            else:
                self.action_combat()
