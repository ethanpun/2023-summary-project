#test
# from main import game
import time

import characters
import data
import enemies
import game
import generate

# test = game.MUDGame()

    
    # try:
    #     data.start_menu()
    # except:
    #     print("Start Menu is screwed")
    # else:
    #     print("Start Menu is fine")

def test_room():
    '''
    ===============================================
    Test the Normal Room and Grid class for errors.
    ===============================================
    '''
    try:
        test_grid = data.Grid("normal", 2, 2)
    except:
        print("Grid cannot be instantiated")
    try:
        test_room = data.Room()
    except:
        print("Room cannot be instantiated")
        raise
        
    try:
        if test_room.grid.get_position() != [2, 2]:
            print("Grid positioning does not work properly.")
        else:
            print("Grid position is ok.")
        
    except:
        print("Grid cannot instantiate (the function does not work).")
    test_room.grid.move([0,0])
    
    for x in range(0, 5):
        for y in range(0, 5):
            pos = [x, y]
            print(pos)
            try:
                if test_room.grid.is_encounter():
                    print(test_room.grid.get_enemies())
            except:
                print("is_encounter() does not work")
            test_room.grid.move(pos)
    
    print("Room and Grid instantiated with no issues.")
    

def test_start_room():
    '''
    ========================================
    Test the start_room function for errors.
    ========================================
    '''
    
    try:
        test_spawn_room = generate.maze()
        if test_spawn_room.__class__.__name__ == "Room":
            print("Spawn Room is a Room Object")
        else:
            raise Exception("Spawn Room created is not a Room Object")
    except:
        raise Exception("Spawn Room function does not run.")
    else:
        print("Spawn Room instantiated with no issues.")


visited = []
def test_room_connections(room=None) -> None:
    '''
    ========================================
    Test that rooms are consistently connected.
    ========================================
    '''
    def opp(direction: str) -> str:
        if direction == 'w': return 's'
        if direction == 's': return 'w'
        if direction == 'a': return 'd'
        if direction == 'd': return 'a'
    
    if not room:
        room = generate.maze()
    if room in visited:
        return
    for direction in 'wasd':
        next_room = room.next_room(direction)
        if not next_room:
            continue
        # room exists
        assert next_room.next_room(opp(direction)) is room
        visited.append(room)
        test_room_connections(next_room)
    

def test_freddy():
    '''
    ========================
    Test the attack (Freddy)
    ========================
    '''
    
    HEALTH = 500
    common_inventory = data.Inventory()
    test_freddy = characters.Freddy(health=100, inventory=common_inventory)
    test_BB = enemies.BB(health = HEALTH)
            
    while not test_BB.is_defeated():
        test_freddy.attack(test_BB, test_freddy.get_attack("Mic Toss"))
        print(f'test_BB health is now {test_BB.health}')
    print("Freddy attack 1 passed")
    time.sleep(2)
    test_BB.health = HEALTH
    
    while not test_BB.has_status("Sleeping"):
        test_freddy.attack(test_BB, test_freddy.get_attack("Sing"))
        test_BB.get_stats()
    while test_BB.has_status("Sleeping"):
        test_BB.update()
    print("Freddy attack 2 (status move) passed")
    time.sleep(2)
    
    while not test_BB.is_defeated():
        test_freddy.attack(test_BB, test_freddy.get_attack("The Bite"))
        print(f'test_BB health is now {test_BB.health}')
    print("Freddy attack 3 passed")
    time.sleep(2)
    test_BB.health = HEALTH
    

def test_bonnie():
    '''
    ========================
    Test the attack (Bonnie)
    ========================
    '''
    
    HEALTH = 500
    common_inventory = data.Inventory()
    test_bonnie = characters.Bonnie(health=100, inventory=common_inventory)
    test_BB = enemies.BB(health = HEALTH)
            
    while not test_BB.is_defeated():
        test_bonnie.attack(test_BB, test_bonnie.get_attack("Rift"))
        print(f'test_BB health is now {test_BB.health}')
        
    print("Bonnie attack 1 passed")
    time.sleep(2)
    test_BB.health = HEALTH
    
    while not test_BB.has_status("Resonance"):
        test_bonnie.attack(test_BB, test_bonnie.get_attack("Guitar Crash"))
        test_BB.health = HEALTH
        test_BB.get_stats()
    
    while test_BB.has_status("Resonance"):
        test_BB.update()
    print("Bonnie attack 2 (status move) passed")
    time.sleep(2)
    
    while not test_BB.is_defeated():
        test_bonnie.attack(test_BB, test_bonnie.get_attack("Rock 'n' Roll"))
        print(f'test_BB health is now {test_BB.health}')
        
    print("Bonnie attack 3 passed")
    time.sleep(2)
    test_BB.health = HEALTH
    




test_room()
test_start_room()
test_room_connections()
# test_freddy()
# test_bonnie()
