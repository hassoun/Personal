#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: hassoun
Game Object Class
Defines a game, its context and the objects running during the game
"""

from plant import Plant
import numpy as np
import emoji

class Game:
    
    def __init__(self, name, max_time_period, max_plant_size):
        """ This is a game constructor. It is called to create a new Game
        :param name: string containing the name of the game
        :param max_time_period: integer containing the number of "rounds" 
        (time periods) in a game
        """

        # name of the game attribute
        if name is not None:
            self.game_name = str(name)
        else:
            self.ame_name = 'Plant'
        
        # current time period of the game. This value will be incremented as
        # the game goes on
        self.time_period = 1
        
        # game duration in terms maximum number of time periods
        if max_time_period > 0:
            self.max_time_period = max_time_period
        else:
            self.max_time_period = 20
            
        # plant's size to achieve before the end of the game (in inches)
        if max_plant_size > 0:
            self.max_plant_size = max_plant_size
        else:
            self.max_plant_size = 10
        
        # the plant object to grow in the game
        self.plant = Plant()
        
        # the available water for the plant to use at current time period
        self.available_water = 0
        
        # the available light for the plant to use at current time period
        self.available_light = 0
        
        # the available nutrients for the plant to use at current time period
        self.available_nutrients = 0
        
        
    def set_time_period(self, value):
        """ Updates the game's current time period value (round #)
        :param value: integer containing the new game's time period value (round #)
        """
        self.time_period = value
    
    
    def set_available_water(self, water_consumed):
        """ Updates the game's water available for the plant to use for current time period
        I takes into account the plants water consumption
        :water_consumed: water consumed in drops
        """
        self.available_water = np.max((self.available_water - water_consumed,0))
    
    
    def set_available_nutrients(self, nutrients_consumed):
        """ Updates the game's nuitrients available for the plant to use for current time period
        I takes into account the plants nutrients consumption
        :nutrients_consumed: nutrients consumed in pills
        """
        self.available_nutrients = np.max((self.available_nutrients - nutrients_consumed,0))
        
        
    def add_water(self, value):
        """ Increments the water level by an added quantity of water (drops)
        :param value: quantity of water (drops) added
        """
        self.available_water += value
        

    def add_light(self, value):
        """ Increments the light level by an increased quantity of light (units)
        :param value: quantity of light (units) increased
        """
        self.available_light += value
        
        
    def add_nutrients(self, value):
        """ Increments the nutrients level by an added quantity of nutrients (pills)
        :param value: quantity of nutrients (pills) added
        """
        self.available_nutrients += value
        
        
    def remove_water(self, value):
        """ Reduces the water level by an removed quantity of water (drops)
        :param value: quantity of water (drops) removed
        """
        if (self.available_water - value) < 0:
            print("After removal seems like there is no water left!")
        self.available_water = np.max((self.available_water - value, 0))
    
    
    def remove_light(self, value):
        """ Reduces the light level by an decreased quantity of light (units)
        :param value: quantity of light (units) decreased
        """
        if (self.available_light - value) < 0:
            print("After removal seems like light has been turned off!")
        self.available_light = np.max((self.available_light - value, 0))
    
    
    def remove_nutrients(self, value):
        """ Reduces the nutrients level by an removed quantity of nutrients (pills)
        :param value: quantity of nutrients (pills) removed
        """
        if (self.available_nutrients - value) < 0:
            print("After removal seems like there are no nutrients left!")
        self.available_nutrients = np.max((self.available_nutrients - value, 0))
    
    
    def update(self):
        """ Updates the game's and plant's parameters
        This will simulate the plant's consumption and growth
        Returns the game status and a reason if any
        -1: if the plant is dead
        0: if the plant is alive but the goal is still not achieved
        1: if the plant is alive and the goal is achieved
        """
        
        # simulate plants's consumption
        w,l,n = self.simulate_plant_consumption()
        
        # simulate plant's growth and update its's size
        growth = self.simulate_plant_growth(w, l, n)
        self.plant.set_size(self.plant.size + growth)
        
        # update available ressources (water and nutrients only)
        self.set_available_water(w)
        self.set_available_nutrients(n)
        
        # check plant's health
        status, reason = self.plant.get_health(growth)
        
        # provide game status at end of round
        self.view_game_status(growth, w, l, n)
        
        # did we achieve the game's goal ?
        # evaluated only if the plant is not dead
        if status == 1:
            status = self.game_goal_achieved()
        
        return status, reason
    
    
    def simulate_plant_consumption(self):
        """ Simulates a plant's consumption (usage) in water/light/nutrients
        It also updates the plant's differentials in terms of consumption vs needs
        Returns the consumed (used) water, light and nutrients
        """
        
        # compute actual consumptions
        water_consumed = self.plant.get_water_consumption(self.available_water)
        light_consumed = self.plant.get_light_consumption(self.available_light)
        nutrients_consumed = self.plant.get_nutrients_consumption(self.available_nutrients)
        
        # update the differential between the plant's actual water/light/nutrients
        # consumption and the water needed by plant for time period
        self.plant.set_delta_n_water(self.available_water)
        self.plant.set_delta_n_light(self.available_light)
        self.plant.set_delta_n_nutrients(self.available_nutrients)
        
        
        
        return water_consumed, light_consumed, nutrients_consumed
    
    
    def simulate_plant_growth(self, water_consumed, light_consumed, nutrients_consumed):
        """ Simulates a plant's growth (in inches) depending on the 
        consumed water/light/nutrients
        :water_consumed: water consumed in drops
        :light_consumed: units of light used
        :nutrients_consumed: nutrients consumed in pills
        Returns the plant's growth in inches
        """
        
        # compute growth
        growth = (self.plant.growth_coef['water'] * self.plant.get_water_growth(water_consumed)) + (
                self.plant.growth_coef['light'] * self.plant.get_light_growth(light_consumed)) + (
                        self.plant.growth_coef['nutrients'] * self.plant.get_nutrients_growth(nutrients_consumed))
        
        return growth
        
        
    def view_game_status(self, growth=0, water_consumed=0, light_consumed=0, nutrients_consumed=0):
        """ Displays some information regarding the plant and game current status
        :growth: plant growth in inches
        :water_consumed: water consumed in drops
        :light_consumed: units of light used
        :nutrients_consumed: nutrients consumed in pills
        """
        print("\n")
        print("************************************************")
        print("Current Plant Size %s : %.3f inches"%(emoji.emojize(':round_pushpin:'), self.plant.size))
        print("Water level %s : %.3f drops"%(emoji.emojize(':droplet:'), self.available_water))
        print("Light level %s : %.3f units"%(emoji.emojize(':sun_with_face:'), self.available_light))
        print("Nutrients level %s : %.3f pills"%(emoji.emojize(':pill:'), self.available_nutrients))
        print("-----------------------------------------------")
        print("Plant growth %s : %.3f inches"%(emoji.emojize(':straight_ruler:'), growth))
        print("Water consumption %s : %.3f drops"%(emoji.emojize(':droplet:'), water_consumed))
        print("Light used %s : %.3f units"%(emoji.emojize(':sun_with_face:'), light_consumed))
        print("Nutrients consumption %s : %.3f pills"%(emoji.emojize(':pill:'), nutrients_consumed))
        print("-----------------------------------------------")
        print("Plant water consumption vs need %s : %.3f drops"%(emoji.emojize(':droplet:'), self.plant.delta_n_water))
        print("Plant light provided vs need %s : %.3f units"%(emoji.emojize(':sun_with_face:'), self.plant.delta_n_light))
        print("Plant nutrients consumption vs need %s : %.3f pills"%(emoji.emojize(':pill:'), self.plant.delta_n_nutrients))
        print("************************************************")
    
    
    def game_goal_achieved(self):
        """ Checks if the game's goal has been achieved>
        That is to say if the plant has reached the maximum heigth
        """
        if self.plant.size >= self.max_plant_size:
            return 1
        else:
            return 0
