docker build -t tayh/api_notifications:homolog .
docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
docker push tayh/api_notifications:homolog