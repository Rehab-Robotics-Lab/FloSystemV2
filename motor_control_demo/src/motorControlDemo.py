#!/usr/bin/env python3
import PySimpleGUI as psg
import rospy
from std_msgs.msg import String
from flo_humanoid.msg import SetJointPositions

def motorGUI():
    id1 = 111
    id2 = 112
    id3 = 121
    id4 = 122
    pub = rospy.Publisher("/set_joint_positions", SetJointPositions, queue_size=10)
    rospy.init_node('motor_control_demo_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    layout = [
    [psg.Text('Flo V2 Motor Control Demo', enable_events=True,
    key='-TEXT-', font=('Arial Bold', 20),
    size=(100, 2), relief="raised", border_width=5,
    expand_x=True, justification='center')],
    [psg.Slider(range=(0, 1500), default_value=500,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor1')],
    [psg.Slider(range=(2500, 3500), default_value=3000,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor2')],
    [psg.Slider(range=(600,1200), default_value=1000,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor3')],
    [psg.Slider(range=(3100, 3900), default_value=3800,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor4')]
        ]
       
    window = psg.Window('Flo V2 Unilateral Demo', layout, size=(715, 300))
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