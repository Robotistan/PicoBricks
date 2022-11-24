## Maze Solver Robot Project Details
Coding education is as old as the history of programming languages. Today, different products are used to popularize coding education and make it exciting and fun. The first of these is educational robots. Preparing and coding robots improves children’s engineering and coding skills. Robotics competitions are organized by institutions and organizations to popularize coding education and encourage teachers and students. One of these competitions is the Maze Solver Robot competitions. These robots firstly learn the destination by wandering around the maze and return to the starting point. Then, when they start the labyrinth again, they try to reach their destination in the shortest way possible. Robots use distance sensors while learning about the maze. Infrared or ultrasonic sensors are used in these robots. Smart robot vacuums used in homes and workplaces also work with logic close to the algorithms of maze-solver robots. Thanks to their algorithms that constantly check and map the obstacles, they try to do it completely and without crashing. Most of the smart vacuums are equipped with LIDAR and infrared sensors, which make high-precision laser measurements for distance measurement and obstacle detection. In this project, we will make a simple robot with PicoBricks that you can prepare for maze solver robot competitions.

In the maze solving robot project, we will use the 2WD robot car kit that comes out of the set. We will use the HC-SR04 ultrasonic distance sensor so that the robot can detect the distance in front of it and decide its movements on its own. In the maze, the robot will detect the distance in front of the car and move forward if it is empty. If the distance is less than 5 cm, the car will turn right, measure the distance again, if the distance on the right is greater than 5 cm, it will continue on its way, if it is less, it will turn left and move forward. In this way, by turning right and left, we will enable the vehicle to move forward and exit the maze through the empty roads in the maze.


## Wiring Diagram

  ![image](https://user-images.githubusercontent.com/111511331/200297471-2e0204d3-410f-45d2-9596-54f2e19edb39.png)

## Construction Stages of the Project

In this project, you can build the maze-solving robot car by following the steps you did for the 2WD robot car assembly in the voice-controlled car project. We will not use the HC05 bluetooth module in this project. In order to mount the HC-SR04 ultrasonic distance sensor on the robot, you can download the required part from the link [here](https://github.com/Robotistan/PicoBricks/blob/main/Examples/STL%20Files/HCSR04_Holder.rar "Heading Link") and print from the 3D printer and mount it on the vehicle.

 ![image](https://user-images.githubusercontent.com/111511331/200297686-7129c3c2-4f61-46b7-bda0-0f8c9e728e59.png)

After assembling the robot, you can use cardboard boxes to build the maze. You can make walls out of cardboard, or you can use 3D printed walls to connect the walls with hot glue to build the maze.
 
![image](https://user-images.githubusercontent.com/111511331/200297719-f1e9ffb7-0538-4c3a-866f-498b6a24766c.png)
![image](https://user-images.githubusercontent.com/111511331/200297756-7b151b91-5775-430e-91ab-cedecb5fb3c2.png)
![image](https://user-images.githubusercontent.com/111511331/200297772-2adddb4e-cbf0-449b-8431-d66381d527eb.png)
![image](https://user-images.githubusercontent.com/111511331/200297787-e38b208b-3431-401f-834f-bfd43ca7cd16.png)


