# abb_communication
communication library for abb robot control

## Installation
Clone repository to your computer <br>
In Rhino: python editor - options - tools: Add parent directory to paths. <br>
On the robot controller: Add tasks: 1. Sender, 2. Receiver, + per robot one motion task: T_ROBx 

## Use
To connect to robot: <br>
ping robot ip address from your computer to ensure it can connect <br>
From robot flex pendant start all three tasks <br>
From gh file: press "init" then "robot on" <br>
If connection succesful, the pendenant wil give you a message "ip address connected" <br>
Now you can send commands to the robot from your gh script <br>

