## Action-Reaction Project Details
As Newton explained in his laws of motion, a reaction occurs against every action. Electronic systems receive commands from users and perform their tasks. Usually a keypad, touch screen or a button is used for this job. Electronic devices respond verbally, in writing or visually to inform the user that their task is over and what is going on during the task. In addition to informing the user of these reactions, it can help to understand where the fault may be in a possible malfunction. In this project, you will learn how to receive and react to a command from the user in your projects by coding the button-LED module of Picobricks.

Different types of buttons are used in electronic systems. Locked buttons, push buttons, switched buttons... There is 1 push button on Picobricks. They work like a switch, they conduct current when pressed and do not conduct current when released. In the project, we will understand the pressing status by checking whether the button conducts current or not. If it is pressed, it will light the LED, if it is not pressed, we will turn off the LED.

## Wiring Diagram

  ![image](https://user-images.githubusercontent.com/111511331/200296342-6562dccf-9076-4370-97db-f737d9cb3191.png)

## Construction Stages of the Project

To prepare the project, you need double-sided foam tape, a utility knife, a waste cardboard box of approximately 15x10x5 cm. 

1. Cut the holes for the ultrasonic sensor, OLED screen, button LED module, buzzer, battery box to pass the cables with a utility knife.
  
![image](https://user-images.githubusercontent.com/111511331/200296480-091fdf4d-a47d-4969-900a-aa58103838e6.png)
![image](https://user-images.githubusercontent.com/111511331/200296519-1180edae-13a1-4b43-99fb-09caf142f5ff.png)
![image](https://user-images.githubusercontent.com/111511331/200296586-849d9e45-546f-429b-9f94-40716064d3ef.png)
![image](https://user-images.githubusercontent.com/111511331/200296609-443eb606-c3f2-41ce-803c-a95f058cb729.png)
![image](https://user-images.githubusercontent.com/111511331/200296629-271532b6-a3a6-4fb0-915b-62ee44e8ce02.png)
![image](https://user-images.githubusercontent.com/111511331/200296649-2de9f7c9-2393-47c5-ab88-5e51a8b88d18.png)

  
2. Hang all the cables inside the box and attach the back of the modules to the box with double-sided foam tape. Connect the trig pin of the ultrasonic sensor to the GPIO14 pin and the echo pin to the GPIO15 pin. You should connect the VCC pin to the VBUS pin on the Picoboard.
 
![image](https://user-images.githubusercontent.com/111511331/200296703-e7466bad-c95b-4a0c-94a5-622b7b513607.png)

3. After completing the cable connections of all modules, you can insert the 2-battery box into the power jack of the Picoboard and turn on the switch. That's it for the digital ruler project!

![image](https://user-images.githubusercontent.com/111511331/200296753-b787f730-503b-464d-9a0d-8e28b4a29e2d.png)

