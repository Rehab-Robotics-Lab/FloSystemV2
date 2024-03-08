CLI commands to build from Dockerfile and run containers to test motors: 

docker build . -t "testmotor:Dockerfile"

docker run -it --privileged --device=/dev/ttyUSB0 --name testmotor_dockerfile testmotor:Dockerfile

docker start testmotor_dockerfile

docker exec -it --privileged testmotor_dockerfile bash

