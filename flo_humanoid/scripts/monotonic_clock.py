#!/usr/bin/env python3

import time

import rospy
from rosgraph_msgs.msg import Clock


def main():
    rospy.init_node("monotonic_clock_publisher")

    publish_rate_hz = float(rospy.get_param("~publish_rate_hz", 100.0))
    start_epoch_sec = float(rospy.get_param("~start_epoch_sec", 0.0))

    if publish_rate_hz <= 0.0:
        raise ValueError("~publish_rate_hz must be > 0")

    publisher = rospy.Publisher("/clock", Clock, queue_size=10)
    period_sec = 1.0 / publish_rate_hz
    monotonic_start_ns = time.monotonic_ns()

    while not rospy.is_shutdown():
        elapsed_sec = (time.monotonic_ns() - monotonic_start_ns) / 1_000_000_000.0
        clock_msg = Clock()
        clock_msg.clock = rospy.Time.from_sec(start_epoch_sec + elapsed_sec)
        publisher.publish(clock_msg)
        time.sleep(period_sec)


if __name__ == "__main__":
    main()
