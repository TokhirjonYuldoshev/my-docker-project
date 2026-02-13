# 🚀 DevOps CI/CD Docker Project

![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-red?style=for-the-badge&logo=jenkins)
![Docker](https://img.shields.io/badge/Docker-Image-blue?style=for-the-badge&logo=docker)
![Python](https://img.shields.io/badge/Python-3.9-yellow?style=for-the-badge&logo=python)
![Tests](https://img.shields.io/badge/Tests-Pytest-success?style=for-the-badge&logo=pytest)

---

## 👨‍💻 Author
**Tokhirjon Yuldoshev**  
🔗 GitHub: https://github.com/TokhirjonYuldoshev  
🐳 Docker Hub: https://hub.docker.com/u/tokhirjonyuldoshev  

---

## 📌 Project Overview
This is a **DevOps + QA Automation** pet project that demonstrates a **fully automated CI/CD pipeline** using industry-standard tools.

The pipeline automatically:

- Validates code quality
- Runs unit tests
- Builds a Docker image
- Pushes the image to Docker Hub
- Sends build notifications to Telegram

---

## 🧱 CI/CD Architecture
```
GitHub (Push)
     │
     ▼
  Jenkins 🤖
     │
     ├─► 1. Checkout Code
     │
     ├─► 2. Lint (Flake8) 🔍
     │
     ├─► 3. Tests (Pytest) 🧪
     │
     ├─► 4. Build Docker Image 🐳
     │
     ├─► 5. Push to Docker Hub ☁️
     │
     └─► 6. Telegram Notification 📱
```

---

## 🛠️ Tech Stack

| Category        | Tool |
|-----------------|------|
| Language        | Python 3.9 |
| Containerization| Docker |
| CI/CD           | Jenkins (Declarative Pipeline) |
| Testing         | Pytest |
| Code Quality    | Flake8 |
| Registry        | Docker Hub |
| Notifications   | Telegram Bot API |

---

## ⚙️ Pipeline Stages

1. **Checkout** – Pull code from GitHub  
2. **Lint** – Code style check via flake8  
3. **Tests** – Run pytest  
4. **Build** – Docker image build  
5. **Push** – Upload image to Docker Hub  
6. **Notify** – Send result to Telegram  

---

## 🟢 Build Status

![Docker Pulls](https://img.shields.io/docker/pulls/tokhirjonyuldoshev/shoxrux-app?style=flat-square&logo=docker)

---

## 🚀 Quick Start

Run the container:

```bash
docker run --rm tokhirjonyuldoshev/shoxrux-app:23
```

---

## 📦 Docker Image
https://hub.docker.com/u/tokhirjonyuldoshev

---

## 🎯 What This Project Demonstrates

- CI/CD pipeline design
- Jenkins Declarative Pipelines
- Automated testing
- Docker image lifecycle
- Secure credentials handling
- Production-like DevOps workflow

---

## 📬 Contact

- GitHub: https://github.com/TokhirjonYuldoshev
- Docker Hub: https://hub.docker.com/u/tokhirjonyuldoshev
