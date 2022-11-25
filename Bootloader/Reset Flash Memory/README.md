## Reset Flash Memory
The Raspberry Pi Pico is a fantastic piece of technology, but it does have one flaw: there is no reset button. How important is this omission? Sometimes our code can go awry, or we need to flash new firmware to our Pico. 

When this happens we have to unplug the Pico and plug it back in again in order to reset it. If we pull out the micro USB lead, a mechanical connection which is rated for a finite number of insertions, too many times, we could wear it out. If we have the Pico connected to a powered USB hub with on / off buttons, we can press the button on that, but what if we don’t. 

With very little equipment, and zero code we can build a simple button to reset our Pico ready for the next project.

## What You Need For this
- A Raspberry Pi Pico 
- 2 x Male to Male Jumper Wires 
- Breadboard 
- Pushbutton 

1. Place the Raspberry Pi Pico into the breadboard so that the micro USB port hangs over the end of the breadboard. 

![12](https://user-images.githubusercontent.com/112697142/203993543-3213adcd-9860-4031-9ef0-f7d51c54ccdf.PNG)

2. Insert a push button as you see in the image

![122](https://user-images.githubusercontent.com/112697142/203993843-3c9bbb61-0cbb-41f9-a091-444660001a70.PNG)

3. Connect one of the jumper wires to the GND pin and the right leg of the button, and connect the other to the RUN pin and the left leg of the button.

![123](https://user-images.githubusercontent.com/112697142/203993965-bdffcfa5-3f41-4a5e-b28a-2c2b7dfe9ada.PNG)


#### You can also check [Raspberry Pi Website](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#resetting-flash-memory) for more information.
