#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: hassoun

Plant Object Class
Defines a plant, its attributes and methods
"""

import numpy as np

class Plant:
    
    def __init__(self):
        """ This is a plant constructor. It is called to create a new Plant
        """
        self.size = 1 # plant's size in inches 
        
        # plant's water consumption rate in drops per inches over a single time perod
        self.water_c_rate = 100
        
        # plant's light consumption rate in units (lux) per inches over a single time period
        self.light_c_rate = 10
        
        # plant's nutrients consumption rate in pills per inches over a single time period
        self.nutrients_c_rate = 5
        
        # plant's growth rate per unit of water consumed (inches per drops) 
        # over a single time period
        self.water_g_rate = .01 # grows exaclty by 1 inch if gets the water needed
        
        # plant's growth rate per unit of water consumed (inches per light units) 
        # over a single time period
        self.light_g_rate = 0.1 # grows exaclty by 1 inch if gets the light needed
        
        # plant's growth rate per unit of water consumed (inches per pills) 
        # over a single time period
        self.nutrients_g_rate = 0.2 # grows exactly by 1 inch if gets the nutrients needed
        
        # plant's growth coefficients over a single time period
        # gives an indication of the importance of each element (w,l,n) in 
        # the plant growing process
        self.growth_coef = {
                'water': 0.33,
                'light': 0.33,
                'nutrients': 0.33
                }
        
        # differential between the plant's actual water consumption 
        # and the water needed by plant for time period
        self.delta_n_water = 0
        
        # differential between the plant's actual light consumption 
        # and the light needed by plant for time period
        self.delta_n_light = 0
        
        # differential between the plant's actual nutrients consumption 
        # and the nutrients needed by plant for time period
        self.delta_n_nutrients = 0
        
        # boundaries of water needed by plant for time period (% of total need)
        # below or above the plant dies
        self.water_range = [-0.5, 0.5]
        
        # boundaries of light needed by plant for time period (% of total need)
        # below or above the plant dies
        self.light_range = [-0.5, 0.5]
        
        # boundaries of nutrients needed by plant for time period (% of total need)
        # below or above the plant dies
        self.nutrients_range = [-0.5, 0.5]
        
        
    def set_size(self, value):
        """ Updates the plant's size
        :param value: float containing the new value of the plant's size
        """
        self.size = value
    
    
    def get_water_needed(self):
        """ Computes the total water needed by a plant for a time period
        """
        return self.size * self.water_c_rate
    
    
    def get_light_needed(self):
        """ Computes the total light needed by a plant for a time period
        """
        return self.size * self.light_c_rate
    
    
    def get_nutrients_needed(self):
        """ Computes the total nutrients needed by a plant for a time period
        """
        return self.size * self.nutrients_c_rate
    
    
    def get_water_consumption(self, available_water):
        """ Computes the actual water consumption by a plant for a time period
        :param available_water: float containing the available water for the
        plant to use for time period 
        """
        return np.min([available_water, self.get_water_needed()])
    
    
    def get_light_consumption(self, available_light):
        """ Computes the actual light consumption by a plant for a time period
        :param available_light: float containing the available light for the
        plant to use for time period
        """
        return np.min([available_light, self.get_light_needed()])


    def get_nutrients_consumption(self, available_nutrients):
        """ Computes the actual nutrients consumption by a plant for a time period
        :param available_nutrients: float containing the available nutrients for the
        plant to use for time period
        """
        return np.min([available_nutrients, self.get_nutrients_needed()])
    
    
    def set_delta_n_water(self, available_water):
        """ Computes the differential between what was provided to the plant in
        terms of water vs the water needed by plant for time period
        :param available_water: float containing the available water for the
        plant to use for time period 
        """
        self.delta_n_water = available_water - self.get_water_needed() 
     
        
    def set_delta_n_light(self, available_light):
        """ Computes the differential between what was provided to the plant in
        terms of light vs the light needed by plant for time period
        :param available_light: float containing the available light for the
        plant to use for time period 
        """
        self.delta_n_light = available_light - self.get_light_needed()


    def set_delta_n_nutrients(self, available_nutrients):
        """ Computes the differential between what was provided to the plant in
        terms of nutrients vs the nutrients needed by plant for time period
        :param available_nutrients: float containing the available nutrients for the
        plant to use for time period 
        """
        self.delta_n_nutrients = available_nutrients - self.get_nutrients_needed()
    
    
    def get_water_growth(self, water_consumed):
        """ Computes the total inches gained by a plant due to consuming a volume of water
        :water_consumed: volume of water consumed in drops
        Returns the growth in inches
        """
        return water_consumed * self.water_g_rate
    
    
    def get_light_growth(self, light_consumed):
        """ Computes the total inches gained by a plant due to light exposure
        :light_consumed: quantity of light used in units
        Returns the growth in inches
        """
        return light_consumed * self.light_g_rate
    
    
    def get_nutrients_growth(self, nutrients_consumed):
        """ Computes the total inches gained by a plant due to nuitrients consumption
        :nutrients_consumed: quantity of nutrients consumed in pills
        Returns the growth in inches
        """
        return nutrients_consumed * self.nutrients_g_rate
    
    
    def get_health(self, growth):
        """Checks the plants health based on it's needs and boundaries for
        a time period
        :growth: plant growth over time period
        Returns a health code and a reason.
        1: plant is alive
        0: plant is dead
        """
        reasons = []
        previous_size = self.size - growth
        status = 1
        
        # check water
        previous_water_needed = previous_size * self.water_c_rate
        water_needs_boundaries = np.multiply(
                self.water_range, previous_water_needed)
        #print(water_needs_boundaries)
        #print(self.delta_n_water)
        
        if self.delta_n_water < water_needs_boundaries[0]:
            reasons.append('not enough water') 
            status = -1
        
        if self.delta_n_water > water_needs_boundaries[1]:
            reasons.append('too much water')
            status = -1
        
        # check light
        previous_light_needed = previous_size * self.light_c_rate
        light_needs_boundaries = np.multiply(
                self.light_range, previous_light_needed)
        #print(light_needs_boundaries)
        #print(self.delta_n_light)
        
        if self.delta_n_light < light_needs_boundaries[0]:
            reasons.append('not enough light') 
            status = -1
            
        if self.delta_n_light > light_needs_boundaries[1]:
            reasons.append('too much light') 
            status = -1

        # check nutrients
        previous_nutrients_needed = previous_size * self.nutrients_c_rate
        nutrients_needs_boundaries = np.multiply(
                self.nutrients_range, previous_nutrients_needed)
        #print(nutrients_needs_boundaries)
        #print(self.delta_n_nutrients)
        
        if self.delta_n_nutrients < nutrients_needs_boundaries[0]:
            reasons.append('not enough nutrients') 
            status = -1
            
        if self.delta_n_nutrients > nutrients_needs_boundaries[1]:
            reasons.append('too much nutrients') 
            status = -1
        
        reason = ", ".join(reasons)
        
        return status, reason
        
        
        
        
        
        
        

