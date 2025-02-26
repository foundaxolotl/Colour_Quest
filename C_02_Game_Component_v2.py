import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows


# helper functions go here
def get_colours():
    file = open("00_colour_list_hex_v3.csv", "r")
    all_colors = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_colors.pop(0)

    return all_colors


def get_round_colours():
    """
    Choose four colours from larger lists ensuring that the scores are all different
    :return: list of colours and score to beat (median of scores)
    """

    all_colour_list = get_colours()

    round_colours = []
    colour_scores = []

    # loop until we have four colours with different scores...
    while len(round_colours) < 4:
        potential_colour = random.choice(all_colour_list)

        # Get the score and check it's not a duplicate
        if potential_colour[1] not in colour_scores:
            round_colours.append(potential_colour)

            # make score an integer ad add it to the list of scores
            colour_scores.append(potential_colour[1])

    # change scores to integers
    int_scores = [int(x) for x in colour_scores]

    # Get median score / target score
    int_scores.sort()
    median = (int_scores[1] + int_scores[2]) / 2
    median = round_ans(median)

    return round_colours, median


def round_ans(val):
    """
    Rounds temperatures to nearest degree
    :param val: Number to be rounded
    :return: Number rounded to nearest degree
    """
    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


# classes start here
class StartGame:
    """

    Initial Game interface (ask users how many rounds they
    would like to play)
    """

    def __init__(self):
        """

        Gets number of rounds from user
        """

        self.start_frame = Frame(pady=10, padx=10)
        self.start_frame.grid()

        # Create play button
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """

        Checks user has entered 1 or more rounds
        """

        Play(5)
        # hide root window
        root.withdraw()


class Play:
    """
    Interface for playing the Colour Quest Game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        # Integers / String Variables
        self.target_score = IntVar()

        # rounds played - starts with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # body for most labels...
        body_font = ("Arial", "12")

        # list of label details
        play_labels_list = [
            ["Rounds # of #", ("Arial", "16", "bold"), None, 0],
            ["Score to beat: #", body_font, "#FFF2CC", 1],
            ["Choose a colour below. Good luck.", body_font, "#D5E8D4", 2],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(item)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up colour buttons...
        self.colour_frame = Frame(self.game_frame)
        self.colour_frame.grid(row=3)

        # create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.colour_button = Button(self.colour_frame, font=("Arial", "12"),
                                        text="Colour Name", width=15)
            self.colour_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", "", 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
            [self.game_frame, "End", "#990000", self.close_play, 21, 7, None]

        ]

        # Create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "16", "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Once interface has been created, invoke new round function for first round.
        self.new_round()

    def new_round(self):
        """
        Chooses four colours, works out median for score to beat.
        Configures button with chosen colours.
        """

        # retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

    def close_play(self):
        # reshow root and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
