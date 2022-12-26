## Number Guessing Game Details
The number guessing game project allows the Picobricks to find a number that you keep in the range of 1-128 by directing the Picobricks with the help of an IR sensor and remote control. 

After pressing the button, Picobricks makes the first guess and waits for the player to direct by using the "up", "down" and "ok" keys of the controller.

![guessnumber](https://user-images.githubusercontent.com/112697142/207285397-acd72479-077e-431d-9374-b91458e7a878.PNG)

## Project Algorithm

- Start when button is pressed.
- Divide the max prediction value by 2.
- If the player presses the up key, that is, if Picobricks’ prediction is less than the player’s number, divide the guess interval by 2 again and add it to the current Picobricks’ prediction.
- If the player presses the down key, that is, if Picobricks’ prediction is greater than the player’s number, divide the guess interval by 2 again and subtract it from the current Picobricks’ prediction.
- If the player presses “ok” button, end the game and congratulate Picobricks.
- Repeat the 2nd, 3rd and 4th steps until the “ok” button is pressed.
- Return the 1st step.


## Project Pin Diagram
![Adsız tasarım](https://user-images.githubusercontent.com/112697142/207284717-e2342f7d-a230-4309-97e5-71fd5edb3655.jpg)


## Project Images
![WhatsApp Image 2022-12-13 at 09 49 59 (1)](https://user-images.githubusercontent.com/112697142/207287438-536ca5a5-c756-4bd4-8002-8352aaac00aa.jpeg)



![WhatsApp Image 2022-12-13 at 09 49 59 (2)](https://user-images.githubusercontent.com/112697142/207287448-088290ac-5948-42d1-9cc0-04b300cb329d.jpeg)


![WhatsApp Image 2022-12-13 at 13 01 14 (1)](https://user-images.githubusercontent.com/112697142/207288251-5d721403-ef77-4833-9d81-e090fefe13a2.jpeg)


![WhatsApp Image 2022-12-13 at 09 49 59 (3)](https://user-images.githubusercontent.com/112697142/207287464-1581b1d6-fb6b-428f-85ec-5401331235d5.jpeg)

