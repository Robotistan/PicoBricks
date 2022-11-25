## Boatloader
The Raspberry Pi Pico is a fantastic piece of technology, but it does have one flaw: there is no reset button. How important is this omission? Sometimes our code can go awry, or we need to flash new firmware to our Pico. When this happens we have to unplug the Pico and plug it back in again in order to reset it. If we pull out the micro USB lead, a mechanical connection which is rated for a finite number of insertions, too many times, we could wear it out. We can prevent this by making a bootloader.

##### Let's start!

<img src="https://user-images.githubusercontent.com/112697142/203794985-e073254f-8b41-41f4-8bf4-881ad45725aa.jpeg" width="600" height="400">

Pico’s BOOTSEL mode lives in read-only memory inside the RP2040 chip, and can’t be overwritten accidentally. No matter what, if you hold down the BOOTSEL button when you plug in your Pico, it will appear as a drive onto which you can drag a new UF2 file. There is no way to brick the board through software. However, there are some circumstances where you might want to make sure your Flash memory is empty. You can do this by dragging and dropping a special UF2 binary onto your Pico when it is in mass storage mode.


- Download the MicroPython UF2 file from the [Raspberry Pi website](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#resetting-flash-memory)
- Hold down the BOOTSEL button on your Pico and plug it into your computer's USB port.
- Open Explorer, and open the RPI-RP2 directory like you would any other hard drive
- Drag and drop the UF2 file into the RPI-RP2 directory



## Code on GitHub
 You can start [here](https://github.com/raspberrypi/pico-examples/blob/master/flash/nuke/nuke.c "here").

