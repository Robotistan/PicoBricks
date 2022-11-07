## Buzz Wire Game Project Details
Projects don't always have to be about solving problems and making things easier. You can also prepare projects to have fun and develop yourself. Attention and concentration are features that many people want to develop. The applications that we can do with this are quite interesting. How about making Buzz Wire Game with Picobricks? You must have heard the expression that computers work with 0s and 1s. 0 represents the absence of electricity and 1 represents its presence. 0 and 1’s come together with a certain number and sequence of combinations to form meaningful data. In electronic systems, 0s and 1s can be used to directly control a situation. Is the door closed or not? Is the light on or off? Is the irrigation system on or not? In order to obtain such information, a status check is carried out. In this project, we will electronically prepare the attention and concentration developer Buzz Wire Game with the help of a conductor wire using the buzzer and LED module with Picobricks. While preparing this project, you will have learned an input technique that is not a button but will be used like a button.

To prepare the project, you need 2 male-male jumper cables and a 15 cm long conductor bendable wire. When the player is ready, it will be asked to press the button to start the game. If the jumper cable touches the conductor wire in the player’s hand when the button is pressed, Picobricks will detect this and give an audible and written warning. The time from the start of the game to the end will also be displayed on the OLED screen. We reset the timer after the user presses the button. Then we will give a voltage of 3.3V to the conductor wire connected to the GPIO1 pin of Picobricks. One end of the cable held by the player will be connected to the GND pin on the Picobricks. If the player touches the jumper cable in his hand to the conductive wire, the GPIO1 pin will drop to the Passive/Off/0 position. Then, it will announce that the game is over, and there will be light, written and audio feedback, then the elapsed time will be shown on the OLED screen in milliseconds. After 5 seconds, the player will be prompted to press the button to restart.

## Wiring Diagram

  ![image](https://user-images.githubusercontent.com/111511331/200278014-f2bb34e2-b307-410c-99fd-6e6eb4cc6805.png)
  
## Construction Stages of the Project

Along with the PicoBricks kit,
1: 2 20 cm male-male jumper cables. One end of the cable to be attached to the GND will be stripped 4-5 cm and made into a ring. 
2: 15-20 cm conductive wire with a thickness of 0.8 mm. Prepare your materials..

![image](https://user-images.githubusercontent.com/111511331/200278238-35209438-8d84-4d88-a849-76ae9a8408ce.png)

Bend the conductor wire on the protoboard as you wish and pass it through the holes, before passing one end, you must pass the male end, which is connected to the GND pin on the PicoBoard, the other end of the cable you have made into a ring.
3: Conductor Wire
4: Jumper cable with one end connected to the GND pin with a looped end.

![image](https://user-images.githubusercontent.com/111511331/200278328-4e7e2f0c-86d2-4478-9a7c-1f0db719fef5.png)
![image](https://user-images.githubusercontent.com/111511331/200278355-a0ded246-b235-4e41-acc2-81812de4ceba.png)

5: One end of the jumper cable, which has both male ends, into the hole right next to the end of the conductive wire you placed on the protoboard
6: Twist the end of the jumper wire and the end of the conductor wire together under the protoboard.
7: Bend the other end of the conductor wire placed on the protoboard so that it does not come out.

![image](https://user-images.githubusercontent.com/111511331/200278468-1a05683a-e030-4b72-99de-ae26f0b1d1ed.png)
![image](https://user-images.githubusercontent.com/111511331/200278502-014d8a02-48b6-4e70-a8d0-9bd6559f4165.png)
![image](https://user-images.githubusercontent.com/111511331/200278542-cf0d3720-534d-4ede-9361-8b411ec2095f.png)

8: Connect the other male end of the jumper cable that you wrapped around the end of the conductor wire in step 6 to the pin no. GPIO1 on the Picoboard

![image](https://user-images.githubusercontent.com/111511331/200278664-7b1b415d-dd7b-4112-99a6-2b9998bd4ed1.png)
![image](https://user-images.githubusercontent.com/111511331/200278685-0f6b5d11-f3cb-4b9f-a1c3-ca724cbd7c50.png)

If you have completed the installation, you can start the game after installing the codes. Have fun. :)

## Project Image

![image](https://user-images.githubusercontent.com/111511331/200279656-8044d5ea-b55f-4783-aa8c-789694db8d19.png)
![image](https://user-images.githubusercontent.com/111511331/200279833-e674abd9-ef9c-4bba-a124-c7cad2005a02.png)
![image](https://user-images.githubusercontent.com/111511331/200279855-0acd263f-394d-45a9-a792-42ad62e2bd31.png)
![image](https://user-images.githubusercontent.com/111511331/200279888-fddfa9e6-5d09-4e61-a9e6-b478aa0c1a16.png)


