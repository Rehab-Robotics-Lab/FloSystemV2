# `flo_humanoid`

Hardware-side ROS package for the FLO V2 Dynamixel arms.

This package is responsible for:

- talking to the Dynamixel bus
- exposing left and right `FollowJointTrajectory` action servers
- publishing hardware `/joint_states`
- converting between raw motor encoder values and ROS joint angles
- loading motor-specific configuration from YAML

## Main Files

- [launch/read_write_arms.launch](/c:/Users/robor/git/FloSystemV2/flo_humanoid/launch/read_write_arms.launch): loads motor config and starts `read_write_arms_node`
- [src/readWriteArms.cpp](/c:/Users/robor/git/FloSystemV2/flo_humanoid/src/readWriteArms.cpp): main hardware controller
- [config/dynamixel_ids.yaml](/c:/Users/robor/git/FloSystemV2/flo_humanoid/config/dynamixel_ids.yaml): ROS joint name to Dynamixel ID mapping
- [config/dynamixel_joint_signs.yaml](/c:/Users/robor/git/FloSystemV2/flo_humanoid/config/dynamixel_joint_signs.yaml): joint direction multipliers
- [config/dynamixel_offsets.yaml](/c:/Users/robor/git/FloSystemV2/flo_humanoid/config/dynamixel_offsets.yaml): software joint-angle offsets in degrees
- [config/dynamixel_homing_offsets.yaml](/c:/Users/robor/git/FloSystemV2/flo_humanoid/config/dynamixel_homing_offsets.yaml): hardware homing offsets in Dynamixel ticks
- [config/joints](/c:/Users/robor/git/FloSystemV2/flo_humanoid/config/joints): calibration notes and legacy neutral/min/max references

## Launch

Hardware-only bringup:

```bash
roslaunch flo_humanoid dual_arm_hardware.launch
```

Direct hardware node launch without `robot_state_publisher` wrapper:

```bash
roslaunch flo_humanoid read_write_arms.launch
```

If another node already owns `/joint_states`, disable the hardware publisher:

```bash
roslaunch flo_humanoid dual_arm_hardware.launch publish_joint_states:=false
```

## Config Files

### `dynamixel_ids.yaml`

This file maps ROS joint names like `l2` and `r4` to Dynamixel IDs on the bus.

Example:

```yaml
joint_id_map:
  l1: 111
  l2: 112
  ...
```

Use this file when:

- a motor ID changes
- a motor is replaced
- the physical wiring is the same but the ID assignment on the bus changes

### `dynamixel_joint_signs.yaml`

This file defines the direction relationship between positive ROS joint motion and positive motor rotation.

- `1`: ROS positive motion matches the motor direction
- `-1`: ROS positive motion must be inverted before commanding the motor

Example:

```yaml
joint_signs:
  l1: 1
  l2: 1
  l4: -1
```

Use this file when:

- the real robot moves opposite to the intended ROS joint direction
- a motor is reassembled or mirrored mechanically
- one joint on the left arm behaves as the opposite of the matching right-arm joint

### `dynamixel_offsets.yaml`

This file contains software-side angle offsets in degrees.

These values are applied in the conversion between raw encoder position and ROS joint angle. They are not written into the motor EEPROM.

Current convention:

- all joints should default to `180`
- this keeps the interpreted software-side angle range roughly in `0..360` degrees
- starting/home pose should be calibrated with hardware homing offsets, not by moving software offsets away from `180`

Use this file when:

- you are preserving the standard `180` degree software reference for all joints
- you want the software-side angle convention to stay consistent across the robot

Avoid using this file to:

- fix a bad home pose
- compensate for horn mounting error
- compensate for motor EEPROM zero error

### `dynamixel_homing_offsets.yaml`

This file contains hardware-side homing offsets in raw Dynamixel ticks.

These values are written by `read_write_arms_node` to Dynamixel control table address `20` during startup while torque is off.

Example:

```yaml
homing_offsets:
  l1: 0
  l2: 0
  ...
```

Use this file when:

- the motor's internal zero needs to move
- you want the actuator's reported present position to shift at the hardware level
- you are doing a deeper calibration after reassembly or horn repositioning
- you want the robot's physical starting/home pose to read as `180` degrees on every joint while keeping `dynamixel_offsets.yaml` fixed at `180`

Important:

- `dynamixel_homing_offsets.yaml` is in raw ticks
- `dynamixel_offsets.yaml` is in degrees
- they are not interchangeable

## Recommended Calibration Workflow

Calibrate in this order:

1. Confirm each physical motor ID.
2. Confirm each joint direction sign.
3. Set hardware homing offsets so the starting/home pose reads as `180` degrees on every joint.
4. Keep software angle offsets at `180` unless you have a deliberate reason to change the software reference convention.

This order keeps the variables separated and makes debugging much easier.

## Dynamixel Wizard

Use the official ROBOTIS DYNAMIXEL Wizard 2.0:

- e-Manual and download page: https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/
- ROBOTIS software overview: https://www.robotis.us/dynamixel-software-solutions/

Wizard is the best tool here for:

- scanning motors on the bus
- changing IDs
- checking current position values
- checking present direction of motion
- writing EEPROM values like homing offset
- testing motors one at a time before launching ROS

## Calibrating IDs

Goal: make sure each physical motor matches the expected ROS joint name.

Workflow:

1. Connect one motor at a time when possible.
2. Open DYNAMIXEL Wizard 2.0 and scan the bus.
3. Verify the detected ID.
4. Change the ID in Wizard if needed.
5. Update [dynamixel_ids.yaml](/c:/Users/robor/git/FloSystemV2/flo_humanoid/config/dynamixel_ids.yaml) to match the final bus IDs.
6. Re-launch the hardware node and confirm startup logs mention the expected ID for each joint.

Tip:

- If multiple motors share an ID accidentally, use Wizard's ID inspection workflow before trying ROS bringup.

## Calibrating Joint Signs

Goal: make sure a positive ROS joint command moves the real joint in the intended positive direction.

Workflow:

1. Start with known-good IDs.
2. In Wizard, jog the motor slightly and observe the physical joint motion.
3. Compare that motion with the intended ROS joint direction for that joint.
4. Set the joint to `1` or `-1` in [dynamixel_joint_signs.yaml](/c:/Users/robor/git/FloSystemV2/flo_humanoid/config/dynamixel_joint_signs.yaml).
5. Rebuild and relaunch the hardware node.
6. Test again with a very small motion before running full actions.

Rule of thumb:

- if the robot consistently moves opposite to the commanded joint angle, fix `joint_signs` first
- do not try to fix a direction problem with homing offsets

## Calibrating Homing Offsets

Goal: align the motor's internal zero at the hardware level so the robot's intended starting/home pose reads as `180` degrees for every joint.

Workflow:

1. Put the mechanism in the intended starting/home pose.
2. Keep [dynamixel_offsets.yaml](/c:/Users/robor/git/FloSystemV2/flo_humanoid/config/dynamixel_offsets.yaml) at `180` for every joint.
3. In Wizard, inspect the current present position / homing-related values for that motor.
4. Compute the homing offset needed so this home pose corresponds to `180` degrees.
5. Put that tick value into [dynamixel_homing_offsets.yaml](/c:/Users/robor/git/FloSystemV2/flo_humanoid/config/dynamixel_homing_offsets.yaml).
6. Restart `read_write_arms_node` so it writes the configured homing offsets at startup.
7. Re-check the reported present position and physical alignment.

Target outcome:

- when the robot is physically in its intended starting/home pose
- each joint should report approximately `180` degrees in the software conversion path
- the software offset file should still remain at `180`

Guidance:

- change one motor at a time
- keep a record of old and new values
- use small, deliberate changes
- verify that the motor model actually supports the expected homing-offset behavior in Wizard before assuming the write succeeded

## Calibrating Software Angle Offsets

Goal: preserve a consistent software convention, not tune home pose.

Default rule:

- keep every value in [dynamixel_offsets.yaml](/c:/Users/robor/git/FloSystemV2/flo_humanoid/config/dynamixel_offsets.yaml) at `180`

Only change software angle offsets if:

- you intentionally want a different software reference convention
- you are making a controlled, system-wide conversion change and understand the downstream impact

Do not use software angle offsets for:

- home-pose calibration
- horn alignment correction
- EEPROM zero correction

In normal operation, use `dynamixel_homing_offsets.yaml` for home-pose calibration instead.

## Practical Troubleshooting

If a joint does not move:

- verify the motor appears in Wizard
- verify the ID matches `dynamixel_ids.yaml`
- verify torque is enabled
- check startup logs from `read_write_arms_node`

If a joint moves in reverse:

- check `dynamixel_joint_signs.yaml`
- do not change homing offsets first

If `/joint_states` looks biased but direction is correct:

- first check whether home pose was calibrated with `dynamixel_homing_offsets.yaml`
- keep `dynamixel_offsets.yaml` at `180` unless you explicitly intend to change the software reference convention

If the motor's raw zero is wrong even before ROS conversion:

- check `dynamixel_homing_offsets.yaml`

If a config change has no effect:

- rebuild the catkin workspace
- relaunch the node
- remember that `read_write_arms_node` is C++, so source changes need rebuilds

## Rebuild

Inside the container or workspace:

```bash
cd /catkin_ws
source /opt/ros/noetic/setup.bash
catkin_make
source /catkin_ws/devel/setup.bash
```

Then restart the hardware launch.
