## Four Operations

![allScripts3153780](https://user-images.githubusercontent.com/112697142/214579004-3278d22d-25ce-46ad-8d92-a997cfb09828.png)


##### You can access the Microblocks code of the project by dragging the image to the Microblocks Run tab or clicking [here](https://microblocks.fun/run/microblocks.html#scripts=GP%20Scripts%0Adepends%20%27OLED%20Graphics%27%0A%0Aspec%20%27%20%27%20%27divide%27%20%27divide%27%0Ato%20divide%20%7B%0A%20%20if%20%28number1%20%3C%20number2%29%20%7B%0A%20%20%20%20result%20%3D%20%28number2%20%2F%20number1%29%0A%20%20%20%20OLEDwrite%20%28%27%5Bdata%3Ajoin%5D%27%20number2%20%27%2F%27%20number1%20%27%3D%27%20result%29%2010%2030%20false%0A%20%20%7D%20else%20%7B%0A%20%20%20%20result%20%3D%20%28number1%20%2F%20number2%29%0A%20%20%20%20OLEDwrite%20%28%27%5Bdata%3Ajoin%5D%27%20number1%20%27%2F%27%20number2%20%27%3D%27%20result%29%2010%2030%20false%0A%20%20%7D%0A%7D%0A%0Aspec%20%27%20%27%20%27multiplied%27%20%27multiplied%27%0Ato%20multiplied%20%7B%0A%20%20result%20%3D%20%28number1%20%2A%20number2%29%0A%20%20OLEDwrite%20%28%27%5Bdata%3Ajoin%5D%27%20number1%20%27X%27%20number2%20%27%3D%27%20result%29%2010%2020%20false%0A%7D%0A%0Aspec%20%27%20%27%20%27plus%27%20%27plus%27%0Ato%20plus%20%7B%0A%20%20result%20%3D%20%28number1%20%2B%20number2%29%0A%20%20OLEDwrite%20%28%27%5Bdata%3Ajoin%5D%27%20number1%20%27%2B%27%20number2%20%27%3D%27%20result%29%2010%200%20false%0A%7D%0A%0Aspec%20%27%20%27%20%27subtracted%27%20%27subtracted%27%0Ato%20subtracted%20%7B%0A%20%20result%20%3D%20%28number1%20-%20number2%29%0A%20%20OLEDwrite%20%28%27%5Bdata%3Ajoin%5D%27%20number1%20%27-%27%20number2%20%27%3D%27%20result%29%2010%2010%20false%0A%7D%0A%0Ascript%20478%20129%20%7B%0AwhenStarted%0AOLEDInit_I2C%20%27OLED_0.96in%27%20%273C%27%200%20false%0Anumber1%20%3D%2020%0Anumber2%20%3D%2010%0Aplus%0Asubtracted%0Amultiplied%0Adivide%0A%7D%0A%0Ascript%201085%2079%20%7B%0Ato%20plus%20%7B%7D%0A%7D%0A%0Ascript%201085%20245%20%7B%0Ato%20subtracted%20%7B%7D%0A%7D%0A%0Ascript%201086%20421%20%7B%0Ato%20multiplied%20%7B%7D%0A%7D%0A%0Ascript%20478%20345%20%7B%0Ato%20divide%20%7B%7D%0A%7D%0A%0A "here").