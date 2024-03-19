docker build ./ -t --pull --no-cache ajyanand/motor_control_demo:latest
# --pull always attempts to pull a newer version of the base image
# --no-cache forces a rebuild of the image
# -t tag the image with the name ajyanand/motor_control_demo:latest