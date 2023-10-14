import random
import time

import characters
import data
import enemies
import text


ACTIONS = ["Attack", "Target", "Stats", "Item"]


class MUDGame:

    def __init__(self):
        # self.spawn = Room('home', up='closed')
        self.boss = enemies.Springtrap()
        self.current_room = data.start_room()
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

    def action_target(self) -> enemies.Enemy:
        """Select an enemy in the room to target."""
        enemy_list = self.current_room.grid.get_enemies()
        choice = text.prompt_valid_choice(
            enemy_list,
            prompt='Choose an enemy to target',
            errmsg='Enter a number corresponding to the surviving enemies.'
        )
        target = enemy_list[choice]
        return target

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

    def do_action(self, actor: characters.Character, target: "enemies.Enemy | None", action) -> "bool | enemies.Enemy":
        """Carry out the selected action by the actor on the target.
        Return True if successfully carried out, False otherwise.
        (e.g. if player cancels action)

        Special case: if a target is chosen,
        returns the target (to be deprecated in future)
        """
        assert target is not None
        if action == 'attack' or action == 0:
            skill = actor.prompt_attack()
            if skill == 'back':
                return False
            else:
                actor.attack(target, skill)
        elif action.lower() == 'target' or action == 1:
            # TODO: keep track of target
            target = self.action_target()
            return target
        elif action.lower() == 'check' or action == 2:
            return self.action_check(actor)
        elif action.lower() == 'item' or action == 3:
            return self.action_item(actor)
        else:
            print(
                f'Please select a valid action. Got {action}.')
        return False

    def run(self):
        data.start_menu()

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
        print('The game will begin.\n')
        while not self.gameOver:
            if not self.current_room.grid.is_encounter():
                #prompt movement
                self.current_room.display_room()
                move = self.current_room.grid.prompt_movement()
                while move not in ['w', 'a', 's', 'd', 'inventory']:
                    print(f"Type w, a, s or d or 'inventory'. Got {move}.\n")
                    move = self.current_room.grid.prompt_movement()
                #Opening inventory
                if move == 'inventory':
                    self.player1.display_inventory()
                    continue
                #entering next room
                if self.current_room.grid.get_position() == [
                        0, 2
                ] and move == 'w' and self.current_room.is_next_room(move):
                    self.current_room = self.current_room.next_room(move)
                    self.current_room.grid.move([4, 2])
                    continue
                elif self.current_room.grid.get_position() == [
                        2, 0
                ] and move == 'a' and self.current_room.is_next_room(move):
                    self.current_room = self.current_room.next_room(move)
                    self.current_room.grid.move([2, 4])
                    continue
                elif self.current_room.grid.get_position() == [
                        4, 2
                ] and move == 's' and self.current_room.is_next_room(move):
                    self.current_room = self.current_room.next_room(move)
                    self.current_room.grid.move([0, 2])
                    continue
                elif self.current_room.grid.get_position() == [
                        2, 4
                ] and move == 'd' and self.current_room.is_next_room(move):
                    self.current_room = self.current_room.next_room(move)
                    self.current_room.grid.move([2, 0])
                    continue
                #moving in current room
                if move == 'w' and self.current_room.grid.get_position(
                )[0] != 0:
                    current_position = self.current_room.grid.get_position()
                    current_position[0] = current_position[0] - 1
                    self.current_room.grid.move(current_position)
                elif move == 's' and self.current_room.grid.get_position(
                )[0] != 4:
                    current_position = self.current_room.grid.get_position()
                    current_position[0] = current_position[0] + 1
                    self.current_room.grid.move(current_position)
                elif move == 'a' and self.current_room.grid.get_position(
                )[1] != 0:
                    current_position = self.current_room.grid.get_position()
                    current_position[1] = current_position[1] - 1
                    self.current_room.grid.move(current_position)
                elif move == 'd' and self.current_room.grid.get_position(
                )[1] != 4:
                    current_position = self.current_room.grid.get_position()
                    current_position[1] = current_position[1] + 1
                    self.current_room.grid.move(current_position)
                #Picking up items
                if self.current_room.grid.is_item():
                    item = self.current_room.grid.get_item()
                    self.player1.add_item(item)
                    self.current_room.grid.clear_tile()
            #Combat Start
            elif self.current_room.grid.is_encounter():
                self.current_room.display_room()
                print('Battle started.\n')
                #Determine turn order
                player_list = [
                    self.player1, self.player2, self.player3, self.player4
                ]
                enemy_list = self.current_room.grid.get_enemies()
                copy_enemy_list = enemy_list.copy()
                turn_order = []
                i = 0
                while len(player_list) != 0 and len(copy_enemy_list) != 0:
                    if len(player_list) != 0:
                        if player_list[i] != None:
                            turn_order.append(player_list[i])
                            player_list.pop(i)
                    if len(copy_enemy_list) != 0:
                        turn_order.append(copy_enemy_list[i])
                        copy_enemy_list.pop(i)
                #Combat
                player_list = [
                    self.player1, self.player2, self.player3, self.player4
                ]
                player_list = [player for player in player_list if player != None]
                k = 0                        
                target = None
                while not characters.is_defeat(player_list) and not characters.is_victory(enemy_list):
                    active_character = turn_order[(k % len(turn_order))]
                    if active_character.has_status('Sleeping'):
                        print(f"{active_character.name} is asleep.")
                        k = (k + 1) % len(turn_order)
                        continue
                    active_character.display_turn()
                    if active_character in enemy_list:
                        time.sleep(1)
                        target = random.choice(player_list)
                        if active_character.has_status('Corrupted'):
                            target = random.choice(turn_order)
                        active_character.attack(target)
                        target = None
                    elif active_character in player_list:
                        action = text.prompt_valid_choice(
                            ACTIONS,
                            prompt='Please choose an action',
                            errmsg='Select a valid action.',
                            prelude='Select one of the following actions:'
                        )
                        if active_character.has_status('Corrupted'):
                            target = random.choice(turn_order)
                            active_character.attack(target, '1')
                            k = (k + 1) % len(turn_order)
                            continue

                        result = self.do_action(active_character, target, action)
                        if isinstance(result, enemies.Enemy):
                            target = result
                    #Remove defeated characters
                    for character in turn_order:
                        if character.is_defeated():
                            if k >= turn_order.index(character):
                                k = k - 1
                            print(f"{character.name} has died.")
                            turn_order.remove(character)
                            if character in enemy_list:
                                enemy_list.remove(character)
                            elif character in player_list:
                                player_list.remove(character)
                    #Reduce count of status effects
                    active_character.remove_status()
                    #Check if victory or defeat
                    if characters.is_defeat(player_list):
                        self.gameOver = True
                        print("Party defeated. Looks like you'll forgotten, just like the other animatronics down here who met their demise.")
                        break
                    elif characters.is_victory(enemy_list):
                        print('Encounter survived.')
                        self.current_room.grid.clear_tile()
                        break
                    #Next Turn
                    k = (k + 1) % len(turn_order)
            elif self.current_room.is_boss():
                #Boss Fight
                self.current_room.display_room()
                print('Battle started.\n')
                #Determine turn order
                player_list = [
                    self.player1, self.player2, self.player3, self.player4
                ]
                enemy_list = [self.boss]
                turn_order = []
                i = 0
                while len(player_list) != 0 and len(enemy_list) != 0:
                    if len(player_list) != 0:
                        if player_list[i] != None:
                            turn_order.append(player_list[i])
                            player_list.pop(i)
                    if len(enemy_list) != 0:
                        turn_order.append(enemy_list[i])
                        enemy_list.pop(i)
                #Combat
                player_list = [
                    self.player1, self.player2, self.player3, self.player4
                ]
                player_list = [player for player in player_list if player != None]
                enemy_list = [self.boss]
                k = 0                        
                target = None
                while not characters.is_defeat(player_list) and not characters.is_victory(
                        enemy_list):
                    active_character = turn_order[(k % len(turn_order))]
                    if active_character.has_status('Sleeping'):
                        print(f"{active_character.name} is asleep.")
                        k = (k + 1) % len(turn_order)
                        continue
                    active_character.display_turn()
                    if active_character in enemy_list:
                        time.sleep(1)
                        target = random.choice(player_list)
                        if active_character.has_status('Corrupted'):
                            target = random.choice(turn_order)
                        active_character.attack(target)
                        target = None
                    elif active_character in player_list:
                        action = text.prompt_valid_choice(
                                ACTIONS,
                                prompt='Please choose an action',
                                errmsg='Select a valid action.',
                                prelude='Select one of the following actions:'
                            )
                        if active_character.has_status('Corrupted'):
                            target = random.choice(turn_order)
                            active_character.attack(target, '1')
                            k = (k + 1) % len(turn_order)
                            continue
                        result = self.do_action(active_character, target, action)
                        if isinstance(result, enemies.Enemy):
                            target = result
                    #Remove defeated characters
                    for character in turn_order:
                        if character.is_defeated():
                            if k >= turn_order.index(character):
                                k = k - 1
                            print(f"{character.name} has died.")
                            turn_order.remove(character)
                            if character in enemy_list:
                                enemy_list.remove(character)
                            elif character in player_list:
                                player_list.remove(character)
                    #Reduce count of status effects
                    active_character.remove_status()
                    #Check if victory or defeat
                    if characters.is_defeat(player_list):
                        self.gameOver = True
                        print("Party defeated. Looks like you'll forgotten, just like the other animatronics down here who met their demise.")
                        break
                    elif characters.is_victory(
                            enemy_list) and self.boss.name == 'Springtrap':
                        #Initiate phase 2
                        self.boss = enemies.Glitchtrap()
                        self.boss.spawn()
                        enemy_list = [self.boss]
                        turn_order.insert(1, enemy_list[0])
                        k = 0
                        continue
                    elif characters.is_victory(
                            enemy_list) and self.boss.name == 'Glitchtrap':
                        self.gameOver = True
                        data.Ending()
                        break
                    k = (k + 1) % len(turn_order)
