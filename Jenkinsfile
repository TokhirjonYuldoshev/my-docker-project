pipeline {
    agent any

    environment {
        // Твой логин Docker Hub
        DOCKER_USER = "tokhirjonyuldoshev" 
        IMAGE_NAME  = "shoxrux-app"
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '=== Шаг 1: Скачиваем код ==='
                checkout scm
            }
        }

        stage('Lint Code') {
            steps {
                echo '=== Шаг 2: Линтинг (Quality Gate) ==='
                bat "python -m flake8 app.py --count --statistics"
            }
        }

        stage('Unit Tests') {
            steps {
                echo '=== Шаг 3: Тесты ==='
                bat "python -m pip install pytest && python -m pytest test_app.py"
            }
        }

        stage('Build & Push') {
            steps {
                echo '=== Шаг 4: Сборка и отправка в Docker Hub ==='
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER_VAR')]) {
                        bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER_VAR% --password-stdin'
                        bat "docker build -t %DOCKER_USER_VAR%/%IMAGE_NAME%:%IMAGE_TAG% ."
                        bat "docker push %DOCKER_USER_VAR%/%IMAGE_NAME%:%IMAGE_TAG%"
                        bat "docker logout"
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                echo '=== Шаг 5: Очистка ==='
                bat "docker rmi ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }

    // --- НОВЫЙ БЛОК УВЕДОМЛЕНИЙ ---
    post {
        always {
            script {
                // Достаем секреты из Jenkins
                withCredentials([string(credentialsId: 'telegram-token', variable: 'BOT_TOKEN'),
                                 string(credentialsId: 'telegram-chat-id', variable: 'CHAT_ID')]) {
                    
                    // Формируем сообщения
                    def successMsg = "✅ BUILD SUCCESS! Project: ${env.JOB_NAME} Build: #${env.BUILD_NUMBER}"
                    def failureMsg = "❌ BUILD FAILED! Project: ${env.JOB_NAME} Build: #${env.BUILD_NUMBER}"
                    
                    if (currentBuild.result == null || currentBuild.result == 'SUCCESS') {
                        echo "Отправляем уведомление об УСПЕХЕ..."
                        // Отправляем запрос в Telegram
                        bat "curl -s -X POST https://api.telegram.org/bot%BOT_TOKEN%/sendMessage -d chat_id=%CHAT_ID% -d text=\"%successMsg%\""
                    } else {
                        echo "Отправляем уведомление об ОШИБКЕ..."
                        bat "curl -s -X POST https://api.telegram.org/bot%BOT_TOKEN%/sendMessage -d chat_id=%CHAT_ID% -d text=\"%failureMsg%\""
                    }
                }
            }
        }
    }
}