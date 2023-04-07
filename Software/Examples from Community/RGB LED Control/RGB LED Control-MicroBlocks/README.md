## Microblocks

![allScripts94684](https://user-images.githubusercontent.com/111511331/201583344-9210bf08-4a94-49ce-9cf8-6ae8f4b152ec.png)


##### You can access the Microblocks codes of the project by dragging the image to the Microblocks Run tab or clicking [here](https://microblocks.fun/run/microblocks.html#scripts=GP%20Scripts%0Adepends%20%27OLED%20Graphics%27%20%27PicoBricks%27%20%27Servo%27%0A%0Ascript%20477%20101%20%7B%0AwhenStarted%0AOLEDInit_I2C%20%27OLED_0.96in%27%20%273C%27%200%20false%0Afor%20i%20%28%27%5Bdata%3Arange%5D%27%20-90%2090%203%29%20%7B%0A%20%20setServoAngle%2021%20i%0A%20%20OLEDclear%0A%20%20OLEDwrite%20%2830%20%2B%20%28i%20%2F%203%29%29%2060%2030%20false%0A%20%20waitMillis%201000%0A%7D%0A%7D%0A%0Ascript%20988%20160%20%7B%0AwhenCondition%20%28pb_button%29%0AstopAll%0A%7D%0A%0Ascript%20851%20252%20%2830%20-%20%28i%20%2F%203%29%29%0A%0A "here").
