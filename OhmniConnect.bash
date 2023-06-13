#pKeyPath stores the path to the private key.
pKeyPath="~/.ssh/rrl_ohmnilabs_1"
#robotIP stores the local IP address of the robot.
robotIP=10.152.96.105
echo $robotIP
echo "ssh into root@$robotIP using private key $pKeyPath"
ssh -i $pKeyPath "root@$robotIP"
