//Include ROS
#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>

//Global parameters
static image_transport::ImageTransport* it;
static image_transport::Publisher image_pub_;

void imageRgbCallback(const sensor_msgs::ImageConstPtr& msg)
{
  ROS_INFO("image callback, size: %d x %d, encoding %s",msg->width,msg->height, msg->encoding.c_str());

  // convert OpenCV image format
  cv_bridge::CvImagePtr cv_ptr;
  try {
    cv_ptr = cv_bridge::toCvCopy(msg, "rgb8");
  } catch (cv_bridge::Exception& e) {
    ROS_ERROR("cv_bridge exception: %s", e.what());
    return;
  }

  // Do you amazing things
  cv::circle(cv_ptr->image, cv::Point(msg->width/2,msg->height/2), 20, CV_RGB(255,0,255), 5);

  // publish the result to orther nodes
  image_pub_.publish(cv_ptr->toImageMsg());
}

int  main (int argc, char** argv)
{
  ros::init(argc, argv, "example_draw_image");
  ros::NodeHandle nh;
  it = new image_transport::ImageTransport(nh);

  image_transport::TransportHints hints("raw", ros::TransportHints(), nh);
  image_transport::Subscriber cam_rgb_sub = it -> subscribe("input_image", 10, &imageRgbCallback, hints);
  image_pub_ = it->advertise("output_image", 1);

  ROS_INFO("Start example_draw_image node");
  ros::spin();
  return 0;
}
