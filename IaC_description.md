# Infrastructure as Code (IaC) Process


### **1. Installing and Configuring Docker**
1. Update the system and install Docker:
   ```bash
   sudo dnf update -y
   sudo dnf install docker -y
    ```
2. Start and enable the Docker service:
   ```bash
    sudo systemctl start docker
    sudo systemctl enable docker

    ```
3. Add the EC2 user to the Docker group for permission management
   ```bash
   sudo usermod -a -G docker ec2-user
    ```

### **2.  Setting Up AWS Credentials**
1. Create the `.aws` directory and set up credentials and configuration files:
   ```bash
   mkdir -p ~/.aws
    echo "[default]" > ~/.aws/credentials
    echo "aws_access_key_id=${AWS_ACCESS_KEY_ID}" >> ~/.aws/credentials
    echo "aws_secret_access_key=${AWS_SECRET_ACCESS_KEY}" >> ~/.aws/credentials
    echo "[default]" > ~/.aws/config
    echo "region=${AWS_REGION}" >> ~/.aws/config
    ```
2. Start and enable the Docker service:
- **AWS_ACCESS_KEY_ID:** Your AWS access key ID.  
- **AWS_SECRET_ACCESS_KEY:** Your AWS secret access key.  
- **AWS_REGION:** The AWS region hosting your resources.  


### **3. Pulling the Docker Image from ECR**
1. Authenticate Docker with ECR using AWS CLI:
   ```bash
   aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
    ```
2. Remove unused Docker images to free space:
   ```bash
    docker image prune -f
    ```
3. Pull the application Docker image from ECR:
   ```bash
   docker pull ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
    ```
    

### **4. Running the Containerized Application**
1. Stop and remove any existing containers to ensure a clean start:
   ```bash
   sudo docker stop weather_app || true
    sudo docker rm weather_app || true
    ```
2. Run the application container:
   ```bash
    sudo docker run -d -p 9999:9999 --name weather_app \
  -e WEATHER_API_ACCESS_TOKEN=${WEATHER_API_ACCESS_TOKEN} \
  ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
    ```


### **5. Verifying Environment Variables**
To ensure the container is properly configured:
   ```bash
   sudo docker exec weather_app sh -c 'echo $AWS_ACCESS_KEY_ID && echo $AWS_SECRET_ACCESS_KEY && echo $AWS_REGION'
    ```

![alt text](images/Deployment.png)