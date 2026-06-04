// Telegram Bot / App Deployment to EC2 (Ubuntu)

pipeline {
    agent any

    environment {
        IMAGE_NAME = "myapp"
        CONTAINER_NAME = "app"
        EC2_IP = "13.60.157.119"
        EC2_USER = "ubuntu"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/SinReaksa/Testing.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Test') {
            steps {
                sh 'echo "Running tests..."'
            }
        }

        stage('Deploy to EC2') {
            steps {
                withCredentials([file(credentialsId: 'ec2-server-key', variable: 'EC2_KEY')]) {
                    sh '''
                    set -e

                    echo "Saving Docker image..."
                    docker save -o myapp.tar $IMAGE_NAME

                    echo "Uploading to EC2..."
                    scp -i $EC2_KEY -o StrictHostKeyChecking=no myapp.tar ${EC2_USER}@${EC2_IP}:/home/${EC2_USER}/myapp.tar

                    echo "Deploying on EC2..."
                    ssh -i $EC2_KEY -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} "
                        docker load -i /home/${EC2_USER}/myapp.tar &&
                        docker stop $CONTAINER_NAME || true &&
                        docker rm $CONTAINER_NAME || true &&
                        docker run -d -p 9090:9090 --name $CONTAINER_NAME $IMAGE_NAME &&
                        rm /home/${EC2_USER}/myapp.tar
                    "

                    rm -f myapp.tar
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful 🚀'
        }
        failure {
            echo 'Deployment Failed ❌'
        }
    }
}