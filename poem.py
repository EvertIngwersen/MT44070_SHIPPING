# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 15:47:10 2025

@author: evert
"""

# A Loop of Life

import time

def breathe():
    print("Inhale... Exhale...")

def chase(dreams):
    print(f"Chasing {dreams}...")

def rest():
    print("Resting under the moonlight...")

def wander():
    print("Wandering through the unknown...")

class Heart:
    def beats(self):
        return True  # Keeps the loop going

class Soul:
    def is_weary(self):
        return False  # Change this to True to stop the loop

class Path:
    def is_complete(self):
        return False  # Change this to True to stop the loop

# Define the journey
heart = Heart()
soul = Soul()
path = Path()

dreams = "stars"
doubts = False
dusk = False
dawn = True

while heart.beats():
    breathe()
    
    if dreams and not doubts:
        chase(dreams)
    
    elif dusk and not dawn:
        rest()
    
    else:
        wander()
    
    if soul.is_weary() or path.is_complete():
        break
    
    time.sleep(2)  # Adds a natural rhythm
