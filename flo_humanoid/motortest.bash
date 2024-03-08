# #LEDs ON
# rostopic pub -1 /set_joint_positions flo_humanoid/SetJointPositions "{id1: 10, id2: 11, id3: 12, id4: 13,  item1: 'LED', item2: 'LED', item3: 'LED', item4: 'LED', value1: 1, value2: 1, value3: 1, value4: 1}"
# #LEDs OFF
# rostopic pub -1 /set_joint_positions flo_humanoid/SetJointPositions "{id1: 10, id2: 11, id3: 12, id4: 13,  item1: 'LED', item2: 'LED', item3: 'LED', item4: 'LED', value1: 0, value2: 0, value3: 0, value4: 0}"

# rostopic pub -1 /set_joint_positions flo_humanoid/SetJointPositions "{id1: 10, id2: 11, id3: 12, id4: 13,  item1: 'position', item2: 'position', item3: 'position', item4: 'position', value1: 0, value2: 0, value3: 0, value4: 0}"
rostopic pub -1 /set_joint_positions flo_humanoid/SetJointPositions "{id1: 111, id2: 112, id3: 121, id4: 122,  item1: 'position', item2: 'position', item3: 'position', item4: 'position', value1: 0, value2: 0, value3: 0, value4: 0}"
rostopic pub -1 /set_joint_positions flo_humanoid/SetJointPositions "{id1: 111, id2: 112, id3: 121, id4: 122,  item1: 'position', item2: 'position', item3: 'position', item4: 'position', value1: 1000, value2: 0, value3: 0, value4: 0}"
rostopic pub -1 /set_joint_positions flo_humanoid/SetJointPositions "{id1: 111, id2: 112, id3: 121, id4: 122,  item1: 'position', item2: 'position', item3: 'position', item4: 'position', value1: 1000, value2: 1000, value3: 0, value4: 0}"
rostopic pub -1 /set_joint_positions flo_humanoid/SetJointPositions "{id1: 111, id2: 112, id3: 121, id4: 122,  item1: 'position', item2: 'position', item3: 'position', item4: 'position', value1: 1000, value2: 1000, value3: 1000, value4: 0}"
rostopic pub -1 /set_joint_positions flo_humanoid/SetJointPositions "{id1: 111, id2: 112, id3: 121, id4: 122,  item1: 'position', item2: 'position', item3: 'position', item4: 'position', value1: 1000, value2: 1000, value3: 1000, value4: 1000}"

# rostopic pub -1 /set_joint_positions flo_humanoid/SetJointPositions "{id1: 121, id2: 122,  item1: 'position', item2: 'position', value1: 100, value2: 150}"
# rostopic pub -1 /set_joint_positions flo_humanoid/SetJointPositions "{id1: 121, id2: 122,  item1: 'position', item2: 'position', value1: 0, value2: 150}"
# rostopic pub -1 /set_joint_positions flo_humanoid/SetJointPositions "{id1: 121, id2: 122,  item1: 'position', item2: 'position', value1: 0, value2: 0}"
# rostopic pub -1 /set_joint_positions flo_humanoid/SetJointPositions "{id1: 121, id2: 122,  item1: 'position', item2: 'position', value1: 100, value2: 150}"