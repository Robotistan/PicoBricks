## MicroBlocks Code of The Project

![allScripts8355479](https://github.com/Robotistan/PicoBricks/assets/112697142/8b0160c6-9f9c-47f4-9dd3-394312ba8f3a)


##### You can access the Microblocks code of the project by dragging the image to the Microblocks Run tab or clicking [here](https://microblocks.fun/run/microblocks.html#scripts=GP%20Scripts%0Adepends%20%27Distance%27%20%27Servo%27%0A%0Ascript%20386%2070%20%7B%0AwhenStarted%0AsetServoAngle%2021%2035%0Aforever%20%7B%0A%20%20sayIt%20%28%27distance%20%28cm%29%27%2015%2014%29%0A%7D%0A%7D%0A%0Ascript%20762%20114%20%7B%0AwhenCondition%20%28%28%27distance%20%28cm%29%27%2015%2014%29%20%3C%208%29%0AservoValue%20%3D%2035%0ArepeatUntil%20%28-45%20%3E%20servoValue%29%20%7B%0A%20%20servoValue%20%2B%3D%20-1%0A%20%20setServoAngle%2021%20servoValue%0A%20%20waitMillis%2020%0A%7D%0AwaitMillis%202000%0ArepeatUntil%20%28servoValue%20%3E%2035%29%20%7B%0A%20%20servoValue%20%2B%3D%201%0A%20%20setServoAngle%2021%20servoValue%0A%20%20waitMillis%2020%0A%7D%0A%7D%0A%0A "here").
