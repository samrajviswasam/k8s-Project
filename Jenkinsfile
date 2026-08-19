pipeline {
    agent any

    environment {
        NAMESPACE = 'devops-app'
        FLASK_IMAGE = 'devops-flask:2.0'
        REACT_IMAGE = 'devops-react:1.0'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/samrajviswasam/k8s-Project.git'
            }
        }

        stage('Build Flask Image') {
            steps {
                sh 'docker build -t ${FLASK_IMAGE} ./flask-app'
            }
        }

        stage('Build React Image') {
            steps {
                sh 'docker build -t ${REACT_IMAGE} ./react-app'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f flask-app/postgres-secret.yaml
                    kubectl apply -f flask-app/postgres-pvc.yaml
                    kubectl apply -f flask-app/postgres-deployment.yaml
                    kubectl apply -f flask-app/postgres-service.yaml

                    kubectl apply -f flask-app/flask-configmap.yaml
                    kubectl apply -f flask-app/flask-deployment.yaml
                    kubectl apply -f flask-app/flask-service.yaml

                    kubectl apply -f react-app/react-deployment.yaml
                    kubectl apply -f react-app/react-service.yaml

                    kubectl apply -f ingress.yaml
                    kubectl apply -f flask-app/flask-hpa.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl rollout status deployment/postgres -n ${NAMESPACE}
                    kubectl rollout status deployment/flask -n ${NAMESPACE}
                    kubectl rollout status deployment/react -n ${NAMESPACE}

                    kubectl get pods -n ${NAMESPACE}
                    kubectl get services -n ${NAMESPACE}
                    kubectl get ingress -n ${NAMESPACE}
                    kubectl get hpa -n ${NAMESPACE}
                '''
            }
        }
    }

    post {
        success {
            echo 'DevOps Kubernetes deployment completed successfully!'
        }

        failure {
            echo 'Deployment failed. Check the Jenkins console output.'
        }
    }
}
