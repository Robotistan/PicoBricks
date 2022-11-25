## Resetting Flash memory
<img src="https://user-images.githubusercontent.com/112697142/203794985-e073254f-8b41-41f4-8bf4-881ad45725aa.jpeg" width="600" height="400">


Pico’s BOOTSEL mode lives in read-only memory inside the RP2040 chip, and can’t be overwritten accidentally. No matter what, if you hold down the BOOTSEL button when you plug in your Pico, it will appear as a drive onto which you can drag a new UF2 file. There is no way to brick the board through software. However, there are some circumstances where you might want to make sure your Flash memory is empty. You can do this by dragging and dropping a special UF2 binary onto your Pico when it is in mass storage mode.

## Code on GitHub
 You can start [here](https://github.com/raspberrypi/pico-examples/blob/master/flash/nuke/nuke.c "here").

