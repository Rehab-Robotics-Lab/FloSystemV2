#!/bin/bash
IMAGE_NAME="ohmni_rgbcam"
IMAGE_TAG="launch"
if [ "$1" == "c" ]
then        
        USE_CACHE=1
fi      

if [ $USE_CACHE ]
then
    echo "build with cache"
    sudo docker build --tag $IMAGE_NAME:$IMAGE_TAG .
else
    echo "build without cache"
    sudo docker build --no-cache --tag $IMAGE_NAME:$IMAGE_TAG .
fi