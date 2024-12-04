

### Building Docker Images
- To build a Docker image for your FastAPI application, ensure you have a Dockerfile in the same directory as your `docker-compose.yml`. Then run:
  - **`docker-compose build`**

## Pushing Images to Docker Hub

### Creating a Docker Hub Account
- Visit [Docker Hub](https://hub.docker.com/) and sign up for an account.
- Once registered, you can create repositories to store your Docker images.

### Logging into Docker Hub from the Command Line
- **`docker login`**
- Enter your Docker Hub username and password.

### Tagging Your Docker Image
- **`docker tag local-image:tagname username/repository:tag`**
  - For example:
    - **`docker tag myfastapi:latest john/myfastapi:latest`**

### Pushing the Image
- **`docker push username/repository:tag`**
  - For example:
    - **`docker push john/myfastapi:latest`**

## Additional Tips

### Viewing Logs
- To view logs for troubleshooting or monitoring application behavior:
  - **`docker-compose logs -f`**
  - The `-f` flag tails the log output.

### Shutting Down
- To stop and remove all running containers:
  - **`docker-compose down`**

This guide is structured to provide clear, step-by-step instructions on how to interact with the Dockerized environment defined by your Docker Compose setup, ideal for educational purposes and ensuring students are well-equipped to manage their development environment effectively.
