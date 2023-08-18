#test
# from main import game

import data

from game import MUDGame

test = MUDGame()

def test():

    try:
        data.start_menu()
    except:
        print("Start Menu is screwed")
    # try:
    #     test.run()
    # except:
    #     print("The game cannot run lmao.")


    
test()
