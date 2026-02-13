pipeline {
    agent any

    environment {
        IMAGE_NAME = "shoxrux-app"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Шаг 1: Забираем код из GitHub...'
                checkout scm
            }
        }

        stage('Lint Code') {
            steps {
                echo 'Шаг 2: Проверка качества кода (Linting)...'
                // Проверяем стиль кода (УСПЕШНО ПРОЙДЕНО)
                bat "python -m flake8 app.py --count --statistics"
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Шаг 3: Запуск модульных тестов...'
                // ИСПРАВЛЕНИЕ: Используем python -m для вызова pip и pytest
                bat "python -m pip install pytest && python -m pytest test_app.py"
            }
        }

        stage('Build Image') {
            steps {
                echo "Шаг 4: Собираем Docker-образ..."
                bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Test Run') {
            steps {
                echo 'Шаг 5: Проверяем запуск контейнера...'
                bat "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Clean Up') {
            steps {
                echo 'Шаг 6: Удаляем временный образ...'
                bat "docker rmi ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }
}