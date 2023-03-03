## Dominate The Rhythm
Many events in our lives have been digitized. One of them is sounds. The tone and intensity of the sound can be processed electrically. So we can extract notes electronically. The smallest unit of sounds that make up music is called a note. Each note has a frequency and intensity. With the codes we will write, we can adjust which note should be played and how long it should last by applying frequency and intensity.
In this project, we will prepare a music system that will play the melody of a song using the buzzer module and adjust the rhythm with the potentiometer module with Picobricks. You will also learn the use of variables, which has an important place in programming terminology, in this project.

![image](https://user-images.githubusercontent.com/112697142/222663338-66930d86-8447-461d-8f27-7c89b2b4733b.png)

#### Project Details
Potentiometer is an analog input module. It is variable resistance. As the amount of current flowing through it is turned, it increases and decreases like opening and closing a faucet. We will adjust the speed of the song by controlling this amount of current with codes. Buzzers change the sound levels according to the intensity of the current passing over them, and the sound tones according to the voltage frequency. With MicroBlocks, we can easily code the notes we want from the buzzer module by adjusting their tones and durations.

#### Project Algorithm
- Start
- Assign the value of the potentiometer to a variable and write it to the display. 
- Wait until the button is pressed
- If the button is pressed, play the determined tones at the specified speed according to the value of the potentiometer.
- Repeat the second step twice.
- Apply the second step until the button is pressed again.

##### You can access the Microblocks test code by dragging the image to the Microblocks Run tab or clicking [here](https://microblocks.fun/run/microblocks.html#scripts=GP%20Scripts%0Adepends%20%27OLED%20Graphics%27%20%27PicoBricks%27%20%27Servo%27%20%27Temperature%20Humidity%20%28DHT11%2C%20DHT22%29%27%0A%0Ascript%20531%20-15%20%7B%0AwhenCondition%20%28pb_button%29%0AOLEDInit_I2C%20%27OLED_0.96in%27%20%273C%27%200%20false%0AOLEDwrite%20%27Hello%20Picobricks%27%200%200%20false%0AOLEDwrite%20%27Temperature%3A%27%200%2010%20false%0AOLEDwrite%20%28temperature_DHT11%2011%29%2095%2010%20false%0AOLEDwrite%20%27Humudity%3A%27%200%2020%20false%0AOLEDwrite%20%28humidity_DHT11%2011%29%2070%2020%20false%0Apb_set_red_LED%20true%0Apb_set_rgb_color%20%28colorSwatch%20200%2039%2014%20255%29%0AwaitMillis%20500%0Apb_set_rgb_color%20%28colorSwatch%202%20190%207%20255%29%0AwaitMillis%20500%0Apb_set_rgb_color%20%28colorSwatch%2012%2022%20190%20255%29%0AwaitMillis%20500%0Apb_set_rgb_color%20%28colorSwatch%20190%20179%205%20255%29%0Apb_beep%20500%0Apb_turn_off_RGB%0Apb_set_relay%20true%0AwaitMillis%201000%0Apb_set_relay%20false%0AsetServoAngle%2021%2090%0AsetServoAngle%2022%2045%0Apb_set_motor_speed%201%20100%0Apb_set_motor_speed%202%20100%0Aforever%20%7B%0A%20%20OLEDwrite%20%27Pot%3A%27%200%2030%20false%0A%20%20OLEDwrite%20%28%27%5Bdata%3AcopyFromTo%5D%27%20%28%27%5Bdata%3Ajoin%5D%27%20%28pb_potentiometer%29%20%27%20%20%27%29%201%204%29%2040%2030%20false%0A%7D%0A%7D%0A%0Ascript%201061%2015%20%7B%0AwhenCondition%20%28%28pb_light_sensor%29%20%3C%2090%29%0Apb_set_rgb_color%20%28colorSwatch%20200%2039%2014%20255%29%0AwaitMillis%20500%0Apb_set_rgb_color%20%28colorSwatch%202%20190%207%20255%29%0AwaitMillis%20500%0Apb_set_rgb_color%20%28colorSwatch%2012%2022%20190%20255%29%0AwaitMillis%20500%0A%7D%0A%0A "here").
