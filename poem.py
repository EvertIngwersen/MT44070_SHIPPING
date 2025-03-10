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
        return time.time() - start_time < 5  # Run for 5 seconds

# Define the journey
heart = Heart()
dreams = "stars"
doubts = False
dusk = False
dawn = True

start_time = time.time()  # Mark the start

while heart.beats():
    breathe()
    
    if dreams and not doubts:
        chase(dreams)
    
    elif dusk and not dawn:
        rest()
    
    else:
        wander()
    
    time.sleep(1)  # Adds a natural rhythm

print("The journey pauses, but the story continues...")
