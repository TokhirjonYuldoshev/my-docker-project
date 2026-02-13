<div align="center">

# 🚀 DevOps CI/CD Automation Project  
# 🚀 DevOps CI/CD Автоматизация

### End-to-End CI/CD Pipeline with Docker, Jenkins & Automated Testing  
### Полноценный CI/CD пайплайн с Docker, Jenkins и автотестами

![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-red?style=for-the-badge&logo=jenkins)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=for-the-badge&logo=docker)
![Python](https://img.shields.io/badge/Python-3.9-yellow?style=for-the-badge&logo=python)
![Pytest](https://img.shields.io/badge/Tests-Pytest-success?style=for-the-badge&logo=pytest)
![Flake8](https://img.shields.io/badge/Lint-Flake8-black?style=for-the-badge)

</div>

---

# 📌 Project Overview | О проекте

## EN

This project demonstrates a production-style **CI/CD pipeline** built using modern DevOps practices.

It automates the full delivery workflow:

- Static code analysis with Flake8  
- Automated testing with Pytest  
- Docker image build  
- Image push to Docker Hub  
- Telegram build notifications  
- Secure credentials management in Jenkins  

The goal is to simulate a real-world DevOps workflow — from code commit to container deployment.

---

## RU

Этот проект демонстрирует production-подобный **CI/CD пайплайн**, построенный с использованием современных DevOps-практик.

Он автоматизирует полный процесс доставки приложения:

- Статический анализ кода через Flake8  
- Автоматическое тестирование с помощью Pytest  
- Сборка Docker-образа  
- Публикация образа в Docker Hub  
- Уведомления о сборке в Telegram  
- Безопасное управление учётными данными в Jenkins  

Цель проекта — смоделировать реальный DevOps-процесс от коммита кода до публикации контейнера.

---

# 🧱 CI/CD Architecture | Архитектура CI/CD

```
Developer → GitHub (Push)
                │
                ▼
            Jenkins Pipeline
                │
    ┌────────────────────────────┐
    │ 1️⃣ Checkout Source Code    │
    │ 2️⃣ Lint (Flake8)           │
    │ 3️⃣ Run Tests (Pytest)      │
    │ 4️⃣ Build Docker Image      │
    │ 5️⃣ Push to Docker Hub      │
    │ 6️⃣ Telegram Notification    │
    └────────────────────────────┘
```

---

# 🛠️ Tech Stack | Технологический стек

| Category | Technology |
|----------|------------|
| Programming Language | Python 3.9 |
| CI/CD Engine | Jenkins (Declarative Pipeline) |
| Containerization | Docker |
| Testing Framework | Pytest |
| Code Quality | Flake8 |
| Container Registry | Docker Hub |
| Notifications | Telegram Bot API |

---

# ⚙️ Pipeline Stages | Этапы пайплайна

| Stage | EN | RU |
|-------|----|----|
| 1️⃣ Checkout | Pull source code from GitHub | Получение исходного кода из GitHub |
| 2️⃣ Lint | Run Flake8 analysis | Проверка качества кода через Flake8 |
| 3️⃣ Test | Execute Pytest suite | Запуск автотестов Pytest |
| 4️⃣ Build | Build Docker image | Сборка Docker-образа |
| 5️⃣ Push | Push image to Docker Hub | Публикация образа в Docker Hub |
| 6️⃣ Notify | Send Telegram notification | Отправка уведомления в Telegram |

---

# 🟢 Build & Image Status | Статус сборки и образа

![Docker Pulls](https://img.shields.io/docker/pulls/tokhirjonyuldoshev/shoxrux-app?style=flat-square&logo=docker)

---

# 🚀 Quick Start | Быстрый запуск

```bash
docker run --rm tokhirjonyuldoshev/shoxrux-app:23
```

---

# 🎯 Key DevOps Concepts | Ключевые DevOps-подходы

## EN
- CI/CD pipeline design  
- Declarative Jenkins Pipelines  
- Automated testing integration  
- Docker image lifecycle management  
- Secure secret handling  
- End-to-end automation  

## RU
- Проектирование CI/CD пайплайна  
- Declarative Pipeline в Jenkins  
- Интеграция автотестирования  
- Управление жизненным циклом Docker-образа  
- Безопасная работа с секретами  
- Сквозная автоматизация  

---

# 👨‍💻 Author | Автор

**Tokhirjon Yuldoshev**

- GitHub: https://github.com/TokhirjonYuldoshev  
- Docker Hub: https://hub.docker.com/u/tokhirjonyuldoshev  

---

<div align="center">

## ⭐ If you found this project useful, consider giving it a star!  
## ⭐ Если проект был полезен — поддержите его звездой!

</div>
