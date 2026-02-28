#!/bin/bash
set -e  # exit on error

# Update system
sudo apt update -y

# -----------------
# Install Java
# -----------------
sudo apt install -y fontconfig openjdk-21-jre

# -----------------
# Install Jenkins
# -----------------
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y jenkins
sudo systemctl enable jenkins
sudo systemctl start jenkins

# -----------------
# Install Docker
# -----------------
sudo apt install -y docker.io
sudo usermod -aG docker jenkins
sudo usermod -aG docker ubuntu
sudo systemctl enable docker
sudo systemctl restart docker

# Wait for Docker to be fully ready
echo "Waiting for Docker daemon to start..."
timeout=30
while ! docker info > /dev/null 2>&1; do
    timeout=$((timeout - 1))
    if [ $timeout -eq 0 ]; then
        echo "ERROR: Docker failed to start"
        exit 1
    fi
    sleep 2
done
echo "Docker is ready!"

# -----------------
# Run SonarQube Container
# -----------------
docker run -d --name sonar -p 9000:9000 sonarqube:lts-community

# -----------------
# Install AWS CLI
# -----------------
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install -y unzip
unzip awscliv2.zip
sudo ./aws/install
rm -rf awscliv2.zip aws/

# -----------------
# Install Kubectl
# -----------------
curl -LO "https://dl.k8s.io/release/v1.28.4/bin/linux/amd64/kubectl"
sudo chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# -----------------
# Install eksctl
# -----------------
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# -----------------
# Install Terraform
# -----------------
# unzip is already installed from AWS CLI section
wget https://releases.hashicorp.com/terraform/1.13.2/terraform_1.13.2_linux_amd64.zip
unzip terraform_1.13.2_linux_amd64.zip
sudo mv terraform /usr/local/bin/
sudo chmod +x /usr/local/bin/terraform

# -----------------
# Install Trivy
# -----------------
sudo apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt update -y
sudo apt install -y trivy

# -----------------
# Install Helm
# -----------------
sudo snap install helm --classic

echo "All installations completed!"



