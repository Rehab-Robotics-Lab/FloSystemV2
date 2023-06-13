# Flo-System-2
This is the master code repository for the second iteration of the Flo system. 

## Connecting to the Ohmni telepresence robot and running docker
1. Clone this repository using git clone https://github.com/Rehab-Robotics-Lab/Flo-System-2.git 

2. Download the private ssh key from penn box https://upenn.app.box.com/folder/206840565719; contact @anht-nguyen for access if necessary.
3. Verify that the IP addess matches RobotIP matches the wlan0/[IP] of the ohmni telepresence robot. 
4. Change the value of pKeyPath if ssh key is stored in a different location.
5. ./ohmniConnect.bash - will ssh into the Ohmni telepresence robot.
6. ./var/dockerhome/floSystem.bash - to start a docker container running the flo system 
