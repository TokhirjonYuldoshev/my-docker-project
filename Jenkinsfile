pipeline {
    agent any

    environment {
        // Твой логин на Docker Hub
        DOCKER_USER = "tokhirjonyuldoshev" 
        
        // Название образа и тег (номер сборки)
        IMAGE_NAME  = "shoxrux-app"
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '=== Шаг 1: Скачиваем код из GitHub ==='
                checkout scm
            }
        }

        stage('Lint Code') {
            steps {
                echo '=== Шаг 2: Проверка качества кода (Linting) ==='
                // Проверяем стиль кода (PEP8)
                bat "python -m flake8 app.py --count --statistics"
            }
        }

        stage('Unit Tests') {
            steps {
                echo '=== Шаг 3: Запуск тестов ==='
                // Устанавливаем pytest и запускаем тест
                bat "python -m pip install pytest && python -m pytest test_app.py"
            }
        }

        stage('Build & Push') {
            steps {
                echo '=== Шаг 4: Сборка и отправка в Docker Hub ==='
                script {
                    // Берем пароль из секретного хранилища Jenkins
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER_VAR')]) {
                        
                        echo "Авторизация в Docker Hub..."
                        bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER_VAR% --password-stdin'
                        
                        echo "Сборка образа..."
                        bat "docker build -t %DOCKER_USER_VAR%/%IMAGE_NAME%:%IMAGE_TAG% ."
                        
                        echo "Отправка в облако..."
                        bat "docker push %DOCKER_USER_VAR%/%IMAGE_NAME%:%IMAGE_TAG%"
                        
                        echo "Выход..."
                        bat "docker logout"
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                echo '=== Шаг 5: Очистка диска ==='
                // Удаляем локальный образ
                bat "docker rmi ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }

    // --- БЛОК УВЕДОМЛЕНИЙ В TELEGRAM ---
    post {
        always {
            script {
                // Достаем секреты (Токен и Chat ID)
                withCredentials([string(credentialsId: 'telegram-token', variable: 'BOT_TOKEN'),
                                 string(credentialsId: 'telegram-chat-id', variable: 'CHAT_ID')]) {
                    
                    // Формируем красивые сообщения (Groovy переменные)
                    def successMsg = "✅ SUCCESS! Build: #${env.BUILD_NUMBER}\n📦 Image: ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    def failureMsg = "❌ FAILED! Build: #${env.BUILD_NUMBER}\n⚠️ Check Jenkins Console!"
                    
                    if (currentBuild.result == null || currentBuild.result == 'SUCCESS') {
                        echo "Отправляем сообщение об УСПЕХЕ..."
                        // Используем curl с флагом -k (insecure) для Windows и --data-urlencode для текста
                        bat "curl -k -s -X POST https://api.telegram.org/bot%BOT_TOKEN%/sendMessage -d chat_id=%CHAT_ID% --data-urlencode \"text=${successMsg}\""
                    } else {
                        echo "Отправляем сообщение об ОШИБКЕ..."
                        bat "curl -k -s -X POST https://api.telegram.org/bot%BOT_TOKEN%/sendMessage -d chat_id=%CHAT_ID% --data-urlencode \"text=${failureMsg}\""
                    }
                }
            }
        }
    }
}