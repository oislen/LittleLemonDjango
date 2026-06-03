:: set docker settings
SET DOCKER_USER=oislen
SET DOCKER_REPO=littlelemondjango
SET DOCKER_TAG=latest
SET DOCKER_IMAGE=%DOCKER_USER%/%DOCKER_REPO%:%DOCKER_TAG%
SET DOCKER_CONTAINER_NAME=lld

:: remove existing docker containers and images
call docker image rm -f %DOCKER_IMAGE%
:: clear docker build cache
call docker builder prune -f

:: build docker image
call docker build --no-cache -t %DOCKER_IMAGE% .
::call docker build -t %DOCKER_IMAGE% .

:: run docker container
SET UBUNTU_DIR=/home/ubuntu
call docker network create littlelemon
:: call docker run --name %DOCKER_CONTAINER_NAME% --net littlelemon --publish 8000:8000 --memory 6GB --shm-size=512m --rm %DOCKER_IMAGE%
:: call docker run -it --entrypoint sh --name %DOCKER_CONTAINER_NAME% --net littlelemon --publish 8000:8000 --memory 6GB --shm-size=512m --rm %DOCKER_IMAGE%

:: useful docker commands
:: docker images
:: docker ps -a
:: docker exec -it {container_hash} /bin/bash
:: docker stop {container_hash}
:: docker start -ai {container_hash}
:: docker rm {container_hash}
:: docker image rm {docker_image}
:: docker push {docker_image}