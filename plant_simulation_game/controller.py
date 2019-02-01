#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: hassoun
Controller Object Class that processes the user's input
Contains all the game's mechanics
"""

import emoji

class Controller:

    def __init__(self, game):
        """ This is a controller constructor. It is called to create a new controller
        :param game: Game object to control
        """
        self.game = game # game attribute (game object controlled by the controller)
        
        # dictionary of adding actions user can perform to grow the plant
        self.dict_add_actions = {
                'water': self.game.add_water,
                'light': self.game.add_light,
                'nutrients': self.game.add_nutrients}
        
        # dictionary of removing actions user can perform to grow the plant
        self.dict_remove_actions = {
                'water': self.game.remove_water,
                'light': self.game.remove_light,
                'nutrients': self.game.remove_nutrients}
        
        # dictionary of units for each of the plant's parameters
        self.dict_units = {
                'water': 'drops',
                'light': 'units',
                'nutrients': 'pills'}
        
        # dictionary of emojis for each of the plant's parameters
        self.dict_emoji = {
                'water': ':droplet:',
                'light': ':sun_with_face:',
                'nutrients': ':pill:'}
    
    def run_game(self):
        """ Runs the game. By asking if a user wants to start or quit
        the game
        """
        print("Please chose between the following options:")
        print("%s  Start Game: Press 1"%(
                emoji.emojize(':thumbsup:', use_aliases=True)))
        print("%s  Quit Game: Press 2"%(
                emoji.emojize(':thumbsdown:', use_aliases=True)))
        choice = input("Enter choice:")
        
        if choice == '1':
            self.start_game()
        elif choice == '2':
            self.quit_game()
        else:
            self.run_game()
            
    
    def start_game(self):
        """ Starts the game. Prompts the user with a set of options to chose from
        """
        print("\n")
        print("Starting game...")
        self.period_choice()
        
        return 1
        
        
    def quit_game(self):
        """ Iniitializes the game. By asking if a user wants to start or quit
        the game
        """
        print("\n")
        print("Quitting game...")
        print("Thank you for playing the %s  %s game!"%(emoji.emojize(':seedling:'), self.game.game_name))
        return 1
    
    
    def period_choice(self):
        """ Prompts the user with choices of actions to perform for the current
        time period
        """
        print("\n")
        print("==============================================================")
        print("What would you like to perform for the time period #%d"%self.game.time_period)   
        print("Please chose between the following options:")
        print("--> View Game Status %s : Press 1"%emoji.emojize(':seedling:'))
        print("--> Manage Water %s : Press 2"%emoji.emojize(':droplet:'))
        print("--> Manage Light %s : Press 3"%emoji.emojize(':sun_with_face:'))
        print("--> Manage Nutrients %s : Press 4"%emoji.emojize(':pill:'))
        print("--> Nothing. Continue to the next round! %s : Press 5"%emoji.emojize(':round_pushpin:'))
        print("--> Quit Game %s : Press 6"%emoji.emojize(':thumbsdown:', use_aliases=True))
        print("==============================================================")   
        choice = input("Enter choice:")
        
        if choice == '1':
            self.game.view_game_status()
            self.period_choice()
            
        elif choice == '2':
            self.manage_parameter('water')
            
        elif choice == '3':
            self.manage_parameter('light')
            
        elif choice == '4':
            self.manage_parameter('nutrients')
            
        elif choice == '5':
            self.next_round()
        
        elif choice == '6':
            self.quit_game()
        
        else:
            self.period_choice()
    
    def next_round(self):
        """ Moves the game to the next round (time period)
        """
        print("\n")
        print("Moving to Next Time Period and updating Plant...")
        
        # update the game
        game_status, reason = self.game.update()
        
        if game_status == 0:
            
            next_round = self.game.time_period + 1
        
            if next_round <= self.game.max_time_period:
            
                # increment the game's time period
                self.game.set_time_period(self.game.time_period + 1)
                self.period_choice()
        
            else:
                print("\n")
                print("Seems like you've reached the time period limit of the game! %s"%
                      emoji.emojize(':hear_no_evil:', use_aliases=True))        
                print("GAME OVER! %s  Try again..."%emoji.emojize(':skull:', use_aliases=True))
                print("Thank you for playing the %s  %s game!"%(
                        emoji.emojize(':seedling:'), self.game.game_name))
                return 1
        
        elif game_status == 1:
            print("\n")
            print("CONGRATULATIONS! %s"%emoji.emojize(':clap:', use_aliases=True))
            print("PLANT IS ALIVE %s  and has reached the %.2f inches goal!"%(
                    emoji.emojize(':green_heart:', use_aliases=True), self.game.max_plant_size))
            print("Thank you for playing the %s  %s game!"%(
                    emoji.emojize(':seedling:'), self.game.game_name))
            return 1
            
        else:
            print("\n")
            print("GAME OVER! %s  Try again..."%emoji.emojize(':skull:', use_aliases=True))
            print("PLANT DIED %s  because of: %s"%(emoji.emojize(
                    ':broken_heart:', use_aliases=True), reason))
            return 1
        
    
    def manage_parameter(self, parameter):
        
        print("\n")
        print("==============================================================")
        print("You can either add or remove/reduce %s  %s (%s) for the time period #%d"%(
              emoji.emojize(self.dict_emoji[parameter]),parameter, self.dict_units[parameter],
              self.game.time_period))   
        print("Please chose between the following options:")
        print("--> View Game Status %s : Press 1"%emoji.emojize(':seedling:'))
        print("--> Add %s %s : Press 2"%(parameter, emoji.emojize(':heavy_plus_sign:')))
        print("--> Remove/Reduce %s %s : Press 3"%(parameter, emoji.emojize(':heavy_minus_sign:')))
        print("--> I'm good. Get back to previous menu %s : Press 4"%emoji.emojize(':thumbs_up:'))
        print("==============================================================")   
        choice = input("Enter choice:")
            
        if choice == '1':
            self.game.view_game_status()
            self.manage_parameter(parameter)
        
        elif choice == '2':
            self.add_choice(parameter)
            
        elif choice == '3':
            self.remove_choice(parameter)
            
        elif choice == '4':
            self.period_choice()
        
        else:
            self.manage_parameter(parameter)
            
    def add_choice(self, parameter):
        
        print("\n")
        print("How much %s  %s %s do you want to add (enter 0 to cancel)?"%(
                emoji.emojize(self.dict_emoji[parameter]), parameter, self.dict_units[parameter]))
        choice = input("Enter choice:")
        
        try:
            integer = int(choice)
            if integer > 0:
                self.dict_add_actions[parameter](integer)
                self.manage_parameter(parameter)
            elif integer < 0:
                print('Please enter a positive integer number')
                self.add_choice(parameter)
            else:
                self.manage_parameter(parameter)
        except ValueError:
            print('Please enter integer number')
            
            
    def remove_choice(self, parameter):
        
        print("\n")
        print("How many %s  %s %s do you want to remove/reduce (enter 0 to cancel)?"%(
                emoji.emojize(self.dict_emoji[parameter]), parameter, self.dict_units[parameter]))
        choice = input("Enter choice:")
        
        try:
            integer = int(choice)
            if integer > 0:
                self.dict_remove_actions[parameter](integer)
                self.manage_parameter(parameter)
            elif integer < 0:
                print('Please enter a positive integer number')
                self.remove_choice(parameter)
            else:
                self.manage_parameter(parameter)
        except ValueError:
            print('Please enter integer number')
            self.remove_choice(parameter)
            
        
        
        
        
                
        
        
        
    

