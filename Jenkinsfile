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

        // ВОТ ЭТОТ ЭТАП НУЖНО ДОБАВИТЬ:
        stage('Lint Code') {
            steps {
                echo 'Шаг 2: Проверка качества кода (Linting)...'
                // Для Windows используем python -m flake8
                bat "python -m flake8 app.py --count --statistics"
            }
        }

        stage('Build Image') {
            steps {
                echo "Шаг 3: Собираем Docker-образ..."
                bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Test Run') {
            steps {
                echo 'Шаг 4: Проверяем запуск контейнера...'
                bat "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Clean Up') {
            steps {
                echo 'Шаг 5: Удаляем временный образ...'
                bat "docker rmi ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }
}