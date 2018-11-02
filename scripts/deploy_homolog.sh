docker build -t tayh/api_cars:homolog .
docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
docker push tayh/api_cars:homolog