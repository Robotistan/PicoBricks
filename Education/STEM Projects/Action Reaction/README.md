## Action Reaction
As Newton explained in his laws of motion, a reaction occurs against every action. Electronic systems receive commands from users and perform their tasks. Usually, a keypad, touch screen, or button is used for this job. Electronic devices respond verbally, in writing, or visually to inform the user that their task is over and what is going on during the task. In addition to informing the user of these reactions, it can help to understand where the fault may be in a possible malfunction.

#### Project Details
Different types of buttons are used in electronic systems. Locked buttons, push buttons, switched buttons... There is 1 push button on Picobricks. They work like a switch, they conduct current when pressed and do not conduct current when released. In the project, we will understand the pressing status by checking whether the button conducts current or not. If it is pressed, it will light the LED, if it is not pressed, we will turn off the LED.

#### Project Algorithm
- Start 
- If the button is pressed, turn on the LED module. 
- Turn off the LED when the button is not pressed.
- Return to the first step

![200255663-5b9e0de8-018c-4caf-be62-d8b358e5ad27](https://user-images.githubusercontent.com/112697142/222446162-8500d004-1cb4-4752-bd6f-a6ca85d65b11.png)

MicroBlocks Code of The Project
Let’s install the PicoBricks library on our project page. Then, let’s drag "when" block from the “control” block to our project page and drag the “PicoBricks button”  block from the PicoBricks library into it. Thanks to this block we have created, all the code blocks we drag under will be realized when we press the button on PicoBricks. Since we want the LED module to work when we press the button, let’s drag "PicoBricks set red LED" block to our project page and create the code block below.

Now, let’s create the code blocks necessary to create the expressions that will happen when the button on PicoBricks is not pressed. Fİrstly, let’s drag "when" block to our project page. Then, let’s drag "not" block from the operator blocks into this block. The expression we drag into the “note” block corresponds to the situations in which that block is negative. When we drag the “PicoBricks button” block into the “note” block, the code block is ready to detect the situations in which the button is not pressed. Then, let’s drag these blocks into the “when” block.

Every block we drag under this block works when the button is not pressed. Since we want the LED to turn off when we do not press the button, let's create the following code blocks on our project page.

### The Code of The Project Is Ready!

![allScripts11660](https://user-images.githubusercontent.com/112697142/222450699-b740b820-2bda-41d0-b9e0-8395da316cd7.png)


##### [Click](https://picobricks.com/action-reaction/ "Click") to see the details of the project.
