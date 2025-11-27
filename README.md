
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

###  **Construire les images Docker localement**
Assurez-vous que Minikube est démarré :
```bash
minikube start --driver=docker --memory=3072 --cpus=2
eval $(minikube docker-env)

docker build -t calculatrice:latest ./calculatrice
docker build -t statistiques:latest ./statistiques

##  Déployer sur Kubernetes

kubectl apply -f k8s/
kubectl get pods
kubectl get svc

## Configurer Jenkins (Pipeline local)

## Installer Jenkins et les plugins :

Pipeline
Docker Pipeline
Kubernetes CLI


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


<img src="https://github.com/user-attachments/assets/4875401b-6eb8-42d5-8851-5a8d5a310fa9" alt="Pods monitoring Running" width="100%"/>

### 2. Interface Grafana fonctionnelle (login admin/admin) – Dashboard Kubernetes ou FastAPI visible
<img src="https://github.com/user-attachments/assets/8dcc47b6-0611-4034-9103-584504943cf5" alt="Grafana Dashboard" width="100%"/>

