#test
# from main import game
import time
import data
import game

# test = game.MUDGame()

    
    # try:
    #     data.start_menu()
    # except:
    #     print("Start Menu is screwed")
    # else:
    #     print("Start Menu is fine")

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





'''
========================================
Test the start_room function for errors.
========================================
'''

try:
    test_spawn_room = data.start_room()
    if test_spawn_room.__class__.__name__ == "Room":
        print("Spawn Room is a Room Object")
    else:
        raise Exception("Spawn Room created is not a Room Object")
except:
    raise Exception("Spawn Room function does not run.")
else:
    print("Spawn Room instantiated with no issues.")



'''
========================
Test the attack (Freddy)
========================
'''

HEALTH = 500
test_freddy = data.Freddy()
test_BB = data.BB(health = HEALTH)
        
while test_BB.is_defeated() == False:
    test_freddy.attack(test_BB, "1")
    print(f'test_BB health is now {test_BB.health}')
print("""
Freddy attack 1 passed
""")
time.sleep(2)
test_BB.health = HEALTH

while not test_BB.has_status("Sleeping"):
    test_freddy.attack(test_BB, "2")
    test_BB.get_stats()
while test_BB.has_status("Sleeping"):
    test_BB.remove_status()
print("""
Freddy attack 2 (status move) passed
""")
time.sleep(2)

while test_BB.is_defeated() == False:
    test_freddy.attack(test_BB, "3")
    print(f'test_BB health is now {test_BB.health}')
print("""
Freddy attack 3 passed
""")
time.sleep(2)
test_BB.health = HEALTH


'''
========================
Test the attack (Bonnie)
========================
'''

HEALTH = 500
test_bonnie = data.Bonnie()
test_BB = data.BB(health = HEALTH)
        
while test_BB.is_defeated() == False:
    test_bonnie.attack(test_BB, "1")
    print(f'test_BB health is now {test_BB.health}')
    
print("""
Bonnie attack 1 passed
""")
time.sleep(2)
test_BB.health = HEALTH

while not test_BB.has_status("Resonance"):
    test_bonnie.attack(test_BB, "2")
    test_BB.health = HEALTH
    test_BB.get_stats()

while test_BB.has_status("Resonance"):
    test_BB.remove_status()
print("""
Bonnie attack 2 (status move) passed
""")
time.sleep(2)

while test_BB.is_defeated() == False:
    test_bonnie.attack(test_BB, "3")
    print(f'test_BB health is now {test_BB.health}')
    
print("""
Bonnie attack 3 passed
""")
time.sleep(2)
test_BB.health = HEALTH





