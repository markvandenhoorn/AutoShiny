# AutoShiny
Automated shiny Pokémon hunting setup on Nintendo DS Lite.
It is able to passively find shiny Pokémon in generations 3, 4 and 5 of the mainline Pokémon games.
This GitHub repository functions as a showcase for my project, as well as a loose guide on how to create such a setup. Please note, however, that this is not a step by step tutorial, but rather a conceptual guide to help you understand the overall setup and replicate it in your own way. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/adf6b044-bcaf-43bc-b8ea-3cf8f523e8be" width="50%" height="50%">
</p>
 
## How It Works (High level)
There are 3 main components in this setup: 
- The Nintendo DS (which plays the game and registers the input)
- The Raspberry Pi (which controls the DS and registers the sounds/detects the shinies)
- The breadboard (which acts as the 'bridge', connecting the Pi and the DS with electronics)

Simply said, the Raspberry Pi acts as a controller by sending signals to the buttons of the DS, such that the DS registers these as button presses. The Pi also listens for sounds, and notifies the user when a shiny Pokémon sound is detected. By combining these two elements, shiny hunts can be set up for random encounters, soft resets, fishing etc.

## How it Works (Detailed)
### Nintendo DS
The DS runs the game and registers button presses.
Each button on the nintendo ds acts as a 'switch' for a circuit. The circuit is open by default, meaning that no electricity can flow. When you press a button, the circuit closes and electricity can flow. The DS detects this and registers it as a putton press. By soldering a wire to the test pin corresponding to a button, we can simulate a button press electronically.

### Raspberry Pi
The Raspberry Pi is the controller and the listening device. It can send signals to our circuit, which simulates a button press. It also runs a script that decides which buttons are being pressed at what moment, and listens for a shiny sound. It sends these signals via the GPIO pins (one for each button) to the breadboard, our next component.

### The Breadboard
The breadboard contains all the electronics. Each button has its own circuit, containing: A wire going to the common ground, a wire coming from the Raspberry Pi, the wire coming from the DS's test pin, a N-channel logic level Mosfet and a 10k ohm resistor going to common ground as well (picture in The Setup part for a schematic). 

What essentialy happens, is that the wire from the DS is connected to one end of the Mosfet, and the wire going to ground is connected to the other side. The Mosfet itself acts as a bridge; when there is no voltage on the Mosfet, the bridge is open and no electricity can flow between the DS's test pin and ground (the circuit is open, no button press). We attach a wire from a GPIO pin of the Raspberry Pi to this Mosfet gate, so that we can control it. Now, when we send a signal to the Mosfet gate with the Pi, the bridge closes and electricity can flow, allowing the DS to detect this flow and register a button press. 

In short, the ds's button is part of an open circuit, and giving the circuit access to ground makes it closed, which is then registered as a button press. We control the button's acces to ground using a switch/bridge in the form of a mosfet, which opens and closes depending on the output of a Raspberry Pi GPIO pin, which is fully automatable.

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
| Aux cable                                                         | 1x  |
| 3,5 mm Aux to 2x Jack Female (stereo and microphone)              | 1x  |
| USB-A 3.0 to 3.5mm Jack Audio Adapter (has to work with mic)      | 1x  |

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
On the DS side there is relatively little setup. First, you obviously need to open the ds up. I recommend disconnecting the top and bottom screen, as well as the grey and black wire so you have easy access to everything. 

Per button you want to automate, you take a piece of 30 AWG wire (stripped a few mm's at the end), and solder it to the test pin you want to automate. I wanted to be able to automate all buttons, so I attached wires to all test pins. Below is a picture showing which test pins control which buttons (found here: https://www.acidmods.com/moddedmatt/dslight%20pinout.jpg):

<img src="https://github.com/user-attachments/assets/699694e3-0936-467c-a418-1852cccea609" width="70%">

*Important: Make sure to also solder a wire to a ground point on the ds, which you will need to create a common ground between the Pi and the DS. (see next picture for which ground point I chose)*

To make the ds playable by hand as well, I made it so the wires came out of the sides of the ds. For this I cut a few pieces of plastic out of the sides, through which the wires could come out of the ds. Here is a schematic of how I routed the wires approximately:

<img width="70%" alt="Ground" src="https://github.com/user-attachments/assets/3270041a-75a6-4917-bf70-d7d34b088e21" />

These 30AWG wires are not very well suited for breadboard use, however. Therefore it is wise to join each of these wires to a jumper wire. I took off the header pin of a male to male jumper wire, stripped it +/- 2cm, and then joined the loose end of the 30AWG wire with this stripped part of the jumper wire. The result is a wire that is soldered to the test pin, which has a header pin at the end which we can use in the breadboard. 

You might also want to do this before soldering the wires to the motherboard. I also recommend labeling your wires, so you know which wire is attached to which test pin. If you want to be able to put the ds back together fully, make holes in the DS's housing where the wires will come out. After this you can reassemble the DS. 

### The Raspberry Pi
On the Raspberry Pi side there is very little setup. All you need to do is attach one female to male jumper wire to a GPIO pin of the Pi (female side on the pin, of course). The male side will later go into the breadboard. Make sure you also attach one jumper wire to a ground pin on the Pi. You also need to put one end of the aux cable into the audio splitter, and that into the aux to usb converter, which goes into the usb port of the Raspberry Pi. The other end of the aux cable later goes into the DS.

By now you should have 30AWG wires attached to all desired test pins on the ds, with each of those wires ending in a header pin. For each one of those wires you should also have one jumper wire attached to a GPIO pin of the Pi + 1 for ground (e.g. if you only want to automate L + R + START + SELECT you need wires soldered to those 4 test pins, as well as 4 wires on GPIO pins). The DS and the Pi are completely disconnected from each other right now.

### The Breadboard
This is where we put everything together. First and foremost, we want to create common ground between the Pi and the DS. We do this by sticking the jumper wire that is connected to the ground pin on the Pi, in the ground rail of the breadboard. Then, you take the wire that is soldered to the ground point on the DS, and put that in the same ground rail. Done!

Next, we have to make a little circuit for each of the buttons we want to automate. I will show how to do it for 1 button, after which you can replicate this as many times as you need. 

- First, put the Mosfet in the breadboard, with each of its legs going into a different rail.
- Put the wire coming from the DS test pin in the rail connected to the Mosfet's Drain.
- Connect a 10k ohm resistor from the gate of the Mosfet to ground.
- Put one of the wires attached to a GPIO pin on this gate rail as well.
- Have a wire going from the source of the Mosfet to ground.

<img width="50%" height="50%" alt="image" src="https://github.com/user-attachments/assets/0d2a6c1e-4414-485b-80af-31241f9059ea" />

That's it! You now have the button completely wired up and ready to go. All you need to do now is control it with the Pi and set up the shiny detection part. 

## The Code (WIP, Please notify me if anything does not work properly)
Note that the code I wrote works very well for me, but certain values, thresholds and variables may need to be tweaked before you can use it yourself. 
I will walk you through everything that definitely has to be prepared in order for the code to work, but know that even after that you might need to tweak values yourself. This may mean that writing the code yourself is easier. Feel free to use my code as a baseline or as inspiration when you do. 
For now, only random encounters are reliably working for gen 4 and 5. 

1.  **Install Dependencies:**
    On your raspberry pi, run:
    ```
    sudo apt-get update
    sudo apt-get install python3-dev
    sudo apt-get install libasound2-dev
    ```

    Then

    ```
    pip3 install sounddevice RPi.GPIO pushover-notifications numpy scipy
    ```

3.  **Configure the Script:**
    *   Rename the `config.ini.example` file to `config.ini`.
    *   Open `config.ini` with a text editor.
    *   Fill in your Pushover API keys if you want notifications.
    *   Adjust the GPIO pin numbers and audio input device to match your specific setup. Change `Thresholds` and `Timings` if necessary.

4.  **Run the Script:**
    ```bash
    python main.py
    ```
    The script will then ask you for the Pokémon generation and the type of hunt you want to perform, as well as whether any extra time has to be added for ability procs        and weather messages etc. Note that at this point in time, only random encounters are reliably working. Happy hunting!
