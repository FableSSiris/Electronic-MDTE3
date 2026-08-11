## How to Use Light Controller

### Purpose

The light controller can be used to control any Arduino NeoPixel LED. Whether it is ceiling-mounted, roped or even chandeliered, the light controller can access and manipulate them. It is a multi-purpose product and can be used simply as a light switch, or for cinematography, or even just ambience lighting for your household. 

### How to set up prototype

Contents (\* is replaceable)

- USB cable\*  
- Junction Box  
- 12V DC plug\*  
- Main Controller Box  
- Straight LED 8-bit\*  
- 2 Jumper Wires\*

Procedure

1. Plug the LED into Sector 1 of the Junction Box. Alternatively, the LED can be plugged directly into the 3 header pins, in which case skip steps 2 and 3  
2. Plug the Jumper Wires into Sector 2 of the Junction Box; connect with the main box via the 3 header pins.  
3. Plug the 12V DC plug into a power socket and link to the power jack screwed onto the junction box.  
4. Connect the microcontroller on the main box to a power supply using the USB cable. Plug into a PC to access serial communication outputs and source code.  
5. That’s it\!

### Features & How to Use

- Menus: Use the rotary encoder, main button, and back button to navigate.  
- Toggle: Use the confirm button to turn the NeoPixel LED on/off.

- Brightness: Use the rotary encoder to adjust main LED brightness. Works while Period feature is active.  
- LED: Controls the *analog* LED, with three states: Off, On and Debug (blinks when a button press causes a change in the program)  
- COLOUR: Choose between 9 preset colours for quick colour switching. The default is white.  
- CUSTOM: A custom colour editor that processes RGB values. Can be turned on or off.

- PERIOD: A music-inspired feature that alternates lights to a set rhythm on repeat. The alternating lights are based on both the preset and custom colours (defaults to white & red). There are four settings:  
  - FIR: Chooses whether to start with the preset or custom colour.  
  - RHY: Rhythm editor, with 4 beat-slots. 14 different letter-coded preset beats dictate the final rhythm. The maximum time signature is 4/4, hence the four slots. One beat is always a ♩ equivalent and cannot be changed. The keys are as follows (British):  
    - N: None. If selected in a slot, removes that beat completely and changes the time signature to (4-n)4, n\>0, where n is the total number of Ns in the four slots.  
    - A: Crotchet  
    - B: Quaver  
    - C: Quaver, 2 Semi-quavers  
    - D: 2 Semi-quavers, Quaver  
    - E: Triplet  
    - F: Dotted Quaver, Semi-quaver  
    - G: 4 Semi-quavers  
    - H: Quaver rest, Quaver  
    - I: Quaver, Quaver rest  
    - J: Crotchet rest  
    - K: Semi-quaver rest, 2 Semi-quavers, Semi-quaver rest  
    - L: Semi-quaver rest, 3 Semi-quavers  
    - M: Semi-quaver, Dotted Quaver  
  - PRD: Determines the time it takes to complete one cycle. Range 1 to 10\.  
  - SAVE/TURN ON: Any changes made can only be applied when this widget is pressed (e.g. if you change the preset or custom colour, it won’t work). Press again, or turn off lights, or enter any other period widget to break the cycle.

### Update & Modify

- Download or copy the latest version of code.py on [GitHub](https://github.com/FableSSiris/Electronic-MDTE3). To modify the program, simply use a text editor; ensure you have CircuitPython and a Python compiler installed.  
- To modify hardware, unscrew the bolts to access the protoboards. May require solder iron and other electronic tools. Modified hardware may not be compatible with the CAD housing.  
- Since this is a prototype, it does not have wires linked to any external lights or LEDS. These components must be custom-installed by the end user.  
- Jumper wires should be replaced to fit the user’s needs or setting.

### Debugging

- For software issues or bugs, report them on GitHub. Clearly state the issue and how it affected product function.   
- For hardware, open the housing and check for any loose wires. Try restarting the microcontroller by unplugging the USB, and check for any connection problems with header pins or solder.

