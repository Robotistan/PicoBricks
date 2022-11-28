## Microblocks
![allScripts9417](https://user-images.githubusercontent.com/112697142/204211340-792d1629-ef85-4ae2-b271-255285a30d06.png)



##### You can access the Microblocks code of the project by dragging the image to the Microblocks Run tab or clicking [here](https://microblocks.fun/run/microblocks.html#scripts=GP%20Scripts%0Adepends%20%27OLED%20Graphics%27%20%27PicoBricks%27%0A%0Ascript%20531%2079%20%7B%0AwhenStarted%0AOLEDInit_I2C%20%27OLED_0.96in%27%20%273C%27%200%20false%0AOLEDwrite%20%27Press%20the%20button%27%200%2010%20false%0AOLEDwrite%20%27TO%20START%21%27%2025%2035%20false%0A%7D%0A%0Ascript%201004%2089%20%7B%0AwhenCondition%20%28pb_button%29%0Afor%20i%20%28%27%5Bdata%3Arange%5D%27%203%201%29%20%7B%0A%20%20OLEDclear%0A%20%20OLEDwrite%20%28%27%5Bdata%3Ajoin%5D%27%20i%20%27...%27%29%2025%2035%20false%0A%20%20waitMillis%201000%0A%7D%0AOLEDclear%0AOLEDwrite%20%27GO%21%21%21%27%2035%2035%20false%0AwaitMillis%20%28random%201000%205000%29%0Apb_set_red_LED%20true%0AresetTimer%0AwaitUntil%20%28pb_button%29%0Ascore%20%3D%20%28timer%29%0Apb_set_red_LED%20false%0Apb_beep%20200%0AOLEDclear%0AOLEDwrite%20%27Press%20the%20%27%2028%208%20false%0AOLEDwrite%20%27BUTTON%27%2040%2024%20false%0AOLEDwrite%20%27to%20Repeat%21%27%2026%2040%20false%0AOLEDwrite%20%28%27%5Bdata%3Ajoin%5D%27%20%27Score%3A%27%20score%20%27ms%27%29%2010%2056%20false%0A%7D%0A%0A "here").

