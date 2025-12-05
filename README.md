
#  Projet Microservices avec Kubernetes & Jenkins (Local)

##  Architecture du projet
microservices-project/
│
├── calculatrice/
│   ├── app.py  // using flask
│   ├── requirements.txt
│   └── Dockerfile
│
├── statistiques/
│   ├── app.py    //using flask
│   ├── requirements.txt
│   └── Dockerfile
│
├── k8s/
│   ├── calculatrice-deployment.yaml
│   └── statistiques-deployment.yaml
│
├── Jenkinsfile          # Pipeline CI/CD local
└── README.md            # Documentation complète

###  **Flux d’architecture**

[Jenkins Pipeline]
|
v
[Docker Build] --> [Images locales dans Minikube]
|
v
[Kubernetes Cluster (Minikube)]
|
├── Deployment: calculatrice + Service
└── Deployment: statistiques + Service


##  **Étapes pour exécuter le projet**
1- preparer l'environement:
    nous avons travaillee sur ubuntu VM :

   -installer docker:
```bash
    # Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

# install docker
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
 ![docker version](https://github.com/MohamedYenge/microservices-project/blob/main/Screenshot%20(716).png)
 -installer docker compose:
 ```bash
      sudo apt-get update
      sudo apt-get install docker-compose-plugin
      docker compose version
      docker compose up -d
```
 ![docker composes version](https://github.com/MohamedYenge/microservices-project/blob/main/Screenshot%20(684).png)

# install Kubernets
```bash
#  instal minikube:
    sudo apt update
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
    sudo dpkg -i minikube_latest_amd64.deb
    curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/
# Disable Swap:
    minikube start
    sudo swapoff -a
    sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

    # Add Kubernetes APT Repository:
    
        sudo apt update
        sudo apt install -y apt-transport-https ca-certificates curl
        curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
        echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
        sudo apt update

   # Install Kubeadm, Kubelet, and Kubectl:


        sudo apt install -y kubelet kubeadm kubectl
        sudo apt-mark hold kubelet kubeadm kubectl
   # Initialize Control Plane Node.

    sudo kubeadm init --pod-network-cidr=<your_pod_network_cidr> **// (Replace <your_pod_network_cidr> with a suitable CIDR, e.g., 10.244.0.0/16 for Flannel.) Configure Kubectl on Control Plane.**

# Install Network Plugin (on Control Plane).   Choose a network plugin (e.g., Flannel, Calico) and follow its installation instructions. For Flannel:
    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
```bash
# Step 1: Update System & Install Java

sudo apt update
sudo apt install openjdk-17-jdk # Or openjdk-11-jdk

# Step 2: Add Jenkins Repository
# Import GPG key
  curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
     /usr/share/keyrings/jenkins-keyring.asc > /dev/null

# Add Jenkins repository to sources list
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
# Step 3: Install Jenkins

sudo apt update
sudo apt install jenkins -y

# Step 4: Start and Enable Jenkins Service
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo systemctl status jenkins # Verify it's running (look for 'active (running)') [7, 11]

# Step 5: Access Jenkins in Browser & Unlock
Open your browser and navigate to http://your_server_ip_or_domain:8080.

# Get the initial admin password:
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
###  **Construire les images Docker localement**
Assurez-vous que Minikube est démarré :
```bash
minikube start --driver=docker --memory=3072 --cpus=2
eval $(minikube docker-env)

docker build -t calculatrice:latest ./calculatrice
docker build -t statistiques:latest ./statistiques
## Docker composer
docker compose up -d
docker compose down
```
##  Déployer sur Kubernetes
```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
```
![k8s apply](https://github.com/MohamedYenge/microservices-project/blob/main/Screenshot%20(694).png)
# resultat
nous avons utilisee RESTED afin que tester les endpoinsts q'on a cree : par examples dans la figure ci-dessous ,nous avons teste l'endpoint /add
en passsant le parametres  ,il nous donne le resulat exact.
![resultat](https://github.com/MohamedYenge/microservices-project/blob/main/Screenshot%20(693).png)
## Configurer Jenkins (Pipeline local)
```bash
## Installer Jenkins et les plugins :

Pipeline
Docker Pipeline
Kubernetes CLI

c
Créer un Pipeline Job et utiliser le Jenkinsfile :

pipeline {
    agent any

    stages {
        stage('Check Minikube') {
            steps {
                sh '''
                if ! minikube status | grep -q "Running"; then
                    echo "Minikube n'est pas démarré. Démarrage avec driver Docker..."
                    minikube start --driver=docker --memory=3072 --cpus=2
                fi
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                eval $(minikube docker-env)
                docker build -t calculatrice:latest ./calculatrice
                docker build -t statistiques:latest ./statistiques
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f k8s/
                kubectl get pods
                kubectl get svc
                '''
            }
        }
    }
}
```
# CI/DI avec Jenkis
![jenkis script](https://github.com/MohamedYenge/microservices-project/blob/main/Screenshot%20(697).png)
![Pods Monitoring](https://github.com/MohamedYenge/microservices-project/blob/main/ci-cd.png)

# monotoring
  j'ai probleme d'utiliser grafana et promeutheus ,donc je choisis minikube dasbord
![Grafana Dashboard](https://github.com/MohamedYenge/microservices-project/blob/main/dashbord.png)























