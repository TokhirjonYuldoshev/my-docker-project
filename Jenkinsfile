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

        stage('Verify Python Runtime') {
            steps {
                bat 'python -c "import sys; print(sys.version); assert sys.version_info >= (3, 12)"'
            }
        }

        stage('Install CI Dependencies') {
            steps {
                bat 'python -m pip install --disable-pip-version-check -r requirements-dev.txt'
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

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %DOCKER_NAMESPACE%/%IMAGE_NAME%:%IMAGE_TAG% .'
            }
        }

        stage('Container Smoke Test') {
            steps {
                bat 'docker run --rm %DOCKER_NAMESPACE%/%IMAGE_NAME%:%IMAGE_TAG% | findstr /x /c:"Hello from Docker! The application is running successfully."'
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'docker-hub-credentials',
                            passwordVariable: 'DOCKER_PASS',
                            usernameVariable: 'DOCKER_USER'
                        )
                    ]) {
                        try {
                            bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                            bat 'docker push %DOCKER_NAMESPACE%/%IMAGE_NAME%:%IMAGE_TAG%'
                        } finally {
                            bat(returnStatus: true, script: 'docker logout')
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                bat(
                    returnStatus: true,
                    script: 'docker rmi %DOCKER_NAMESPACE%/%IMAGE_NAME%:%IMAGE_TAG%'
                )
            }
        }

        success {
            script {
                withCredentials([
                    string(credentialsId: 'telegram-token', variable: 'BOT_TOKEN'),
                    string(credentialsId: 'telegram-chat-id', variable: 'CHAT_ID')
                ]) {
                    def notifyStatus = bat(
                        returnStatus: true,
                        script: 'curl --fail --silent --show-error -X POST "https://api.telegram.org/bot%BOT_TOKEN%/sendMessage" -d "chat_id=%CHAT_ID%" --data-urlencode "text=SUCCESS: Jenkins build #%BUILD_NUMBER% published %DOCKER_NAMESPACE%/%IMAGE_NAME%:%IMAGE_TAG%"'
                    )
                    if (notifyStatus != 0) {
                        echo 'WARNING: Telegram success notification could not be delivered.'
                    }
                }
            }
        }

        failure {
            script {
                withCredentials([
                    string(credentialsId: 'telegram-token', variable: 'BOT_TOKEN'),
                    string(credentialsId: 'telegram-chat-id', variable: 'CHAT_ID')
                ]) {
                    def notifyStatus = bat(
                        returnStatus: true,
                        script: 'curl --fail --silent --show-error -X POST "https://api.telegram.org/bot%BOT_TOKEN%/sendMessage" -d "chat_id=%CHAT_ID%" --data-urlencode "text=FAILED: Jenkins build #%BUILD_NUMBER%. Check Jenkins console output."'
                    )
                    if (notifyStatus != 0) {
                        echo 'WARNING: Telegram failure notification could not be delivered.'
                    }
                }
            }
        }
    }
}
