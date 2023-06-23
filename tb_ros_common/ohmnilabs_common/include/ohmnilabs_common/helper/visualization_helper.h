#ifndef VISUALIZATION_HELPER_H
#define VISUALIZATION_HELPER_H

//Include ROS
#include <ros/ros.h>
#include <visualization_msgs/Marker.h>
#include <geometry_msgs/Point.h>

namespace ohmnilabs {
visualization_msgs::Marker Vector3Marker (const std::string frame_id,
                                          const std::string ns,
                                          const double x,
                                          const double y,
                                          const double z,
                                          const char color);

visualization_msgs::Marker Point3Marker(const std::string frame_id,
                                                  const std::string ns,
                                                  const double x, const double y, const double z,
                                                  const char color);

}
#endif // VISUALIZATION_HELPER_H
