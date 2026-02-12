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

        stage('Build Image') {
            steps {
                echo "Шаг 2: Собираем Docker-образ..."
                // Для Windows используем bat вместо sh
                bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Test Run') {
            steps {
                echo 'Шаг 3: Проверяем запуск контейнера...'
                bat "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Clean Up') {
            steps {
                echo 'Шаг 4: Удаляем временный образ...'
                bat "docker rmi ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }
}