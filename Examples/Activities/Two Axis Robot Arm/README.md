## Two Axis Robot Arm Project Details
Robot arms have replaced human power in the industrial field. In factories, robotic arms undertake the tasks of carrying and turning loads of weights and sizes that cannot be carried by a human. Being able to be positioned with a precision of one thousandth of a millimeter is above the sensitivity that a human hand can exhibit. When you watch the production videos of automobile factories, you will see how vital the robot arms are. The reason why they are called robots is that they can be programmed to do the same work with endless repetitions. The reason why it is called an arm is because it has an articulated structure like our arms. How many different directions a robot arm has the ability to rotate and move is expressed as axes. Robot arms are also used for carving and shaping aluminum and various metals. These devices, which are referred to as 7-axis CNC Routers, can shape metals like a sculptor shapes mud. According to the purpose of use in robot arms, stepper motor and servo motors, which are a kind of electric motor, are used. PicoBricks allows you to make projects with servo motors.

In preparation for the installation, we will first write and upload the codes to set the servo motors to 0 degrees. When an object is placed on the LDR sensor, the robot arm will bend down and close its open gripper. After the gripper is closed, the robot arm will rise again. As a result of each movement of the robot arm, a short beep will be heard from the buzzer. The RGB LED will glow red when an object is placed on the LDR sensor. When the object is held by the robot arm and lifted into the air, the RGB LED will turn green. Servo motor movements are very fast. In order to slow down the movement, we will code the servo motors with a total of 90 degrees of movement, 2 degrees each at 30 millisecond intervals. We’re not going to do this for the gripper to close. In order for the servo to perform its holding and releasing function, print and assemble the necessary parts from the 3D printer from the link [here](https://www.thingiverse.com/thing:2302957/files "here").

## Wiring Diagram

  ![image](https://user-images.githubusercontent.com/111511331/200284435-a870a200-d576-4c4c-af26-5086a5b301a9.png)
  
## Construction Stages of the Project

Prepare the parts of the Pan-Tilt kit to prepare the project. Carry your 3D printed parts, waste cardboard pieces, hot silicone glue and scissors with you.
 
![image](https://user-images.githubusercontent.com/111511331/200284827-480c1892-e13a-45d4-a904-a3a0e5efc0a4.png)



1.	First of all, we will prepare the fixed arm of the robot arm. Make an 8 cm high cardboard cylinder into the rounded part of part D. Place it on the D part and attach or glue it with silicone.
 
 ![image](https://user-images.githubusercontent.com/111511331/200284859-a883a1f2-e6b6-45ee-b128-051cf150ac2c.png)

2.	Place the head that came out of the servo motor package on the C part by shortening it a little. Fix with the smallest screws from the Pan Tilt kit.
  
  ![image](https://user-images.githubusercontent.com/111511331/200284886-c7dedd84-af78-4b6a-9f08-02c8bd3a812a.png)
 ![image](https://user-images.githubusercontent.com/111511331/200284918-3f8aac69-88ea-4b26-8f9d-de43a24ec72e.png)

3.	Fix parts A and C together with 2 pointed screws.
 
 ![image](https://user-images.githubusercontent.com/111511331/200285081-fc9c3ed7-e460-4f8b-9e56-3667c39cde10.png)

4.	Internally attach the servo motor to part C. Then place the servo motor on part B and screw it.
  
  ![image](https://user-images.githubusercontent.com/111511331/200285113-0ece014b-d3e4-4d3d-bbc5-aa793fce45a1.png)
![image](https://user-images.githubusercontent.com/111511331/200285147-5b7fee8d-5241-4c19-8958-08eb72bb5329.png)

5.	For the holder, cut one of the servo motor heads in the middle of the gear part that you printed on the 3D printer and place it into the gear. Then screw it to the servo motor.
  
  ![image](https://user-images.githubusercontent.com/111511331/200285172-02519527-d58d-4e81-bdce-9dbee4cd9912.png)
![image](https://user-images.githubusercontent.com/111511331/200285199-e0c46432-5634-4dff-8b72-5c526fb8861d.png)

6.	Adhere together the 3D printed Linear gear and the handle with strong adhesive.
 
 ![image](https://user-images.githubusercontent.com/111511331/200285431-0374773a-3ddd-45ef-adf6-cd3765e4e106.png)

7.	Place the servo in the 3D print holder and fix it. You can do this with hot silicone or by screwing. When placing the servo gear on the linear gear, make sure it is fully open.
 
 ![image](https://user-images.githubusercontent.com/111511331/200286437-71da362e-78a9-47d9-9cac-f2c5d89eddbb.png)

8.	Attach the holding servo system to part B with silicone.

 ![image](https://user-images.githubusercontent.com/111511331/200286458-aac7b0e5-da19-4d9b-bd9f-d9b5c49c7017.png)

9.	Pass the piece we prepared in step 3 over the cylinder we prepared from cardboard in the first step and fix it with silicone.
 
 ![image](https://user-images.githubusercontent.com/111511331/200286497-1290d18f-d06e-4d9f-bc66-0c76ff9a1ce5.png)

10.	Put the motor drive jumpers on the Servo pins. Connect the cable of the holding servo to the GPIO21 and the cable of the tilting servo to the GPIO22.
 
 ![image](https://user-images.githubusercontent.com/111511331/200286526-71ae4bb1-9aad-4945-bba8-976bdd245887.png)

11.	Place the motor driver, buzzer, LDR and RGB LED module on a platform and place the robot arm on the platform accordingly. With the 3D Pen printer, you can customize your project as you wish.
 
 ![image](https://user-images.githubusercontent.com/111511331/200286565-1739419b-ea5f-4a60-89d1-0ef6ff5c74ac.png)

12. You can operate the Robot arm if you feed Picobricks with USB or 3 pen batteries from the power jack on the Picoboard.
