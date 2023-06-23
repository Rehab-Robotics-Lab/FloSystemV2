#include "ohmnilabs_common/helper/visualization_helper.h"

visualization_msgs::Marker ohmnilabs::Vector3Marker(const std::string frame_id,
                                         const std::string ns,
                                         const double x, const double y, const double z,
                                         const char color)
{
  visualization_msgs::Marker marker;
  marker.header.frame_id = frame_id;
  marker.header.stamp = ros::Time::now();
  marker.ns = ns;
  marker.id = 0;
  marker.type = visualization_msgs::Marker::ARROW;
  marker.action = visualization_msgs::Marker::ADD;
  geometry_msgs::Point p;
  //start point default is the origin
  p.x = 0.0;
  p.y = 0.0;
  p.z = 0.0;
  marker.points.push_back(p);
  //end point defined by the vector3
  p.x = x;
  p.y = y;
  p.z = z;
  marker.points.push_back(p);

  //set shaft diameter
  marker.scale.x = 0.01;
  //set head diameter
  marker.scale.y = 0.02;
  //set length
  marker.scale.z = 0.3;

  // Set the color -- be sure to set alpha to something non-zero!
  marker.color.a = 1.0;
  switch (color) {
  case 'r':
    marker.color.r = 1.0f;
    marker.color.g = 0.0f;
    marker.color.b = 0.0f;
    break;
  case 'g':
    marker.color.r = 0.0f;
    marker.color.g = 1.0f;
    marker.color.b = 0.0f;
    break;
  case 'b':
    marker.color.r = 0.0f;
    marker.color.g = 0.0f;
    marker.color.b = 1.0f;
    break;
  default:
    marker.color.r = 0.0f;
    marker.color.g = 0.0f;
    marker.color.b = 1.0f;
    break;
  }

  marker.lifetime = ros::Duration();

  return marker;
}

visualization_msgs::Marker ohmnilabs::Point3Marker(const std::string frame_id,
                                         const std::string ns,
                                         const double x, const double y, const double z,
                                         const char color)
{
  visualization_msgs::Marker marker;
  marker.header.frame_id = frame_id;
  marker.header.stamp = ros::Time::now();
  marker.ns = ns;
  marker.id = 0;
  marker.type = visualization_msgs::Marker::SPHERE;
  marker.action = visualization_msgs::Marker::ADD;
  geometry_msgs::Point p;

  marker.pose.position.x = x;
  marker.pose.position.y = y;
  marker.pose.position.z = z;

  //set
  marker.scale.x = 0.05;
  //set
  marker.scale.y = 0.05;
  //set
  marker.scale.z = 0.05;

  // Set the color -- be sure to set alpha to something non-zero!
  marker.color.a = 1.0;
  switch (color) {
  case 'r':
    marker.color.r = 1.0f;
    marker.color.g = 0.0f;
    marker.color.b = 0.0f;
    break;
  case 'g':
    marker.color.r = 0.0f;
    marker.color.g = 1.0f;
    marker.color.b = 0.0f;
    break;
  case 'b':
    marker.color.r = 0.0f;
    marker.color.g = 0.0f;
    marker.color.b = 1.0f;
    break;
  default:
    marker.color.r = 0.0f;
    marker.color.g = 0.0f;
    marker.color.b = 1.0f;
    break;
  }

  marker.lifetime = ros::Duration();

  return marker;
}
