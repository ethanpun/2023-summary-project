import random
import data


def accuracy_calc(light: int) -> bool:
    temp = [True] * light + [False] * (100 - light)
    return temp[random.randint(0, len(temp) - 100)]


def defeat(players: list) -> bool:
    for player in players:
        if not player.is_defeated():
            return False
    return True


def victory(enemies: list) -> bool:
    for enemy in enemies:
        if not enemy.is_defeated():
            return False
    return True


class MUDGame:
    def __init__(self):
        # self.spawn = Room('home', up='closed')
        self.boss = data.Springtrap.encounter()
        self.current_room = data.start_room()
        self.gameOver = False
        self.player1 = None
        self.player2 = None
        self.player3 = None
        self.player4 = None

    
    def set_player(self, player, character):
        if player == 'self.player1':
            self.player1 = character
        elif player == 'self.player2':
            self.player2 = character
        elif player == 'self.player3':
            self.player3 = character
        elif player == 'self.player4':
            self.player4 = character

    def run(self):
        data.start_menu()
        for player in [
                'self.player1', 'self.player2', 'self.player3', 'self.player4'
        ]:
            valid = False
            while not valid:
                character = data.choose_character()
                if character != None:
                    valid = True
            if character.lower() == 'freddy':
                self.set_player(player, data.Freddy())
            elif character.lower() == 'bonnie':
                self.set_player(player, data.Bonnie())
            elif character.lower() == 'chica':
                self.set_player(player, data.Chica())
            elif character.lower() == 'foxy':
                self.set_player(player, data.Foxy())
            elif character.lower() == 'skip':
                break
        while not self.gameOver:
            if not self.current_room.grid.is_encounter():
                #prompt movement
                self.current_room.display_room()
                input = self.current_room.grid.prompt_movement()
                while input.lower() not in 'wasd' or input.lower(
                ) != 'inventory':
                    input = self.current_room.grid.prompt_movement()
                #Opening inventory
                if input.lower() == 'inventory':
                    data.display_inventory()
                    continue
                #entering next room
                if self.current_room.grid.get_position() == [0, 2] and input == 'w':
                    self.current_room.next_room(input)
                    self.current_room.grid.move([4, 2])
                    continue
                elif self.current_room.grid.get_position() == [2, 0] and input == 'a':
                    self.current_room.next_room(input)
                    self.current_room.grid.move([2, 4])
                    continue
                elif self.current_room.grid.get_position() == [4, 2] and input == 's':
                    self.current_room.next_room(input)
                    self.current_room.grid.move([0, 2])
                    continue
                elif self.current_room.grid.get_position() == [2, 4] and input == 'd':
                    self.current_room.nextRoom(input)
                    self.current_room.grid.move([2, 0])
                    continue
                #moving in current room
                if input.lower() == 'w' and self.current_room.grid.get_position()[0] != 0:
                    current_position = self.current_room.grid.get_position()
                    current_position[1] = current_position[1] + 1
                    self.current_room.grid.move(current_position)
                elif input.lower() == 's' and self.current_room.grid.get_position()[0] != 4:
                    current_position = self.current_room.grid.get_position()
                    current_position[1] = current_position[1] - 1
                    self.current_room.grid.move(current_position)
                elif input.lower() == 'a' and self.current_room.grid.get_position()[1] != 0:
                    current_position = self.current_room.grid.get_position()
                    current_position[0] = current_position[0] - 1
                    self.current_room.grid.move(current_position)
                elif input.lower() == 'd' and self.current_room.grid.get_position()[1] != 4:
                    current_position = self.current_room.grid.get_position()
                    current_position[0] = current_position[0] + 1
                    self.current_room.grid.move(current_position)
                #Picking up items
                if self.current_room.grid.is_item():
                    items = self.current_room.grid.get_items()
                    data.add_item(items)
            #Combat Start
            elif self.current_room.grid.is_encounter():
                #Determine turn order
                player_list = [
                    self.player1, self.player2, self.player3, self.player4
                ]
                enemy_list = self.current_room.grid.get_enemies()
                turn_order = []
                i = 0
                while len(player_list) != 0 and len(enemy_list) != 0:
                    if player_list[i] != None:
                        turn_order.append(player_list[i])
                    else:
                        player_list.pop(i)
                    turn_order.append(enemy_list[i])
                    i += 1
                #Combat
                k = 0
                while not defeat(player_list) and not victory(enemy_list):
                    active_character = turn_order[k % (len(turn_order) - 1)]
                    active_character.display_turn()
                    if active_character in enemy_list:
                        target = random.choice(player_list)
                        skill = random.randint(1, 2)
                        hit = accuracy_calc(player_list[0].get_light())
                        if hit:
                            damage = active_character.attack(target, skill)
                            statuses = active_character.inflict_status(
                                target, skill)
                            heal = active_character.heal(
                                active_character, skill)
                            if damage != None:
                                player_list[target].take_dmg(damage)
                            if statuses != None:
                                player_list[target].set_status(statuses)
                            if heal != None:
                                active_character.receive_heal(heal)
                        else:
                            active_character.display_miss()
                    elif active_character in player_list:
                        target = None
                        action = active_character.prompt_action()
                        if action == 'attack':
                            skill = active_character.prompt_attack()
                            hit = accuracy_calc(active_character.get_light())
                            if hit:
                                damage = active_character.attack(
                                    enemy_list[target], skill)
                                statuses = active_character.inflict_status(
                                    enemy_list[target], skill)
                                heal = active_character.heal(
                                    active_character, skill)
                                if damage != None:
                                    enemy_list[target].take_dmg(damage)
                                if statuses != None:
                                    enemy_list[target].set_status(statuses)
                                if heal != None:
                                    active_character.receive_heal(heal)
                            else:
                                active_character.display_miss()
                        elif action.lower() == 'target':
                            target = active_character.target() - 1
                            continue
                        elif action.lower() == 'stats':
                            active_character.get_stats()
                            continue
                        elif action.lower() == 'light':
                            valid = False
                            while not valid:
                                input = active_character.prompt_light()
                                if input in ['back', 'increase', 'decrease']:
                                    valid = True
                            if input == 'increase':
                                active_character.increase_light(10)
                            elif input.lower() == 'decrease':
                                active_character.decrease_light(10)
                            elif input.lower() == 'back':
                                continue
                        elif action.lower() == 'item':
                            continue
                            #Remove defeated characters
                    for character in turn_order:
                        if character.is_defeated():
                            turn_order.remove(character)
                        if character in enemy_list:
                            enemy_list.remove(character)
                        elif character in player_list:
                            player_list.remove(character)
                    k = k + 1
                if defeat(player_list):
                    self.gameOver = True
                    #Defeat message
                elif victory(enemy_list):
                    #Victory message
                    self.current_room.grid.clear_tile()
                    break
            #Code boss fight here
