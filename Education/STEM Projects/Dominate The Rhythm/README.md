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

#### MicroBlocks Code of The Project
Since we will print the speed value from the potentiometer on the OLED display when the project starts, let's start the OLED display and print "Speed:" on the display.

Let's assign the value from the potentiometer to a variable named "rhythm". The value of the potentiometer is between 0-1023. We will use the "rescale" block  to change this value range to 1-7. This block is included in the operator blocks, but it is an advanced block. After clicking “show advanced blocks”, it will appear between operator blocks.

![image](https://user-images.githubusercontent.com/112697142/222668615-b34ccaf7-6e08-4a9f-9f13-6ae5aeced14c.png)

Let’s create the following code blocks to reduce the value of the potentiometer between 1-7 and define it to a variable called “rhythm”.
![image](https://user-images.githubusercontent.com/112697142/222670020-1c9bc1f6-f004-479d-919b-7538d9ab1ffa.png)

Let's print this variable on the OLED display. Then, let's create another variable called “beat” and define this value as 1000 / “rhythm” variable. This action determines how many seconds the tones will sound. Wait 50 milliseconds after this process.

![image](https://user-images.githubusercontent.com/112697142/222670161-03105860-8c17-45bb-b2cc-e798a5f8010e.png)

Since I want these steps to continue continuously, let’s drag it into the “forever” block.

![image](https://user-images.githubusercontent.com/112697142/222670288-36935c00-09f3-4c57-a0f1-767de3d6b84c.png)

#### After pressing the button, let’s do the following steps to make the tones play at the speed we have determined.

![image](https://user-images.githubusercontent.com/112697142/222670433-453436b2-e75c-4e0f-b4f4-0307da3c4727.png)

1. Now, let’s install the “Tone” library and set the tones required for our melody. Then, we determine how many milliseconds these tones will play with the “beat” variable.

![image](https://user-images.githubusercontent.com/112697142/222670779-30ce0074-3a6f-4f79-be80-3c346f793271.png)

2. Since we want to create a melody by repeating these tones twice, let's take them into the "repeat" block and set the repeat value to 2.

![image](https://user-images.githubusercontent.com/112697142/222670952-651e88ab-c3c0-4848-9f34-a6040137b4fb.png)



#### The Code of The Project Is Ready!

![allScripts14501](https://user-images.githubusercontent.com/112697142/222666654-c008cc23-4b1a-4304-ba26-6aabcfdd191f.png)


##### You can access the Microblocks test code by dragging the image to the Microblocks Run tab or clicking [here](https://picobricks.com/dominate-the-rhythm/ "here").
