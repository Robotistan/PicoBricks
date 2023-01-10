## Score
![allScripts1287706](https://user-images.githubusercontent.com/112697142/211499305-4609f38c-7e8c-4eaf-a2ab-3301b1b18768.png)


##### You can access the Microblocks code of the project by dragging the image to the Microblocks Run tab or clicking [here](https://microblocks.fun/run/microblocks.html#scripts=GP%20Scripts%0Adepends%20%27OLED%20Graphics%27%20%27PicoBricks%27%0A%0Ascript%20468%2092%20%7B%0AwhenStarted%0Ascore%20%3D%200%0AOLEDInit_I2C%20%27OLED_0.96in%27%20%273C%27%200%20false%0Aforever%20%7B%0A%20%20if%20%28%28pb_button%29%20%3D%3D%20%28booleanConstant%20true%29%29%20%7B%0A%20%20%20%20score%20%2B%3D%201%0A%20%20%20%20OLEDwrite%20%27Score%3A%27%200%200%20false%0A%20%20%20%20OLEDwrite%20score%2055%200%20false%0A%20%20%20%20waitMillis%20100%0A%20%20%7D%20else%20%7B%0A%20%20%20%20OLEDwrite%20%27Score%3A%27%200%200%20false%0A%20%20%20%20OLEDwrite%20score%2055%200%20false%0A%20%20%7D%0A%7D%0A%7D%0A%0A "here").
