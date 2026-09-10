pipeline {
    agent any

    environment {
        DOCKER_NAMESPACE = "tokhirjonyuldoshev"
        IMAGE_NAME = "shoxrux-app"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install CI Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements-dev.txt'
            }
        }

        stage('Lint') {
            steps {
                bat 'python -m flake8 app.py test_app.py --count --statistics'
            }
        }

        stage('Unit Tests') {
            steps {
                bat 'python -m pytest -q'
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'docker-hub-credentials',
                            passwordVariable: 'DOCKER_PASS',
                            usernameVariable: 'DOCKER_USER'
                        )
                    ]) {
                        bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                        bat 'docker build -t %DOCKER_NAMESPACE%/%IMAGE_NAME%:%IMAGE_TAG% .'
                        bat 'docker push %DOCKER_NAMESPACE%/%IMAGE_NAME%:%IMAGE_TAG%'
                        bat 'docker logout'
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                bat 'docker rmi %DOCKER_NAMESPACE%/%IMAGE_NAME%:%IMAGE_TAG%'
            }
        }
    }

    post {
        success {
            script {
                withCredentials([
                    string(credentialsId: 'telegram-token', variable: 'BOT_TOKEN'),
                    string(credentialsId: 'telegram-chat-id', variable: 'CHAT_ID')
                ]) {
                    bat 'curl --fail --silent --show-error -X POST "https://api.telegram.org/bot%BOT_TOKEN%/sendMessage" -d "chat_id=%CHAT_ID%" --data-urlencode "text=SUCCESS: Jenkins build #%BUILD_NUMBER% published %DOCKER_NAMESPACE%/%IMAGE_NAME%:%IMAGE_TAG%"'
                }
            }
        }

        failure {
            script {
                withCredentials([
                    string(credentialsId: 'telegram-token', variable: 'BOT_TOKEN'),
                    string(credentialsId: 'telegram-chat-id', variable: 'CHAT_ID')
                ]) {
                    bat 'curl --fail --silent --show-error -X POST "https://api.telegram.org/bot%BOT_TOKEN%/sendMessage" -d "chat_id=%CHAT_ID%" --data-urlencode "text=FAILED: Jenkins build #%BUILD_NUMBER%. Check Jenkins console output."'
                }
            }
        }
    }
}
