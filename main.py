# Import statements

from game import MUDGame


game = MUDGame()


def start_menu():
    """Displays start menu """
    print('Welcome to FNAF:Reckoning!')
    choice = input("Type 'Start' to begin: ")
    while choice.lower() != 'start':
        print("To begin the game, enter 'start'.")
        choice = input("Type 'Start' to begin: ")
    print('--------------------------------------------------------')
    

if __name__ == "__main__":
    start_menu()
    game.setup()
    game.run()
