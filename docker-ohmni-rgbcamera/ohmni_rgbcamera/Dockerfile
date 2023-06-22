FROM ohmni_rgbcam:base

COPY launch/* /
COPY ros_launch.sh /
COPY ros_entrypoint.sh /

#Build an example
RUN mkdir -p root/catkin_ws/src
COPY example_draw_image root/catkin_ws/src/example_draw_image
RUN /bin/bash -c ' source /opt/ros/melodic/setup.bash; cd root/catkin_ws\
    ;catkin_make -DCATKIN_WHITELIST_PACKAGES="example_draw_image" -DCMAKE_BUILD_TYPE=Release'
 
#start core nodes
ENTRYPOINT ["./ros_entrypoint.sh"]
CMD ["bash"]

