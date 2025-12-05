
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
 # Resultat calculatrice (addition)
 ![resultat](https://github.com/MohamedYenge/microservices-project/blob/main/Screenshot%20(693).png)
 -installer docker compose:
 ```bash
      sudo apt-get update
      sudo apt-get install docker-compose-plugin
      docker compose version
      docker compose up -d
```
 ![docker composes version](https://github.com/MohamedYenge/microservices-project/blob/main/Screenshot%20(684).png)
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



















