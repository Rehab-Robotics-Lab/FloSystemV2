#!/usr/bin/env python
import PySimpleGUI as psg
import rospy
from std_msgs.msg import String
from flo_humanoid.msg import SetArmsJointPositions

def biMotorGUI():
    id1 = 111
    id2 = 112
    id3 = 121
    id4 = 122
    id5 = 211
    id6 = 212
    id7 = 221
    id8 = 222
    pub = rospy.Publisher("/set_arms_joint_positions", SetArmsJointPositions, queue_size=10)
    rospy.init_node('BiMotorGUI', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    layout = [
    [psg.Text('Flo V2 Bilateral Motor Control Demo', enable_events=True,
    key='-TEXT-', font=('Arial Bold', 20),
    size=(50, 2), relief="raised", border_width=5,
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
    orientation='horizontal', key='Motor4')],
    [psg.Slider(range=(2000, 3900), default_value=3000,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor5')],
    [psg.Slider(range=(3050, 3900), default_value=3100,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor6')],
    [psg.Slider(range=(800, 2000), default_value=1000,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor7')],
    [psg.Slider(range=(3050, 3900), default_value=3100,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor8')]
        ]
    window = psg.Window('BiMotorControl', layout, size=(1000, 1000))
    while not rospy.is_shutdown():
        event, values = window.read()
        print(event, values)
        if event == psg.WIN_CLOSED or event == 'Exit':
            break
        if (event == 'Motor1' or event == 'Motor2' or event == 'Motor3' or event == 'Motor4' 
            or event == 'Motor5' or event == 'Motor6' or event == 'Motor7' or event == 'Motor8'):
            pub.publish(SetArmsJointPositions(id1, id2, id3, id4, id5, id6, id7,id8, 
                                              'position', 'position', 'position', 'position','position', 'position', 'position', 'position',
                                                int(values['Motor1']), int(values['Motor2']), int(values['Motor3']), int(values['Motor4']),
                                                    int(values['Motor5']), int(values['Motor6']), int(values['Motor7']), int(values['Motor8'])))
            rospy.loginfo("publishing to /set_arms_joint_positions values: %s", values)
    window.close()
    rate.sleep()

if __name__ == '__main__':

    try:
        biMotorGUI()
    except rospy.ROSInterruptException:
        pass