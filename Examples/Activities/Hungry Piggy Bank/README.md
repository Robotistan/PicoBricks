## Glutton Piggy Bank Project Details
Ultrasonic sensors are sensors that show electrical change by being affected by sound waves. These sensors send sound waves at a frequency that our ears cannot detect and produce distance information by calculating the return time of the reflected sound waves. We, the programmers, develop projects by making sense of the measured distance and the changes in distance. Parking sensors in the front and back of the cars are the places where ultrasonic sensors are most common in daily life. Do you know the creature that finds its way in nature with this method? Because bats are blind, they find their way through the reflections of the sounds they make. Many of us like to save money. It is a very nice feeling that the money we save little by little is useful when needed. In this project, you will make yourself a very enjoyable and cute piggy bank. You will use the servo motor and ultrasonic distance sensor while making the piggy bank.
Different types of buttons are used in electronic systems. Locked buttons, push buttons, switched buttons... There is 1 push button on Picobricks. They work like a switch, they conduct current when pressed and do not conduct current when released. In the project, we will understand the pressing status by checking whether the button conducts current or not. If it is pressed, it will light the LED, if it is not pressed, we will turn off the LED.

HC-SR04 ultrasonic distance sensor and SG90 servo motor will be used in this project. When the user leaves money in the hopper of the piggy bank, the distance sensor will detect the proximity and send it to the Picobricks. According to this information, Picobricks will operate a servo motor and raise the arm, throw the money into the piggy bank and the arm will go down again.

## Wiring Diagram

  ![image](https://user-images.githubusercontent.com/111511331/200290607-73fc418c-cb0e-4691-bba2-897d46624275.png)

## Construction Stages of the Project

You can access the original files and construction stages of the project by clicking [here](https://www.thingiverse.com/thing:2824451 "Heading Link"). Unlike the project in this link, we will use the HC-SR04 ultrasonic distance sensor. You can download the updated 3D drawing files according to the HC-SR04 ultrasonic distance sensor from this [link](https://github.com/Robotistan/PicoBricks/tree/main/Examples/STL%20Files "Heading Link") and get 3D printing.	

 ![image](https://user-images.githubusercontent.com/111511331/200290982-01aee858-3399-4c38-9312-897a76c0d7d2.png)


1: Fix the plastic apparatus of the servo motor to the piggy bank arm with 2 screws.

![image](https://user-images.githubusercontent.com/111511331/200291009-7768a370-7d26-479c-9a79-2cd2b021007d.png)
![image](https://user-images.githubusercontent.com/111511331/200291039-eac1d5bd-2cc3-4807-940b-a2a8e102ca53.png)


2: Fix the second part of the piggy bank arm with the M3 screw and nut to the first part where the hopper is. 

3: Pass the servo motor cable and place it in its slot.

![image](https://user-images.githubusercontent.com/111511331/200291070-ec04710f-9319-4937-ad9e-5bc26c0ae98a.png)
![image](https://user-images.githubusercontent.com/111511331/200291097-bc531ce9-4c9c-43c9-95ce-0bd83920cb9b.png)

4: Place the servo motor and its housing on the body of the piggy bank. You can use hot glue here. 

5: Place the ultrasonic distance sensor in the piggy bank body and fix it with hot glue.

![image](https://user-images.githubusercontent.com/111511331/200291347-f3d3fc44-6059-425f-a3bf-a2ea3ca16abb.png)
![image](https://user-images.githubusercontent.com/111511331/200291376-035b5d7d-e3fc-4afd-9d95-7fd3c00a6599.png)
  

6: Attach the piggy bank arm to the servo motor and fix it to the top cover with M3 screws. 
7: Fix the piggy bank arm to the body with M2 screw.

![image](https://user-images.githubusercontent.com/111511331/200291417-c98d2b9b-5dd4-47b6-a144-1eff2e4d5a20.png)
 ![image](https://user-images.githubusercontent.com/111511331/200291441-563a03d7-6515-4e9d-bb53-7aa1c7262d14.png)
 

8: Plug the cables of the servo motor and ultrasonic distance sensor and connect the power cables. 
9: According to the circuit diagram, connect the cables of the servo motor and ultrasonic distance sensor to the pico.

 ![image](https://user-images.githubusercontent.com/111511331/200291463-94f77c69-9b0a-44b8-a80d-4fbd43d5e9a3.png)


10: Plug Pico's USB cable and reassemble the cables and attach the bottom cover. That is all.
