import random
import time

#Rooms
class Room:
    def __init__(self, x = 2, y = 2, up = None, down = None, left = None, right = None, number = 0):
        #next rooms
        self.up = up
        self.down = down 
        self.right = right
        self.left = left
        self.count = number
        connections = random.randint(1, 3)
        next_rooms = [self.up, self.down, self.left, self.right]
        for room in next_rooms:
            if room != None:
                next_rooms.remove(room)
        while connections != 0:
            next_room = random.randint(0, len(next_rooms) - 1)
            next_rooms[next_room] = 'closed'
            next_rooms.pop(next_room)
            connections = connections - 1
         
        self.grid = Grid(x, y)
        
    def display_room(self):
        pass

    def is_next_room(self, next : str) -> bool:
        if next.lower() == 'w':
            if self.up == None:
                return False
            return True
        elif next.lower() == 'a':
            if self.left == None:
                return False
            return True
        elif next.lower() == 's':
            if self.down == None:
                return False
            return True
        elif next.lower() == 'd':
            if self.right == None:
                return False
            return True

    def next_room(self, next : str) -> None:
        '''
        User moves to next room. Depending on the input, move to room above, below, left or right. Also, check if next room for given input exists.
        '''
        if next.lower() == 'w':
            if self.up == None:
                print('It seems that this door is locked.')
            else:
                prev = self
                self.up = Room(up = prev, number=self.countRoom())
                self = self.up
        if next.lower() == 's':
            if self.down == None:
                print('It seems that this door is locked.')
            else:
                prev = self
                self.down = Room(down = prev, number=self.countRoom())
                self = self.down
        if next.lower() == 'a':
            if self.left == None:
                print('It seems that this door is locked.')
            else:
                prev = self
                self.left = Room(right = prev, number=self.countRoom())
                self = self.left
        if next.lower() == 'd':
            if self.right == None:
                print('It seems that this door is locked.')
            else:
                prev = self
                self.right = Room(left = prev, number=self.countRoom())
                self = self.right
    def current_room(self) -> 'Room':
        '''
        Returns the current room
        '''
        return self

    def countRoom(self):
        self.count += 1
        return self.count

def start_room():
    """Instantiates a spawn room"""
    current_room = Room()
    return current_room

class Grid:
    def __init__(self, x, y):
        self.grid = [{0 : None, 1 : None, 2 : None, 3 : None, 4 : None},
                    {0 : None, 1 : None, 2 : None, 3 : None, 4 : None},
                    {0 : None, 1 : None, 2 : None, 3 : None, 4 : None},
                    {0 : None, 1 : None, 2 : None, 3 : None, 4 : None},
                    {0 : None, 1 : None, 2 : None, 3 : None, 4 : None}]
        i = 0
        #Spawning creatures
        while i < 5:
            if self.grid[random.randint(0, 4)][random.randint(0, 4)] == None:
                self.grid[random.randint(0, 4)][random.randint(0, 4)] = {'type' : 'creature', 'creatures':[]}
            i = i + 1
        k = 0
        # Spawning items
        while k < 5:
            if self.grid[random.randint(0, 4)][random.randint(0, 4)] == None:
                self.grid[random.randint(0, 4)][random.randint(0, 4)] = {'type' : 'items', 'items':[]}
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
        action = input('Type an action:')
        return action
        
    def move(self, position : list):
        '''
        Update user position and coordinates in the room
        '''
        self.coordinates = position
    
    def is_encounter(self):
        '''
        Return true if user coordinates are currently on a creature tile.
        '''
        if self.grid[self.get_position()[0]][self.get_position()[1]]['type'] == 'creature':
            return True
        else:
            return False

    def get_enemies(self):
        '''
        Return the enemies on that tile
        '''
        return self.grid[self.get_position()[0]][self.get_position()[1]]['creatures']
    def is_item(self):
        '''
        Return true if user coordinates are currently on a item tile.
        '''
        if self.grid[self.get_position()[0]][self.get_position()[1]]['type'] == 'item':
            return True
        else:
            return False
            
    def get_items(self, coordinates : list) -> str:
        '''
        If user is on an item tile, return the item on that tile
        '''
        return self.grid[self.get_position()[0]][self.get_position()[1]]['items']
    def remove(self):
        '''
        After a defeating a creature or picking up an item, remove it from the grid
        '''
        self.grid[self.get_position()[0]][self.get_position()[1]] = None
        


#Start
def start_menu():
    print('Welcome to FNAF:Reckoning!')
    choice = input("Type 'Start' to begin or 'Info' for more information: ")
    if choice.lower() == 'start':
        choose_character()
    elif choice.lower() == 'info':
        info()
    else:
        print("Please type either Start or Info." )
        start_menu()

def info():
    print('1. Freddy Fazbear')
    print('2. Bonnie')
    print('3. Chica')
    print('4. Foxy')
    cr = input('Please select a character to read their description or Back to return to start menu: ')
    if cr.lower() == 'freddy':
        print('HP: 100')
        print('Description: The lovable brown bear enters the dungeon, ready to face any and all challenges in his way. With his trusty microphone, Freddy faces fear head on as he ventures deeper into the spiraling depths of the abyss.')
        print('Ability: Lullaby - Freddy sings a lullaby, causing all nearby monsters (except the boss) to fall asleep (for 3 turns) , allowing Freddy to walk past them without alerting them.')
        print('Passive: Freddy does increased damage against enemies that are asleep.')
        print('Attacks:')
        print('1. Mic Toss')
        print('2. Sing')
        print('3. The Bite')
        print('--------------------------------------------------------')
        info()
        
    elif 'bonnie' in cr.lower():
        print('HP: 100')
        print('Description: Bonnie the bunny is here and he is ready to stir up a storm. He treads through the treacherous dungeon as he sends rumbles through each room, pathing a way for him to dive deeper into the dungeons.')
        print('Ability: Reverb - Bonnie strums his guitar, sending shockwaves in a specific direction towards enemies, hitting each of them for 10 damage each and immediately enters combat with them. This ability stacks up to 2 times.')
        print('Passive: If there are more enemies than Bonnie in the room, Bonnie increases his attacks by 5 damage.')
        print('Attacks:')
        print('1. Rift')
        print('2. Gatecrash')
        print("3. Rock 'n' Roll")
        print('--------------------------------------------------------')
        info()
        
    elif 'chica' in cr.lower():
        print('HP: 100')
        print('Description: Chica is afraid of the darkness, hence she brought her best friend along with her - cupcake. Cupcake reassures her constantly that everything will be fine and helps her get through the dungeons, yet honestly she just wants to go back to the pizzeria and feast on pizza. ')
        print("Ability: Cupcake - Chica throws her cupcake, causing it to explode in a 3x3 area once the cupcake comes into contact with a solid object, dealing 30 damage to enemies within its area.")
        print('Passive: Chica’s cupcake acts as a light source, however her fear gauge increases quicker when she is in the dark.')
        print('Attacks:')
        print('1. Pizza Slice')
        print('2. Decoy')
        print("3. Devour")
        print('--------------------------------------------------------')
        info()
        
    elif 'foxy' in cr.lower():
        print('HP: 85')
        print('Description: Foxy brandishes his hook, waiting for his next unsuspecting prey to walk past him as he lurks in the shadows. His unique eyes allow him to adapt to the darkness, but is also the reason why he is largely deterred from light sources. Though Foxy may be seen as arrogant and boastful by others, his band members know that he just wants to be able to be someone to somebody, in this case a better teammate for his friends.')
        print('Ability: Scamper - Foxy dashes in a targeted direction, dealing 50 damage to any enemies in his way and takes 5 damage for each solid object hit.')
        print('Passive:')
        print('Foxy regenerates 5 hp each time he defeats an enemy.')
        print('Foxy does not have a fear bar but light causes him to take 5 damage when he comes into contact with it.')
        print('When Foxy’s health falls below 50%, the damage of his skills increases by 30%.')
        print('Attacks:')
        print('1. Yar-Har')
        print('2. Harvest Moon')
        print("3. Death Grip")
        print('--------------------------------------------------------')
        info()
        
    elif 'back' in cr.lower():
        start_menu()
    else:
        print('Please enter a valid animatronic.')
        info()
    
def choose_character():
    print('Characters:')
    print('1. Freddy Fazbear')
    print('2. Bonnie')
    print('3. Chica')
    print('4. Foxy')
    cr = input('Please select your character or skip if you are ready to start the game: ')
    if cr.lower() == 'freddy':
        print('You have selected Freddy Fazbear.')
        return 'freddy'
    elif 'bonnie' in cr.lower():
        print('You have selected Bonnie.')
        return 'bonnie'
    elif 'chica' in cr:
        print('You have selected Chica.')
        return 'chica'
    elif 'foxy' in cr:
        print('You have selected Foxy.')
        return 'foxy'
    elif 'skip' in cr.lower():
        print('The game will begin.')
        return 'skip'
    else:
        print('Please enter a valid animatronic.')
        return None



#accuracy
def accuracy(hit_chance):
    miss_chance = random.randint(1, 100)
    if miss_chance > hit_chance:
        return False
    else:
        return True

#Characters and Enemies
class GB:
    def __init__(self, name, status=None, counter=0, health=50, damage=0):
        self.name = name
        self.health = health
        self.counter = counter
        self.status = status if status is not None else []
        self.damage = damage

    def take_damage(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} has died!")

    def add_status(self, status):
        self.status.append(status)

    def remove_status(self, status):
        if status in self.status:
            self.status.remove(status)

    def has_status(self, status):
        return status in self.status

    def turn_end(self):
        self.counter -= 1

    def get_stats(self, target):
        print(f"{self.name}'s stats")
        print(f"HP: {self.health}")
        #print(f"Light level: {self.light}")
        if self.status == []:
            print('Status: No statuses.')
        else:
            for status in self.status:
                print(f'Status: {status}')

    def attack(self, target):
        if 'sleep' in self.status:
            print(f'{self.name} is asleep!')
            sleep(self)
        else:
            print(f"{self.name} attacks {target.name}!")
            n = random.randint(1, 100)
            if n < 50:
                if accuracy(80) == True:
                    print(f"{self.name} used Bash!")
                    self.damage += 10
                    target.take_damage(self.damage)
                    self.damage -= 10
                else:
                    print('The attack missed!')
            else:
                if accuracy(80) == True:
                    print(f"{self.name} used Ram!")
                    self.damage += 15
                    target.take_damage(self.damage)
                    self.damage -= 15
                else:
                    print('The attack missed!')
        print('---------------------------------------------------------')


class Springtrap:
    def __init__(self, name, evasion=20, status=None, counter=0, health=300, damage=0):
        self.name = name
        self.health = health
        self.evasion = evasion
        self.counter = counter
        self.status = status if status is not None else []
        self.damage = damage

    def take_damage(self, damage: int):
        self.health -= damage
        Glitchtrap.spawn()

    def add_status(self, status):
        self.status.append(status)

    def remove_status(self, status):
        if status in self.status:
            self.status.remove(status)

    def has_status(self, status):
        return status in self.status

    def turn_end(self):
        self.counter -= 1

    def get_stats(self, target):
        print(f"{self.name}'s stats")
        print(f"HP: {self.health}")
        #print(f"Light level: {self.light}")
        if self.status == []:
            print('Status: No statuses.')
        else:
            for status in self.status:
                print(f'Status: {status}')

    def encounter():
        #if current_room() == '?':
            print('You notice the pungent smell of decaying matter.')
            time.sleep(2)
            print('Then, you hear the clanking of metal wires and robotic movement.')
            time.sleep(2)
            print('Finally, you see him.')
            time.sleep(2)
            print('Springtrap.')
        
    def attack(self, target):
        if 'sleep' in self.status:
            print(f'{self.name} is asleep!')
            sleep(self)
        else:
            print(f"{self.name} attacks {target.name}!")
            n = random.randint(1, 3)
            if n == '1':
                print(f'{self.name} used Phantom Mirage!')
                #reduce target's accuracy
            if n == '2':
                if accuracy(40) == True:
                    print(f'{self.name} used Decaying Grasp!')
                    self.damage += 30
                    target.take_damage(self.damage)
                    self.damage -= 30
                    #reduce target's attack
                else:
                    print('The attack missed!')
            if n == '3':
                if accuracy(15) == True:
                    print(f'{self.name} used Eternal Torment!')
                    self.damage += 85
                    target.take_damage(self.damage)
                    self.damage -= 85
                else:
                    print('The attack missed!')
        print('---------------------------------------------------------')



class Glitchtrap:
    def __init__(self, name, status=None, counter=0, health=250, damage=0):
            self.name = name
            self.health = health
            self.counter = counter
            self.status = status if status is not None else []
            self.damage = damage
    
    def take_damage(self, damage: int):
            self.health -= damage
            if self.health <= 0:
                print(f"{self.name} has died!")
    
    def add_status(self, status):
            self.status.append(status)
    
    def remove_status(self, status):
            if status in self.status:
                self.status.remove(status)
    
    def has_status(self, status):
            return status in self.status
    
    def turn_end(self):
            self.counter -= 1
    
    def get_stats(self, target):
        print(f"{self.name}'s stats")
        print(f"HP: {self.health}")
        #print(f"Light level: {self.light}")
        if self.status == []:
            print('Status: No statuses.')
        else:
            for status in self.status:
                print(f'Status: {status}')

    def spawn():
        if Springtrap.health <= 0:
            print("Springtrap has died!")
            time.sleep(2)
            print('Or has he?')
            time.sleep(2)
            print('Springtrap: Did you really think this would be enough to finish me?')
            time.sleep(2)
            print('Springtrap: Death has never been my concern.')
            time.sleep(3)
            print('Springtrap: You forget,')
            time.sleep(3)
            print('Springtrap: I always come back.')
            time.sleep(4)
            print('You watch as the decaying bunny is encapsulated in digital code, turning him into another bunny with stitches running down his sides as he chuckles.')
            time.sleep(5)
            print('Glitchtrap: This is only the beginning.')
    
    def attack(self, target):
        if 'sleep' in self.status:
            print(f'{self.name} is asleep!')
            sleep(self)
        else:
            print(f"{self.name} attacks {target.name}!")
            n = random.randint(1, 100)
            if n > 30 and n < 60: #28% chance to use this attack
                print(f'{self.name} used Corrupt!')
                if accuracy(50) == True:   
                    self.damage += 20
                    target.take_damage(self.damage)
                    self.damage -= 20
                    target.add_status('corrupt')
                    corrupt(target)
                else:
                    print('The attack missed!')
            if n > 15 and n < 31: #17% chance to use this attack
                print(f'{self.name} used Digital Infiltration!')
                if accuracy(30) == True:
                    target.add_status('infiltrated')
                    print(f"{self.name} infiltrated {target.name}'s system!")
                else:
                    print('The attack missed!')
            if n >= 2 and n < 16: #14% chance to use this attack
                print(f'{self.name} used System Overload!')
                if accuracy(40) == True:
                    self.damage += 40
                    target.take_damage(self.damage) #somehow make it hit all players
                    self.damage -= 40
                else:
                    print('The attack missed!')
            if n >= 60: #40% chance to use this attack
                print(f'{self.name} used Pixel Blast!')
                if accuracy(70) == True:
                    self.damage += 15
                    target.take_damage(self.damage)
                    self.damage -= 15
                else:
                    print('The attack missed!')
            if n == 1:  #1% chance to use this attack
                print(f'{self.name} hit the Griddy!') 
                print('You were fascinated and stared in awe.')


class Freddy:
    def __init__(self, name, status=None, counter=0, attacking=0, health=100, inventory=None):
        self.name = name
        self.health = health
        self.counter = counter
        self.status = status if status is not None else []
        self.attacking = attacking
        self.inventory = inventory if inventory is not None else []

    def heal(self, amnt):
        self.health += amnt
        print(f"Freddy healed {amnt} hp!")

    def take_damage(self, damage_taken):
        self.health -= damage_taken
        print(f"Freddy took {damage_taken} damage!")
        print(f'HP left:{self.health}')
        if self.health <= 0:
            print('You died!')

    def inventory(self, item):
        print(f"{self.name}'s Inventory:")
        for item in self.inventory:
            print(item)

    def add_status(self, status):
        self.status.append(status)
        
    def add_items(self, item):
        self.inventory.append(item)

    def attack(self, target):
            print(f"Freddy attacks {target.name}!")
            print('1. Mic Toss  90 acc  15 dmg')
            print('2. Sing  40 acc - dmg')
            print('3. The Bite  19 acc 87 dmg')
            atk = input("Please select an ability to use: ")
            if atk == '1':    
                print('Freddy used Mic Toss!')
                if accuracy(90) == True:
                    self.passive(target)
                    self.attacking += 15
                    print(f"{target.name} took {self.attacking} damage!")
                    target.take_damage(self.attacking)
                    self.attacking -= 15
                    self.depassive(target)
                else:
                    print('The attack missed!')
            if atk == '2':
                print('Freddy used Sing!')
                if target.has_status('sleep'):
                    print(f'{target.name} is already asleep!')
                    return
                else:
                    if accuracy(100) == True:
                        print(f"{target.name} fell asleep!")
                        sleep(target)
                        target.add_status('sleep')
                    else:
                        print('The attack missed!')
            if atk == '3':
                print('Freddy used The Bite!')
                if accuracy(19) == True:
                    self.passive(target)
                    self.attacking += 87
                    print(f"{target.name} took {self.attacking} damage!")
                    target.take_damage(self.attacking)
                    self.attacking -= 87
                    self.depassive(target)
                else:
                    print('The attack missed!')
            if atk < '1' or atk > '3':
                print('Please select a valid ability.')
                self.attack(target)
            
    
    def passive(self, target):
        if 'sleep' in target.status:
            self.attacking += 5

    def depassive(self, target):
        if 'sleep' in target.status:
            self.attacking -= 5

    def remove_status(self, status):
        if status in self.status:
            self.status.remove(status)

    def has_status(self, status):
        return status in self.status

    def display_turn(self):
        print(f"It is {self.name}'s turn.")

    def get_stats(self):
        print(f"{self.name}'s stats")
        print(f"HP: {self.health}")
        #print(f"Light level: {self.light}")
        if self.status == []:
            print('Status: No statuses.')
        else:
            for status in self.status:
                print(f'Status: {status}')

    def prompt_action(self, target):
        print('1. Attack')
        print('2. Stats')
        print('3. Light Level')
        print('4. Item')
        dec = input('Please choose an action: ')
        if dec in ['attack', 'stats', 'light', 'item']:
            return dec
        else:
            return None

    def prompt_light():
        L = input('Do you want to increase or decrease your light level: ')
        if 'increase' in L.lower():
            return L
        elif 'decrease' in L.lower():
            return L
        elif 'back' in L.lower():
            return L
        else:
            print('Please choose either increase, decrease or back.')

#Status
def sleep(target):
    if target.has_status('sleep'):
        if target.counter != 0:
            print(f'{target} is already asleep!')
            target.turn_end()
        else:
            target.remove_status('sleep')
            print(f'{target.name} woke up!')
    else:
        target.counter += 3
        print(f'{target} fell asleep!')


def corrupt(target):
    if target.has_status('corrupt'):
        if target.counter != 0:
            print(f'{target} is already corrupted!')
            target.turn_end()
        else:
            target.remove_status('corrupt')
            print(f'{target.name} stabilised itself!')
    else:
        target.counter += 1
        print(f'{target} has been corrupted!')


def infiltrated(target):
    if target.has_status('infiltrated'):
        print(f'{target} was infiltrated by Glitchtrap, causing them to lose a turn!')
        target.remove_status('infiltrated')
    else:
        pass
