pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timeout(time: 30, unit: 'MINUTES')
    }

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
            when {
                expression {
                    return env.BRANCH_NAME == 'main' || env.GIT_BRANCH == 'origin/main'
                }
            }
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

                def buildResult = currentBuild.currentResult ?: 'UNKNOWN'
                def telegramHeader = buildResult == 'SUCCESS' ? '✅ Jenkins CI/CD — УСПЕХ' : '🚨 Jenkins CI/CD — ТРЕБУЕТ ВНИМАНИЯ'

                try {
                    withCredentials([
                        string(credentialsId: 'telegram-token', variable: 'BOT_TOKEN'),
                        string(credentialsId: 'telegram-chat-id', variable: 'CHAT_ID')
                    ]) {
                        withEnv([
                            "TG_BUILD_RESULT=${buildResult}",
                            "TG_HEADER=${telegramHeader}"
                        ]) {
                            def notifyStatus = bat(
                                returnStatus: true,
                                script: '''@echo off
chcp 65001 >nul
set "TG_MESSAGE_FILE=%TEMP%\\jenkins-telegram-%BUILD_NUMBER%.txt"
(
  echo %TG_HEADER%
  echo.
  echo 📦 Image: %DOCKER_NAMESPACE%/%IMAGE_NAME%:%IMAGE_TAG%
  echo 🔄 Build: #%BUILD_NUMBER%
  echo 📊 Result: %TG_BUILD_RESULT%
  echo 🧪 Gates: Flake8 ^> Pytest ^> Docker build ^> Runtime smoke
  echo 📤 Publish policy: Docker Hub only from main
  echo 🔗 Jenkins: %BUILD_URL%
)>"%TG_MESSAGE_FILE%"

curl --fail --silent --show-error --connect-timeout 10 --max-time 20 -X POST "https://api.telegram.org/bot%BOT_TOKEN%/sendMessage" -d "chat_id=%CHAT_ID%" --data-urlencode "disable_web_page_preview=true" --data-urlencode "text@%TG_MESSAGE_FILE%"
set "TG_EXIT=%ERRORLEVEL%"
del /q "%TG_MESSAGE_FILE%" >nul 2>&1
exit /b %TG_EXIT%
'''
                            )
                            if (notifyStatus != 0) {
                                echo "WARNING: Telegram notification could not be delivered. Jenkins result remains ${buildResult}."
                            }
                        }
                    }
                } catch (err) {
                    echo "WARNING: Telegram notification setup failed. Jenkins result remains ${buildResult}."
                }
            }
        }
    }
}
