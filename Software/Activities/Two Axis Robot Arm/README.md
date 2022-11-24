## Two Axis Robot Arm Project Details
Robot arms have replaced human power in the industrial field. In factories, robotic arms undertake the tasks of carrying and turning loads of weights and sizes that cannot be carried by a human. Being able to be positioned with a precision of one thousandth of a millimeter is above the sensitivity that a human hand can exhibit. When you watch the production videos of automobile factories, you will see how vital the robot arms are. The reason why they are called robots is that they can be programmed to do the same work with endless repetitions. The reason why it is called an arm is because it has an articulated structure like our arms. How many different directions a robot arm has the ability to rotate and move is expressed as axes. Robot arms are also used for carving and shaping aluminum and various metals. These devices, which are referred to as 7-axis CNC Routers, can shape metals like a sculptor shapes mud. According to the purpose of use in robot arms, stepper motor and servo motors, which are a kind of electric motor, are used. PicoBricks allows you to make projects with servo motors.

In preparation for the installation, we will first write and upload the codes to set the servo motors to 0 degrees. When an object is placed on the LDR sensor, the robot arm will bend down and close its open gripper. After the gripper is closed, the robot arm will rise again. As a result of each movement of the robot arm, a short beep will be heard from the buzzer. The RGB LED will glow red when an object is placed on the LDR sensor. When the object is held by the robot arm and lifted into the air, the RGB LED will turn green. Servo motor movements are very fast. In order to slow down the movement, we will code the servo motors with a total of 90 degrees of movement, 2 degrees each at 30 millisecond intervals. We’re not going to do this for the gripper to close. In order for the servo to perform its holding and releasing function, print and assemble the necessary parts from the 3D printer from the link [here](https://www.thingiverse.com/thing:2302957/files "here").

## Wiring Diagram

  ![image](https://user-images.githubusercontent.com/111511331/200284435-a870a200-d576-4c4c-af26-5086a5b301a9.png)
  
## Construction Stages of the Project

Prepare the parts of the Pan-Tilt kit to prepare the project. Carry your 3D printed parts, waste cardboard pieces, hot silicone glue and scissors with you.
 
![image](https://user-images.githubusercontent.com/111511331/200287259-2e44a84d-c206-44d3-8f2b-d6826ed2f50e.png)

1.	First of all, we will prepare the fixed arm of the robot arm. Make an 8 cm high cardboard cylinder into the rounded part of part D. Place it on the D part and attach or glue it with silicone.
 
![image](https://user-images.githubusercontent.com/111511331/200287006-b906db01-cb30-4ee2-bc0f-41e721917be0.png)

2.	Place the head that came out of the servo motor package on the C part by shortening it a little. Fix with the smallest screws from the Pan Tilt kit.
  
![image](https://user-images.githubusercontent.com/111511331/200287377-359c6172-257c-44d6-aa41-bbe1b0be5de9.png)
![image](https://user-images.githubusercontent.com/111511331/200287408-c4d97732-0efd-4633-b540-ced032e47919.png)

3.	Fix parts A and C together with 2 pointed screws.
 
 ![image](https://user-images.githubusercontent.com/111511331/200285081-fc9c3ed7-e460-4f8b-9e56-3667c39cde10.png)

4.	Internally attach the servo motor to part C. Then place the servo motor on part B and screw it.
  
![image](https://user-images.githubusercontent.com/111511331/200287463-64126d7c-afd7-4c6c-8901-e4a3dbdb681d.png)
![image](https://user-images.githubusercontent.com/111511331/200287496-ccf3bdf8-ddba-483b-89a5-4a569e6cde29.png)

5.	For the holder, cut one of the servo motor heads in the middle of the gear part that you printed on the 3D printer and place it into the gear. Then screw it to the servo motor.
  
![image](https://user-images.githubusercontent.com/111511331/200287634-60f11ce5-d658-4f78-b289-fee357c72f02.png)
![image](https://user-images.githubusercontent.com/111511331/200287679-450e3f23-7348-43b9-abde-5656a840c30d.png)

6.	Adhere together the 3D printed Linear gear and the handle with strong adhesive.
 
![image](https://user-images.githubusercontent.com/111511331/200287731-ee08827e-53f7-47dd-80f1-cbe479ba9c70.png)

7.	Place the servo in the 3D print holder and fix it. You can do this with hot silicone or by screwing. When placing the servo gear on the linear gear, make sure it is fully open.
 
![image](https://user-images.githubusercontent.com/111511331/200287967-c35cdae9-fd9b-4b97-8aab-7ecd59947ee3.png)

8.	Attach the holding servo system to part B with silicone.

![image](https://user-images.githubusercontent.com/111511331/200288239-6c7aebcb-f735-487d-b129-723c5876d326.png)

9.	Pass the piece we prepared in step 3 over the cylinder we prepared from cardboard in the first step and fix it with silicone.
 
![image](https://user-images.githubusercontent.com/111511331/200288556-36cc6a52-e8f7-424c-9992-2d76b8aa4109.png)

10.	Put the motor drive jumpers on the Servo pins. Connect the cable of the holding servo to the GPIO21 and the cable of the tilting servo to the GPIO22.
 
![image](https://user-images.githubusercontent.com/111511331/200288950-e8018c08-3a15-4092-9105-82b14be223e2.png)

11.	Place the motor driver, buzzer, LDR and RGB LED module on a platform and place the robot arm on the platform accordingly. With the 3D Pen printer, you can customize your project as you wish.
 
![image](https://user-images.githubusercontent.com/111511331/200286736-4fd9cc53-b112-4109-a18e-9b32bcd88267.png)

12. You can operate the Robot arm if you feed Picobricks with USB or 3 pen batteries from the power jack on the Picoboard.
