#pKeyPath stores the path to the private key.
pKeyPath="~/.ssh/rrl_ohmnilabs_1"
#robotIP stores the local IP address of the robot.
echo Please enter the robot IP
read robotIP
echo "ssh into root@$robotIP using private key $pKeyPath"
ssh -i $pKeyPath "root@$robotIP"
