pipeline {
    agent any

    environment {
        // --- НАСТРОЙКИ ---
        // Твой логин на Docker Hub (без пароля!)
        DOCKER_USER = "tokhirjonyuldoshev" 
        
        // Название образа и тег
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
                        // 1. Логинимся (пароль передается скрытно)
                        bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER_VAR% --password-stdin'
                        
                        echo "Сборка образа..."
                        // 2. Собираем образ: логин/имя:версия
                        bat "docker build -t %DOCKER_USER_VAR%/%IMAGE_NAME%:%IMAGE_TAG% ."
                        
                        echo "Отправка в облако..."
                        // 3. Отправляем (Push)
                        bat "docker push %DOCKER_USER_VAR%/%IMAGE_NAME%:%IMAGE_TAG%"
                        
                        // 4. Выходим
                        bat "docker logout"
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                echo '=== Шаг 5: Очистка диска ==='
                // Удаляем локальный образ, чтобы не занимать место
                bat "docker rmi ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }
}