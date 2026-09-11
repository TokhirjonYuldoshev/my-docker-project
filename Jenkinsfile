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
                bat 'python -m pip check'
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

        stage('Container Runtime Policy') {
            steps {
                bat '''@echo off
setlocal
set "INSPECT_FILE=%TEMP%\\docker-user-%BUILD_NUMBER%.txt"
docker image inspect %DOCKER_NAMESPACE%/%IMAGE_NAME%:%IMAGE_TAG% --format "{{.Config.User}}" > "%INSPECT_FILE%" 2>&1
set "INSPECT_EXIT=%ERRORLEVEL%"
if not "%INSPECT_EXIT%"=="0" (
    type "%INSPECT_FILE%"
    del /q "%INSPECT_FILE%" >nul 2>&1
    endlocal & exit /b %INSPECT_EXIT%
)
set /p "CONFIGURED_USER="<"%INSPECT_FILE%"
del /q "%INSPECT_FILE%" >nul 2>&1
if not defined CONFIGURED_USER (
    echo ERROR: Docker image does not declare a runtime user.
    endlocal & exit /b 1
)
if /I "%CONFIGURED_USER%"=="root" (
    echo ERROR: Docker image declares root as runtime user.
    endlocal & exit /b 1
)
if "%CONFIGURED_USER%"=="0" (
    echo ERROR: Docker image declares UID 0 as runtime user.
    endlocal & exit /b 1
)
echo Verified non-root Docker runtime user: %CONFIGURED_USER%
endlocal
'''
            }
        }

        stage('Container Smoke Test') {
            steps {
                bat '''@echo off
setlocal
set "SMOKE_FILE=%TEMP%\\docker-smoke-%BUILD_NUMBER%.txt"
docker run --rm %DOCKER_NAMESPACE%/%IMAGE_NAME%:%IMAGE_TAG% > "%SMOKE_FILE%" 2>&1
set "DOCKER_EXIT=%ERRORLEVEL%"
if not "%DOCKER_EXIT%"=="0" (
    type "%SMOKE_FILE%"
    del /q "%SMOKE_FILE%" >nul 2>&1
    endlocal & exit /b %DOCKER_EXIT%
)
powershell.exe -NoLogo -NoProfile -NonInteractive -Command "$actual = (Get-Content -LiteralPath $env:SMOKE_FILE -Raw).Trim(); if ($actual -cne 'Hello from Docker! The application is running successfully.') { Write-Error ('Container stdout contract mismatch. Actual: ' + $actual); exit 1 }"
set "VERIFY_EXIT=%ERRORLEVEL%"
type "%SMOKE_FILE%"
del /q "%SMOKE_FILE%" >nul 2>&1
if not "%VERIFY_EXIT%"=="0" (
    endlocal & exit /b %VERIFY_EXIT%
)
endlocal
'''
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
  echo 🧪 Gates: Flake8 ^> Pytest ^> Docker build ^> non-root policy ^> runtime smoke
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
