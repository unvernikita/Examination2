"""Shell this is what the user see"""

import cmd
from pig import dice, gameplay, Intellegance, user, highscore


class Shell(cmd.Cmd):
    """The introduction to a command driven game of dice"""

    intro = "This is a game of Pig \n"
    prompt = "(PIG)"

    def __init__(self):
        """Instansiate the object"""
        super().__init__()
        self.dice = dice.Dice()
        self.game = gameplay.Gameplay()
        self.two_player = ""
        self.intelligence = Intellegance.Intellegance()
        self.user_comp_1 = user.User
        self.computer = user.User

    def do_players(self, arg):
        """
        User decides to play against computer or another player
        'players 1' - Play against the computer
        'players 2' - Play against a friend
        """
        error_message = "Invalid choice. Write 'players 1' or 'players 2'"
        if arg == "1":
            # Calls the computer intelligence
            print("You have choosen to play against the computer")
            level = input("At what level do you want to start?")
            self.game.computer_intelligence(level)
            user_name = input("What is your name?: ")
            self.user_comp_1 = user.User(user_name)
            self.computer = user.User("Computer")
            self.two_player = "No"
        elif arg == "2":
            print("You have choosen to play against another player.")
            users = self.game.add_two_players()
            users = self.game.check_if_user_exists(users)
            users = self.game.check_saved_game(users)
            user_1 = users[0]
            user_2 = users[1]
            print(
                f"Welcome {user_1.user_name} and "
                f"{user_2.user_name}!   {user_1.user_name} starts. Write "
                f"toss to start the game."
            )
            self.two_player = "Yes"
        else:
            print(error_message)
        return

    def do_toss(self, _):
        """Toss the dices for you"""
        error_msg = "Please enter 'player 1' or 'player 2'."
        dices = self.game.toss()
        if self.two_player == "Yes":
            user = self.game.update_user_score(dices)
            print(f"Dices rolled: {dices[0]}, {dices[1]}")
            if dices[0] == 1 or dices[1] == 1:
                print(
                    f"\nBad luck, you rolled a 1. {user.get_user_name()}"
                    f" no points this round. \n"
                )
            elif dices[0] == 1 and dices[1] == 1:
                print(f"\nNo, two ones, all of  {user.get_user_name()}'s points disapear. \n")
            else:
                if user.get_user_score() >= 100:
                    self.game.winner(user)
                    return
                else:
                    print(
                        f"\n{user.get_user_name()} has {user.round_count}"
                        f" points this round, Toss or Hold?.\n"
                    )
        # Plays against computer
        elif self.two_player == "No":
            self.user_comp_1 = self.game.update_user_score_one_player(
                dices, self.user_comp_1
            )
            print(f"Dices rolled: {dices[0]}, {dices[1]}")
            if dices[0] == 1 or dices[1] == 1:
                print(
                    f"\nBad luck, you rolled a 1. {self.user_comp_1.get_user_name()}"
                    f" no points this round. \n"
                )
                self.game.hold_one_player()
            elif dices[0] == 1 and dices[1] == 1:
                print(
                    f"\nNo, two ones, all {self.user_comp_1.get_user_name()} points disapear. \n"
                )
                self.game.hold_one_player()
            else:
                if self.user_comp_1.get_score() >= 100:
                    self.game.winner(self.user_comp_1)
                    return
                else:
                    print(
                        f"\n{self.user_comp_1.get_user_name()} has "
                        f"{self.user_comp_1.round_count()}"
                        f" points this round, Toss or Hold?.\n"
                    )
        else:
            print(error_msg)

    def do_hold(self, _):
        """Holds the game and start tallys the score and saves it"""
        if self.two_player == "Yes":
            user = self.game.hold()
            print(
                f"\n{user.user_name}'s turn to play. Your total score is "
                f"{user.score} and you have tossed {user.toss_count} times.\n"
            )
        elif self.two_player == "No":
            self.game.hold_one_player()

    def do_quit(self, _):
        """Quits the game"""
        return True

    def do_cheat(self, _):
        """A cheat to directly win the game (for testing purposes only)"""
        print("Cheater.. cheater..")
        cheater =  user.User("Cheater")
        cheater.cheat()
        self.game.winner(cheater)
    
    def do_highscore(self, _):
        """Displays the highscore"""
        display_highscore = highscore.Highscore()
        display_highscore.read_from_file()
        display_highscore.sort_player_highscore()
        print(display_highscore.display())

