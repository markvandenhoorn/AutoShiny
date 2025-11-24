# AutoShiny
Automated shiny Pokémon hunting setup on Nintendo DS Lite.
It is able to passively find shiny Pokémon in generations 3, 4 and 5 of the mainline Pokémon games.

![WhatsApp Image 2025-11-24 at 12 15 27 (2)](https://github.com/user-attachments/assets/adf6b044-bcaf-43bc-b8ea-3cf8f523e8be)

## Introduction
This GitHub repository functions as a showcase for my project, as well as a loose guide on how to create such a setup. Please note, however, that this is not a step by step tutorial, but rather a conceptual guide to help you understand the overall setup and replicate it in your own way. 

## How It Works 
There are 3 main components in this setup: 
- The Nintendo DS (which plays the game and registers the input)
- The Raspberry Pi (which controls the DS and registers the sounds)
- The breadboard (which acts as the 'bridge', connecting the Pi and the DS with electronics)

Simply said, the Raspberry Pi acts as a controller by sending signals to the buttons of the DS, such that the DS registers these as button presses. The Pi also listens for sounds, and notifies the user when a shiny Pokémon sound is detected. By combining these two elements, shiny hunts can be set up for random encounters, soft resets, fishing etc.

## Materials
To create this setup these materials are required (I recommend buying a few more than listed of most materials):
- Nintendo DS (best to use one you are not emotionally attached to)              1x
- Female to Male jumper wires (I used quite long ones to be safe)                12x
- Male to Male jumper wires                                                      +/- 30x
- 10k ohm resistors                                                              12x
- 2N7000 N-Channel Logic Level Mosfets (don't get scared by the terminology)     12x
- 30 AWG solid core wire                                                         1x 5m (1m is probably enough, I bought a lot to be safe)

## The Nintendo DS
On the DS side there is relatively little setup. T
