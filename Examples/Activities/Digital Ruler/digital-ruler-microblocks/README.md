## Microblocks
![allScripts2424317](https://user-images.githubusercontent.com/112697142/192446513-0c3bf341-7692-492e-98a3-1950ec7d8333.png)



##### You can access the Microblocks codes of the project by dragging the image to the Microblocks Run tab or clicking [here](https://microblocks.fun/run/microblocks.html#scripts=GP%20Scripts%0Adepends%20%27AMRadioTone%27%20%27Distance%27%20%27OLED%20Graphics%27%20%27PicoBricks%27%0A%0Ascript%20433%20101%20%7B%0AwhenCondition%20%28pb_button%29%0Ameasure%20%3D%200%0Apb_set_red_LED%20true%0Apb_beep%2050%0Arepeat%2020%20%7B%0A%20%20measure%20%2B%3D%20%28%27distance%20%28cm%29%27%2015%2014%29%0A%20%20waitMillis%2050%0A%7D%0Adistance%20%3D%20%28%28measure%20%2F%2020%29%20%2B%206%29%0Apb_set_red_LED%20false%0AsendBroadcast%20%27go%20to%20OLED%27%0A%7D%0A%0Ascript%20810%2080%20%7B%0AwhenBroadcastReceived%20%27go%20to%20OLED%27%0AOLEDInit_I2C%20%27OLED_0.96in%27%20%273C%27%200%20false%0AOLEDwrite%20%27%3EDigital%20Ruler%3C%27%203%205%20false%0AOLEDwrite%20%28%27%5Bdata%3Ajoin%5D%27%20%27Distance%3A%27%20distance%20%27cm%27%29%2015%2032%20false%0A%27play%20tone%27%20%27C%27%202%2050%0A%7D%0A%0A "here").
