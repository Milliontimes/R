import dice
import player
import sys

N_DICES = 2
GOAL_SCORE = 100
DEFAULT_LIMIT = 15

def setup_game():
    # Initialize two dice
    dices = [0] * N_DICES
    for i in range(N_DICES):
        dices[i] = dice.Dice()

    # Initialize a list of players
    name = input("What is your name, human? ")
    human_player = player.Player(name)
    computer_player = player.Player("Computer")
    print(f"Hi, {human_player.name}.")
    
    players = (human_player, computer_player)
    return dices, players

def quit_game():
    print("See you again.")

def print_dices(dices):
    return ' '.join(map(str, dices))

def instructions():
    str_out = "The first player that reaches {} wins.\n".format(GOAL_SCORE)
    str_out += "Enter 'r' to roll the dice.\n"
    str_out += "-If you roll a '1', you lose all your points for the roll and your turn.\n"
    str_out += "-If you roll two '1's, you lose all your score and your turn.\n"
    str_out += "Enter 'h' to hold your points and pass the turn to the next player.\n"
    str_out += "Enter 'q' at any time to quit the game.\n"
    str_out += "Humans go first."
    return str_out

def set_computer_limit(args):
    '''
    Updates the computer limit to the second command line argument
    Parameters:
        args: list
    Returns:
        new_limit: int
    '''
    if len(args) > 1:
        try:
            new_limit = int(args[1])
            if new_limit <= 0:
                raise ValueError("Must be a positive integer.")
            return new_limit
        except ValueError as e:
            print(f"{type(e).__name__}: {e}")
    return DEFAULT_LIMIT

def main(args):
    computer_limit = set_computer_limit(args)
    dices, players = setup_game()
    human_player, computer_player = players

    print(instructions())

    while True:
        for player in players:
            print("\nScore: {} - {}, Computer - {}".format(human_player.name, human_player.score, computer_player.score))
            print("It is now {}'s turn...".format(player.name))

            if player == human_player:
                decision = input("What do you want to do ('q' to quit game, 'r' to roll, 'h' to hold)? ").strip().lower()
                if decision == 'q':
                    quit_game()
                    return
                elif decision == 'r':
                    roll_values = [d.roll() for d in dices]
                    print("You have rolled:", print_dices(roll_values))
                    if 1 in roll_values:
                        print("You rolled a 1. You lose all your points for the roll, and your turn ends.")
                        player.turn_score = 0
                        break
                    else:
                        player.turn_score += sum(roll_values)
                elif decision == 'h':
                    player.score += player.turn_score
                    player.turn_score = 0
                    break
                else:
                    print("I don't understand...")
            else:  # Computer's turn
                while player.turn_score < computer_limit:
                    roll_values = [d.roll() for d in dices]
                    print("Computer has rolled:", print_dices(roll_values))
                    if 1 in roll_values:
                        print("Computer rolled a 1. It loses all its points for the roll, and its turn ends.")
                        player.turn_score = 0
                        break
                    else:
                        player.turn_score += sum(roll_values)
                player.score += player.turn_score
                player.turn_score = 0

            if player.score >= GOAL_SCORE:
                print(f"{player.name} wins!")
                return

if __name__ == "__main__":
    main(sys.argv)
