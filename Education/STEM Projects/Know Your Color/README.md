## Know Your Color
LEDs are often used on electronic systems. Each button can have small LEDs next to each option. By making a single LED light up in different colors, it is possible to do the work of more than one LED with a single LED. LEDs working in this type are called RGB LEDs. It takes its name from the initials of the colors names Red, Green, and Blue. Another advantage of this LED is that it can light up in mixtures of 3 primary colors. Purple, turquoise, orange…

In this project, you will learn about the randomness used in every programming language. We will prepare an enjoyable game with the RGB LED, OLED display, and button module of PicoBricks.

![image](https://user-images.githubusercontent.com/112697142/222712273-a2be424e-2724-4039-904a-974bbfd25388.png)

#### Project Details
The game we will build in the project will be built on the user knowing the colors correctly or incorrectly. One of the colors red, green, blue, and white will light up randomly on the RGB LED on PicoBricks, and the name of one of these four colors will be written randomly on the OLED screen at the same time. The user must press the button of PicoBricks within 1.5 seconds to use the right of reply. The game will be repeated 10 times, each repetition will get 10 points if the user presses the button when the colors match, or if the user does not press the button when they do not match. If the user presses the button even though the colors do not match, he will lose 10 points. After ten repetitions, the user’s score will be displayed on the OLED screen. If the user wishes, he may not use his right to reply by not pressing the button.
![image](https://user-images.githubusercontent.com/112697142/222712797-27282d46-9e8c-4526-ba43-5d7a87d3484c.png)

#### Project Algorithm
- Start
- Print a random color from green-blue-red-white on the OLED display.
- Activate a random color among the green-blue-red-white colors on the RGB LED.
- If the color on the OLED display and the color on the RGB LED module are the same and the button is pressed, increase the score by 10. 
- The color on the OLED display is the same as the RGB LED, but if the button is not pressed, decrease the score by 10.
- If the color on the OLED display and the RGB LED are not the same, leave the score the same.
- After repeating these operations 10 times, print the score on the display.
- Return to the first step

#### MicroBlocks Code of The Project
1. Since we will be using the OLED display module in our project, let's start by initializing the OLED display.
2. Let's turn off the RGB LED at the start of the project to reset the RGB LED module every time the project starts.
3. Let’s create a variable named “score” to record our score throughout the game.
4. After printing "The game begins" on the OLED display, wait 2 seconds and clean the OLED display.

Let's create the following code blocks on our project page to provide the above mentioned items.

![image](https://user-images.githubusercontent.com/112697142/222713321-ca70b5d5-d51f-4874-8fbb-5a622d4a5c1e.png)

5. Just below these blocks, the main operations necessary for our game will be done. Since the game will repeat 10 times, let’s drag the “repeat loop” and set its value to 10.
6. Inside the repeat loop, there will be a “define” block that randomly flashes colors on the RGB LED module and prints one of four different colors on the OLED display. Let’s name this block “random_color” and drag it into the “repeat” block.

![image](https://user-images.githubusercontent.com/112697142/222714796-5359f41d-040e-4a8f-9378-e5f79a86af2e.png)

#### Let’s analyze “random_color” blocks through the following blocks.

![image](https://user-images.githubusercontent.com/112697142/222713701-da746d37-e92d-4e6f-af09-f477495332d4.png)

7. Let's define another variable called "noSelection" and drag the value of this variable from the operator blocks to the key block. Let's set the value of this key explicitly. This variable will allow us to detect whether the button has been pressed or not.

![image](https://user-images.githubusercontent.com/112697142/222713880-5319e333-86c7-467c-a408-139cc4f2a4e8.png)

8. Let’s create another “define” block named “check_Button” to detect if the button has been pressed.

![image](https://user-images.githubusercontent.com/112697142/222713992-c09796b4-6496-4cd4-9106-381ceb4ddd4a.png)

#### Let’s examine the “check_Button” blocks through the Blocks below

![image](https://user-images.githubusercontent.com/112697142/222714091-4bf044ae-3660-431f-840c-f6e788dd4087.png)

9. After the “check_Button” block works, we clear the display and turn off the RGB LED module.
10. Finally, we print the “score” variable to the display.

![image](https://user-images.githubusercontent.com/112697142/222714334-e08e4ae2-04ab-404a-a07a-69a182623cef.png)

#### The Code of The Project Is Ready!


![allScripts18356](https://user-images.githubusercontent.com/112697142/222714630-15ec646f-b4e4-4caf-9435-21711ed02472.png)



##### [Click](https://picobricks.com/know-your-color/ "Click") to see the details of the project.
