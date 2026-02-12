pipeline {
    agent any

    environment {
        // Имя твоего будущего образа
        IMAGE_NAME = "shoxrux-app"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Шаг 1: Забираем актуальный код из GitHub...'
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                echo "Шаг 2: Собираем Docker-образ ${IMAGE_NAME}..."
                // Собираем образ, используя Dockerfile в корне папки
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Test Run') {
            steps {
                echo 'Шаг 3: Проверяем работу контейнера...'
                // Запускаем контейнер и смотрим, выведет ли он наше сообщение из app.py
                sh "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Clean Up') {
            steps {
                echo 'Шаг 4: Очистка системы от временного образа...'
                sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }

    post {
        success {
            echo 'ПОБЕДА: Пайплайн завершен успешно!'
        }
        failure {
            echo 'ОШИБКА: Что-то пошло не так. Проверь логи сборки.'
        }
    }
}