## MicroBlocks Code of The Project

![smart_trash_bin](https://user-images.githubusercontent.com/112697142/224255734-dd747734-f9ea-44c0-819a-1ad80618a19a.png)

##### You can access the Microblocks code of the project by dragging the image to the Microblocks Run tab or clicking [here](https://microblocks.fun/run/microblocks.html#scripts=GP%20Scripts%0Adepends%20%27Distance%27%20%27Servo%27%0A%0Ascript%201321%20643%20%7B%0AwhenCondition%20%28%28%27distance%20%28cm%29%27%2015%2014%29%20%3C%2010%29%0AservoValue%20%3D%20-70%0AwaitMillis%202000%0AsetServoAngle%2021%20servoValue%0AwaitMillis%202000%0ArepeatUntil%20%28servoValue%20%3E%20-15%29%20%7B%0A%20%20servoValue%20%2B%3D%205%0A%20%20setServoAngle%2021%20servoValue%0A%20%20waitMillis%20200%0A%7D%0AsayIt%20servoValue%0A%7D%0A%0Ascript%201320%20483%20%7B%0AwhenStarted%0AsetServoAngle%2021%20-15%0Aforever%20%7B%0A%20%20sayIt%20%28%27distance%20%28cm%29%27%2015%2014%29%0A%7D%0A%7D%0A%0A "here").
