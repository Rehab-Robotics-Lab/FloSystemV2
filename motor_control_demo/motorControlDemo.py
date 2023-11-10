import PySimpleGUI as psg
import rospy
from std_msgs.msg import String
from flo_humanoid.msg import SetJointPositions

def motorGUI():
    pub = rospy.Publisher('MotorCmds', SetJointPositions, queue_size=10)
    rospy.init_node('MotorGUI', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    layout = [
    [psg.Text('Flo V2 Motor Control Demo', enable_events=True,
    key='-TEXT-', font=('Arial Bold', 20),
    size=(50, 2), relief="raised", border_width=5,
    expand_x=True, justification='center')],

    [psg.Slider(range=(0, 1000), default_value=0,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor1')]
    [psg.Slider(range=(0, 1000), default_value=0,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor2')]
    [psg.Slider(range=(0, 1000), default_value=0,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor3')]
    [psg.Slider(range=(0, 1000), default_value=0,
    expand_x=True, enable_events=True,
    orientation='horizontal', key='Motor4')]
        ]
       
    window = psg.Window('Hello', layout, size=(715, 150))
    while True:
    event, values = window.read()
    print(event, values)
    if event == psg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-SL-':
        window['-TEXT-'].update(font=('Arial Bold', int(values['-SL-'])))
    window.close()
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':

    try:
        motorGUI()
    except rospy.ROSInterruptException:
        pass