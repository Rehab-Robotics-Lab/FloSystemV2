#!/bin/bash

#pKeyPath stores the path to the private key.
pKeyPath="~/.ssh/rrl_ohmnilabs_1"
#robotIP stores the local IP address of the robot
read -p 'robot IP: ' robotIP
read -p 'Would you like to enter custom path to private key?(yes/no) ' cusPath
if [ $cusPath = "yes" ]; then
    read -p 'Private Key: ' pKeyPath
fi    
echo "ssh into root@$robotIP using private key at $pKeyPath"
ssh -i $pKeyPath "root@$robotIP"