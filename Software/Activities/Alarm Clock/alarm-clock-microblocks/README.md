## Microblocks
![allScripts1358718](https://user-images.githubusercontent.com/112697142/199731013-85a47825-1123-42a8-8e95-59df500c79e2.png)


##### You can access the Microblocks code of the project by dragging the image to the Microblocks Run tab or clicking [here](https://microblocks.fun/run/microblocks.html#scripts=GP%20Scripts%0Adepends%20%27OLED%20Graphics%27%20%27PicoBricks%27%0A%0Ascript%20525%2098%20%7B%0AwhenStarted%0AOLEDInit_I2C%20%27OLED_0.96in%27%20%273C%27%200%20false%0AOLEDwrite%20%27Good%20night%27%2025%2032%20false%0AwaitMillis%202000%0A%7D%0A%0Ascript%20527%20237%20%7B%0AwhenCondition%20%28%28pb_light_sensor%29%20%3E%2090%29%0AwaitMillis%203000%0ArepeatUntil%20%28pb_button%29%20%7B%0A%20%20OLEDwrite%20%27Good%20morning%27%2015%2032%20true%0A%20%20pb_set_rgb_color%20%28colorSwatch%20255%20255%20255%20255%29%0A%20%20pb_beep%20500%0A%7D%0AOLEDwrite%20%27have%20a%20nice%20day%27%200%2032%20false%0Apb_turn_off_RGB%0AstopTask%0A%7D%0A%0A "here").
