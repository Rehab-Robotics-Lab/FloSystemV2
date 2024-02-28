#!/usr/bin/env python
import PySimpleGUI as psg
import rospy
from std_msgs.msg import String
from flo_humanoid.msg import SetArmsJointPositions

def motorGUI():
    id1 = 10
    id2 = 11
    id3 = 12
    id4 = 13
    pub = rospy.Publisher("/set_joint_positions", SetJointPositions, queue_size=10)
    rospy.init_node('MotorGUI', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    layout = [
    [psg.Text('Flo V2 Motor Control Demo', enable_events=True,
    key='-TEXT-', font=('Arial Bold', 20),
    size=(50, 2), relief="raised", border_width=5,
    expand_x=True, justification='center')],
    [psg.Slider(range=(0, 1000), default_value=0,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor1')],
    [psg.Slider(range=(0, 1000), default_value=0,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor2')],
    [psg.Slider(range=(0, 1000), default_value=0,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor3')],
    [psg.Slider(range=(0, 1000), default_value=0,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor4')]
        ]
       
    window = psg.Window('Hello', layout, size=(715, 300))
    while not rospy.is_shutdown():
        event, values = window.read()
        print(event, values)
        if event == psg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Motor1' or event == 'Motor2' or event == 'Motor3' or event == 'Motor4':
            pub.publish(SetJointPositions(id1, id2, id3, id4, 'position', 'position', 'position', 'position', int(values['Motor1']), int(values['Motor2']), int(values['Motor3']), int(values['Motor4'])))
            rospy.loginfo("publishing to /set_joint_positions values: %s", values)
    window.close()
    rate.sleep()

if __name__ == '__main__':

    try:
        motorGUI()
    except rospy.ROSInterruptException:
        pass