# Flo-System-2
This is the master code repository for the second iteration of the Flo system. 
It contains code used for the control of the humanoid robot, the control of the mobile telepresence platform and the autonomous navigation stack.

It contains repositories for the following components:
1. Control of the joints of second version of the flo humanoid
2. Control of the ohmni telepresence base
3. Camera and sensor data collection
4. Central systems to coordinate the above components 
## License:

MIT License. Have fun!

Copyright 2021 University of Pennsylvania, Rehabilitation Robotics Lab

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
## Connecting to the Ohmni telepresence robot and running docker
1. Clone this repository using git clone https://github.com/Rehab-Robotics-Lab/Flo-System-2.git 
2. Download the private ssh key from penn box https://upenn.app.box.com/folder/206840565719; contact @anht-nguyen for access if necessary. 
3. ./ohmniConnect.bash - will ssh into the Ohmni telepresence robot (must be on the same local network)
4. ./var/dockerhome/floSystem.bash - to start a docker container running the flo system (will run in detached mode)
5. docker attach flo_system
