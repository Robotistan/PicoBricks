## Truth or Dare Project Details
Play the very popular game truth or dare, this time with Picobricks. You can change the questions and commands in the code as you wish.
## Rules
- Run the code
- Choose truth or dare by using the potentiometer
- Then, push the button
- If you choose the dare, complete the mission. Else, answer the question correctly.


![allScripts10506782](https://user-images.githubusercontent.com/112697142/204086059-f6268c34-5158-4b41-a07b-8140123718f5.png)



##### You can access the Microblocks codes of the project by dragging the image to the Microblocks Run tab or clicking [here](https://microblocks.fun/run/microblocks.html#scripts=GP%20Scripts%0Adepends%20%27OLED%20Graphics%27%20%27PicoBricks%27%0A%0Ascript%20625%20-212%20%7B%0AwhenStarted%0AOLEDInit_I2C%20%27OLED_0.96in%27%20%273C%27%200%20false%0AOLEDwrite%20%27Spin%27%2035%2030%20false%0AOLEDwrite%20%27the%20bottle%27%2020%2040%20false%0Apb_set_motor_speed%202%2050%0AwaitMillis%202000%0Apb_set_motor_speed%202%200%0AOLEDclear%0AOLEDwrite%20%27Truth%20or%20dare%27%200%2010%20false%0ArepeatUntil%20%28pb_button%29%20%7B%0A%20%20truth_or_dare%20%3D%20%28%28%28pb_potentiometer%29%20%2A%2060%29%20%2F%201023%29%0A%20%20if%20%28%28truth_or_dare%20%25%202%29%20%3D%3D%200%29%20%7B%0A%20%20%20%20OLEDwrite%20%27Truth%20or%20Dare%27%200%2010%20false%0A%20%20%20%20OLEDwrite%20%27truth%27%200%2040%20false%0A%20%20%20%20waitMillis%20500%0A%20%20%20%20OLEDclear%0A%20%20%7D%20else%20%7B%0A%20%20%20%20OLEDwrite%20%27Truth%20or%20Dare%27%200%2010%20false%0A%20%20%20%20OLEDwrite%20%27dare%27%2010%2040%20false%0A%20%20%20%20waitMillis%20500%0A%20%20%20%20OLEDclear%0A%20%20%7D%0A%7D%0Aif%20%28%28turth_or_dare%20%25%202%29%20%3D%3D%200%29%20%7B%0A%20%20OLEDwrite%20%28at%20%27random%27%20%28%27%5Bdata%3AmakeList%5D%27%20%27Do%20you%20have%20a%20hidden%20talent%3F%27%20%27When%27%27s%20the%20last%20time%20you%20apologized%3F%20What%20for%3F%27%20%27What%20is%20your%20biggest%20fear%3F%27%29%29%200%200%20false%0A%7D%20else%20%7B%0A%20%20OLEDwrite%20%28at%20%27random%27%20%28%27%5Bdata%3AmakeList%5D%27%20%27Yell%20out%20the%20first%20word%20that%20comes%20to%20your%20mind%27%20%27Eat%20a%20snack%20without%20using%20your%20hands%27%20%27Dance%20without%20music%20for%20two%20minutes%27%29%29%200%200%20false%0A%7D%0A%7D%0A%0A "here").
