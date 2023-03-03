## Alarm Clock
Global warming is affecting the climate of our world worse every day. Countries take many precautions and sign agreements to reduce the effects of global warming. The use of renewable energy sources and the efficient use of energy is an issue that needs attention everywhere, from factories to our rooms. Many reasons such as keeping road and park lighting on in cities due to human error, and the use of high energy-consuming lighting tools reduce energy efficiency. Many electronic and digital systems are developed and programmed by engineers to measure the light, temperature and humidity values of the environment and ensure that they are used only when needed and in the right amounts. In this project, we will create a timer alarm that adjusts for daylight using the light sensor in PicoBricks.


![image](https://user-images.githubusercontent.com/112697142/222707381-f2898940-5057-46b7-936f-9e7a8014c581.png)


#### Project Details
In this project, we will make a simple alarm application. The alarm system we will design is designed to sound automatically in the morning. For this, we will use an LDR sensor in the project. At night, the OLED screen will display a good night message to the user, in the morning, an alarm will sound with a buzzer sound, a good morning message will be displayed on the screen, and the RGB LED will light up in white for light notification. The user will have to press the button of Picobricks to stop the alarm. After these processes, which continue until the alarm is stopped, when the button is pressed, the buzzer and RGB LED will turn off and a good day message will be displayed on the OLED screen.


![image](https://user-images.githubusercontent.com/112697142/222708551-4906cee3-b711-4e2b-8835-f7ac96fdba18.png)


#### Project Algorithm
- Start
- Print “Good Night” on the OLED screen.
- If the PicoBricks LDR module has a value greater than 90 ( when the sensor detects the daylight), wait three seconds.
- Until the button is pressed, print “Good morning” on the OLED screen, turn on RGB LED and buzzer.
- If the button is pressed, print “Have a nice day” on the OLED screen and turn of RGB LED.
- Return to the first step. 

#### MicroBlocks Code of The Project
When our project code start, let’s create the following code blocks to wait 2 seconds after printing “Good night” on the OLED screen.

![image](https://user-images.githubusercontent.com/112697142/222709516-ccf44cf8-7ef8-454a-9f51-705ba8c52ba7.png)

When the LDR module detects the daylight, let’s create the necessary block to start the code blocks we want to run.

Let’s assume that the value of the LDR module is greater than 90 when the sun is up (This value differs from environment to environment.). When this condition is happened, let’s create the following code blocks to run the desired code blocks.

![image](https://user-images.githubusercontent.com/112697142/222709647-1f729e88-8006-46b0-8b9d-128ddc2da161.png)

When the sun is up, that is, when the value of the LDR sensor is greater than 90, wait 3 seconds and print "Good morning" on the OLED screen until the button is pressed, turn on the RGB LED and activate the buzzer. Let's drag the following code blocks to perform these operations.

![image](https://user-images.githubusercontent.com/112697142/222709751-52caf452-707d-46d7-bfc9-b566dddc1819.png)


After pressing the button, let's print "Have a nice day" on the OLED screen, turn off the RGB LED and stop the running blocks. Let's drag the following code blocks to run these operations.

![image](https://user-images.githubusercontent.com/112697142/222709817-d73f44c5-8837-4011-ba9a-6dc0c682981f.png)


#### The Code of The Project Is Ready!

![allScripts6850](https://user-images.githubusercontent.com/112697142/222710088-be44d30b-b4e2-4c14-9881-1cf8b9fbd301.png)

##### [Click](https://picobricks.com/alarm-clock/ "here") to see the details of the project.
