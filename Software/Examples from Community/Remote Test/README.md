## Microblocks
Created by [PeterMathijssen](https://community.robotistan.com/profile/PeterMathijssen "PeterMathijssen")

The latest PicoBricks has a Raspberry Pi Pico W. That is why it has an IR sensor instead of a WiFi slot. To test your IR sensor with the remote you get with your Zero to Hero kit, you can use this script.

![allScripts397507](https://user-images.githubusercontent.com/112697142/218952968-8aead9bf-7e2f-4e6f-bbd5-50b11e9c99cf.png)

The broadcast block sends out the message content specified into the program context. All when received message blocks with the same message content will receive the message and act on it.

I added when received for the first 4 buttons only. But I guess you get the message how it works.

Have fun

##### You can access the Microblocks codes of the project by dragging the image to the Microblocks Run tab or clicking [here](https://microblocks.fun/run/microblocks.html#scripts=GP%20Scripts%0Adepends%20%27IR%20Remote%27%0A%0Ascript%20895%20160%20%7B%0AwhenStarted%0AattachIR%200%0Aforever%20%7B%0A%20%20%27IR%20code%27%20%3D%20%28receiveIR%29%0A%20%20sayIt%20%28%27%5Bdata%3Ajoin%5D%27%20%27Button%20%27%20%28at%20%28%27%5Bdata%3Afind%5D%27%20%28v%20%27IR%20code%27%29%20%28%27%5Bdata%3AmakeList%5D%27%2069%2070%2071%2068%2064%2067%207%2021%209%2022%2025%2013%2024%208%2028%2090%2082%29%29%20%28%27%5Bdata%3AmakeList%5D%27%201%202%203%204%205%206%207%208%209%20%27%2A%27%200%20%27%23%27%20%27Arrow%20Up%27%20%27Arrow%20Left%27%20%27OK%27%20%27Arrow%20Right%27%20%27Arrow%20Down%27%29%29%20%27%20Pressed%27%29%0A%20%20sendBroadcast%20%28v%20%27IR%20code%27%29%0A%7D%0A%7D%0A%0Ascript%20523%20469%20%7B%0AwhenBroadcastReceived%20%2769%27%0AsayIt%20%27Button%201%20pressed%27%0A%7D%0A%0Ascript%20713%20475%20%7B%0AwhenBroadcastReceived%20%2771%27%0AsayIt%20%27Button%203%20pressed%27%0A%7D%0A%0Ascript%20519%20560%20%7B%0AwhenBroadcastReceived%20%2770%27%0AsayIt%20%27Button%202%20pressed%27%0A%7D%0A%0Ascript%20714%20566%20%7B%0AwhenBroadcastReceived%20%2768%27%0AsayIt%20%27Button%204%20pressed%27%0A%7D%0A%0A "here").
