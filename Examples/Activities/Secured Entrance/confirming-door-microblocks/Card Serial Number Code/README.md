
## Microblocks
![allScripts8406545](https://user-images.githubusercontent.com/112697142/195046858-e4f148d0-4788-4684-aafb-b9105d40b436.png)



##### You can access the Microblocks code of the project by dragging the image to the Microblocks Run tab or clicking [here](https://microblocks.fun/run/microblocks.html#scripts=GP%20Scripts%0Adepends%20%27RFID%20%28RC522%29%27%0A%0Ascript%20531%2078%20%7B%0AwhenStarted%0Arc522_initialize_SPI%2017%0Aforever%20%7B%0A%20%20if%20%28rc522_card_present%29%20%7B%0A%20%20%20%20sayIt%20%28%27%5Bdata%3AjoinStrings%5D%27%20%28rc522_read_uid%29%20%27%2C%27%29%0A%20%20%7D%20else%20%7B%0A%20%20%20%20sayIt%20%27No%20Card%20detected%27%0A%20%20%7D%0A%20%20waitMillis%20100%0A%7D%0A%7D%0A%0A "here").
