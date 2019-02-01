#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Usage:
    run.py <max_time_periods> <max_plant_size>

Arguments:
    <max_time_periods>       Number (integer) of rounds in the game (# time periods)
    <max_plant_size>       Plant's size (integer) to reach before the end of the game (in inches)

Options:
    -h --help                Show this screen

"""

from game import Game
from docopt import docopt
from controller import Controller
import emoji

def main(args):
    
    # retrieve arguments
    max_time_periods = args['<max_time_periods>']
    try:
        int_period = int(max_time_periods)
        
        max_plant_size = args['<max_plant_size>']
        try:
            int_size = int(max_plant_size)
            
            # initialize game object
            game = Game('Plant simulation', int_period, int_size)
            
            # start game
            print("============================================")
            print('Welcome to the %s game! %s %s %s'%(
                    (game.game_name),emoji.emojize(':seedling:'), emoji.emojize(':seedling:'),
                    emoji.emojize(':seedling:')))
            print("============================================\n")
            
            print("The goal of the game is to grow a plant to %d inches tall"%(game.max_plant_size))
            print("To do so you will have %d time periods in which you'll have to:"%game.max_time_period)
            print("- Decide how much you want to water the plant %s"%emoji.emojize(':droplet:'))
            print("- Decide how much light you want to provide to the plant %s"%emoji.emojize(':sun_with_face:'))
            print("- Decide how much nutrient pills you want to feed the plant %s"%emoji.emojize(':pill:'))
            print("\n")
            # initialize
            c = Controller(game)
            c.run_game()
            
        except ValueError:
            print('Re run script by entering an integer for Max Plant Size')
            return 1
        
    except ValueError:
        print('Re run script by entering an integer for Max Time Period')
        return 1
    

if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)

    
    





