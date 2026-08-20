pipeline {
    agent any

    environment {
        NAMESPACE   = 'devops-app'
        FLASK_IMAGE = 'samsj/devops-flask:2.0'
        REACT_IMAGE = 'samsj/devops-react:1.0'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/samrajviswasam/k8s-Project.git'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin
                    '''
                }
            }
        }

        stage('Verify Docker Images') {
            steps {
                sh '''
                    docker pull ${FLASK_IMAGE}
                    docker pull ${REACT_IMAGE}
                '''
            }
        }

        stage('Deploy PostgreSQL') {
            steps {
                sh '''
                    kubectl apply -f flask-app/postgres-secret.yaml  
                    kubectl apply -f flask-app/postgres-pvc.yaml
                    kubectl apply -f flask-app/postgres-deployment.yaml
                    kubectl apply -f flask-app/postgres-service.yaml
                '''
            }
        }

        stage('Deploy Flask') {
            steps {
                sh '''
                    kubectl apply -f flask-app/flask-configmap.yaml
                    kubectl apply -f flask-app/flask-deployment.yaml
                    kubectl apply -f flask-app/flask-service.yaml
                '''
            }
        }

        stage('Deploy React') {
            steps {
                sh '''
                    kubectl apply -f react-app/react-deployment.yaml
                    kubectl apply -f react-app/react-service.yaml
                '''
            }
        }

        stage('Deploy Ingress') {
            steps {
                sh '''
                    kubectl apply -f ingress.yaml
                '''
            }
        }

        stage('Configure HPA') {
            steps {
                sh '''
                    kubectl apply -f flask-app/flask-hpa.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    echo "===== DEPLOYMENTS ====="
                    kubectl get deployments -n ${NAMESPACE}

                    echo "===== PODS ====="
                    kubectl get pods -n ${NAMESPACE}

                    echo "===== SERVICES ====="
                    kubectl get services -n ${NAMESPACE}

                    echo "===== INGRESS ====="
                    kubectl get ingress -n ${NAMESPACE}

                    echo "===== HPA ====="
                    kubectl get hpa -n ${NAMESPACE}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    kubectl rollout status deployment/postgres -n ${NAMESPACE}
                    kubectl rollout status deployment/flask -n ${NAMESPACE}
                    kubectl rollout status deployment/react -n ${NAMESPACE}
                '''
            }
        }

        stage('Final Status') {
            steps {
                sh '''
                    echo "===== FINAL POD STATUS ====="
                    kubectl get pods -n ${NAMESPACE}

                    echo "===== FINAL DEPLOYMENT STATUS ====="
                    kubectl get deployments -n ${NAMESPACE}
                '''
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }

        success {
            echo 'CI/CD deployment completed successfully!'
        }

        failure {
            echo 'CI/CD deployment failed. Check the Jenkins console output.'
        }
    }
}
