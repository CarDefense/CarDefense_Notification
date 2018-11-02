docker build -t tayh/api_cars:prod .
docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
docker push tayh/api_cars:prod