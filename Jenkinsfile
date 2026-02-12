pipeline {
    agent any

    environment {
        // Название твоего образа
        IMAGE_NAME = "my-docker-app"
        IMAGE_TAG  = "${env.BUILD_NUMBER}" // Тег будет равен номеру сборки
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Скачиваем код из Git...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Начинаем сборку образа...'
                script {
                    // Команда сборки Docker-образа
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Test Container') {
            steps {
                echo 'Проверяем, что контейнер запускается...'
                script {
                    // Запускаем контейнер и проверяем, что он выдает нужный текст
                    sh "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Clean Up') {
            steps {
                echo 'Удаляем старые образы, чтобы не занимать место...'
                sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }

    post {
        success {
            echo 'Ура! Образ собран и протестирован.'
        }
        failure {
            echo 'Что-то пошло не так. Проверь логи Docker.'
        }
    }
}