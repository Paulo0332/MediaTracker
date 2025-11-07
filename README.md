# 📺 Media Tracker - (🚧 In development 🚧)

> MediaTracker is a Django-based web app that lets users search, save, manage and review media by using data fetched from external APIs.

---

## 📘 Table of Contents
- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Docker Setup](#docker-setup)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🧩 About

A clear and concise description of the project.  
Explain **what** it does, **why** it exists, and **who** it’s for.

> MediaTracker is a Django-based web app that serves as a personal media tracker. It lets users search, save, manage, and review movies, games, and other media using data fetched from external APIs. It helps users centralize what they are watching, reading, playing, or listening to into a single personal hub.
---

## ✨ Features

List of key features or functionality.

- 🔍 Search movies, games, books, and anime from external APIs  
- 💾 Save and manage favorites  
- 🌟 Review media with a custom rating system  
- 🧱 Dockerized environment with PostgreSQL  
- 🔐 User authentication system

---

## 🧰 Tech Stack

| Layer        | Technology                         |
|--------------|------------------------------------|
| Backend      | Python / Django                    |
| Database     | PostgreSQL                         |
| API          | External REST API Consumption      |
| Deployment   | Docker & Docker Compose            |
| Frontend     | To be decided                      |


---

## 📁 Project Structure

```bash
├── backend
│   ├── core
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── manage.py
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
└── wait_for_db.sh
```
---

## ⚙️ Setup & Installation

The project uses Docker Compose to orchestrate the entire stack (Django web service and PostgreSQL database). The development environment is configured for zero-setup using VS Code Dev Containers.

### Prerequisites

You must have the following tools installed on your host machine:

1.  **Docker Desktop:** (Includes Docker Engine, CLI, and Compose)
2.  **Visual Studio Code (VS Code):**
3.  **VS Code Dev Containers Extension:** (Installed inside VS Code)

### Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Paulo0332/MediaTracker.git
    cd MediaTracker
    ```

2.  **Configure Secrets**
    The project requires secure environment variables. Copy the provided template to create your local secrets file:
    ```bash
    cp .env.example .env
    # IMPORTANT: Open the new .env file and fill in a strong SECRET_KEY and POSTGRES_PASSWORD.
    ```

3.  **Launch the Development Environment**
    Open the project folder in Visual Studio Code. When prompted by the Dev Containers extension, click **"Reopen in Container."**

The environment will automatically build the necessary images, start the web and db services, and place your terminal inside the web container.

## 🔨 Next sections coming soon!