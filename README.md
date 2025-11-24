# AutoShiny
Automated shiny Pokémon hunting setup on Nintendo DS Lite.
It is able to passively find shiny Pokémon in generations 3, 4 and 5 of the mainline Pokémon games.

<img src="https://github.com/user-attachments/assets/adf6b044-bcaf-43bc-b8ea-3cf8f523e8be" width="50%" height="50%">

## Introduction
This GitHub repository functions as a showcase for my project, as well as a loose guide on how to create such a setup. Please note, however, that this is not a step by step tutorial, but rather a conceptual guide to help you understand the overall setup and replicate it in your own way. 

## How It Works 
There are 3 main components in this setup: 
- The Nintendo DS (which plays the game and registers the input)
- The Raspberry Pi (which controls the DS and registers the sounds)
- The breadboard (which acts as the 'bridge', connecting the Pi and the DS with electronics)

Simply said, the Raspberry Pi acts as a controller by sending signals to the buttons of the DS, such that the DS registers these as button presses. The Pi also listens for sounds, and notifies the user when a shiny Pokémon sound is detected. By combining these two elements, shiny hunts can be set up for random encounters, soft resets, fishing etc.

## Materials
To create this setup, the following materials are required.  
(*I recommend buying a few extra of most wires and electronics.*)

### **Hardware**
| Item                                                              | Qty |
|-------------------------------------------------------------------|-----|
| Nintendo DS (best to use one you are not emotionally attached to) | 1x  |
| Raspberry Pi (Zero 2W or better) with power supply (assuming you already set this up with Raspian etc)| 1x  |
| Breadboard (400 or 800 points — I used 800)                       | 1x  |

### **Wires & Electronics**
| Item                                                              | Qty |
|-------------------------------------------------------------------|-----|
| Female-to-Male jumper wires (longer is safer)                     | 12x |
| Male-to-Male jumper wires                                         | ~30x |
| 10kΩ resistors                                                     | 12x |
| 2N7000 N-Channel Logic Level MOSFETs                               | 12x |
| 30 AWG solid-core wire                                            | 5m (1m probably enough) |

### **Tools**
| Item                               | Qty |
|------------------------------------|-----|
| Soldering iron                     | 1x  |
| Solder                             | 1x  |
| Tri-wing screwdriver (Y00 or Y0)   | 1x  |
| Small Phillips screwdriver (PH00/PH000) | 1x  |
| Something to cut the plastic of the ds with | 1x  |

### **Optional**
| Item                                                | Qty | Did I use this? |
|-----------------------------------------------------|-----|-----------------|
| Flux (*highly recommended*)                         | 1x  | Yes |
| Wire cutters                                        | 1x  | No |
| 0.5A fuses (*for when you touch the wrong test pin lol*) | As needed | Yes (because I touched the wrong pin) |
| Heat-shrink tubing                                  | 1x  | No |
| Extra header pins                                   | As needed | No (I stripped them off male to male jumper wires) |
| Tweezers                                            | 1x  | Yes |
| Multimeter (*mostly useful if you shorted something*)| 1x  | Yes (Because I blew a fuse) |
| Isopropyl alcohol + (tooth)brush                    | 1x  | Yes (Good practice) |

## The Setup
### Nintendo DS
On the DS side there is relatively little setup. 
Per button you want to automate, you take the 30 AWG wire (stripped a few mm's at the end), and solder it to the test pin you want to automate. Below here is a picture showing which test pins control which buttons (found here: https://www.acidmods.com/moddedmatt/dslight%20pinout.jpg):

<img src="https://github.com/user-attachments/assets/699694e3-0936-467c-a418-1852cccea609" width="70%">

*Important: Make sure to also solder a wire to a ground point on the ds, which you will need to create a common ground between the Pi and the DS. (see next picture for which ground point I chose)*

To make the ds playable by hand as well, I made it so the wires came out of the sides of the ds. For this I cut a few pieces of plastic out of the sides, through which the wires could come out of the ds. Here is a schematic of how I routed the wires approximately:

<img width="70%" alt="Ground" src="https://github.com/user-attachments/assets/3270041a-75a6-4917-bf70-d7d34b088e21" />


