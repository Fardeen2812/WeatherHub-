# WeatherHub 🌦️

WeatherHub is a microservices-based application designed to provide weather updates, user preferences, and recommendations. It leverages modern cloud-native technologies like Kubernetes, Docker, and PostgreSQL to deliver a scalable and reliable solution.

---

## Features 🚀

- **Weather API Integration**: Fetch real-time weather data using OpenWeather API.
- **User Preferences**: Store and manage user preferences securely.
- **Recommendations**: Provide personalized recommendations based on weather conditions.
- **Notifications**: Send alerts and notifications using Twilio and SendGrid.
- **Scalable Architecture**: Built with Kubernetes and Docker for scalability and reliability.

---

## Architecture Overview 🏗️

The application consists of the following microservices:

1. **Frontend Gateway**:
   - Acts as the entry point for users.
   - Connects to backend services like `user-preferences`, `recommendation-engine`, and `weather-api`.

2. **User Preferences**:
   - Manages user credentials and preferences.
   - Stores data in a PostgreSQL database.

3. **Recommendation Engine**:
   - Provides personalized recommendations based on user preferences and weather data.

4. **Weather API**:
   - Fetches real-time weather data from OpenWeather API.

5. **Alert Notifications**:
   - Sends alerts and notifications using Twilio and SendGrid.

6. **Redis**:
   - Used for caching to improve performance.

---

## Prerequisites 🛠️

Before running the application, ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Kubernetes](https://kubernetes.io/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/)
- [Git](https://git-scm.com/)
- [Python 3.10+](https://www.python.org/)

---

## Installation and Setup ⚙️

### 1. Clone the Repository
```bash
git clone https://github.com/Fardeen2812/WeatherHub.git
cd WeatherHub

Project Structure 📂

weatherhub/
├── README.md
├── architecture-diagram.png
├── docker-compose.yml (for local testing)
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── providers.tf
├── jenkinsfile
├── frontend-gateway/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   └── style.css
│   ├── requirements.txt
│   ├── Dockerfile
├── weather-api/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
├── user-preferences/
│   ├── app.py
│   ├── models.py
│   ├── auth.py
│   ├── requirements.txt
│   ├── Dockerfile
├── recommendation-engine/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
├── alerts-notifications/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
└── k8s/
    ├── weather-api-deployment.yaml
    ├── user-preferences-deployment.yaml
    ├── recommendation-engine-deployment.yaml
    ├── alerts-notifications-deployment.yaml
    ├── frontend-gateway-deployment.yaml
    ├── redis-deployment.yaml
    ├── postgres-deployment.yaml
    ├── secrets.yaml

📈 Diagram Flow (Architecture)

User --> Frontend Gateway (Flask) --> Microservices
                               ↘
                        Weather-API (OpenWeather)
                        User Preferences (PostgreSQL)
                        Recommendation Engine (Redis)
                        Alerts & Notifications (Twilio/SendGrid)

All deployed on Azure Kubernetes Service (AKS), managed by Jenkins pipelines, secrets in KeyVault, monitored by Prometheus/Grafana.

                           +---------------------+
                           |      Frontend        |
                           |  (Flask Gateway)     |
                           +----------+-----------+
                                      |
             +-------------------------------------------------+
             |       Kubernetes Cluster (Azure AKS)            |
             | +------------+  +------------+ +--------------+ |
             | | Weather API |  | Preferences| |Recommendation| |
             | +------------+  +------------+ +--------------+ |
             | +----------------------+ +--------------------+ |
             | | Alerts Notifications  | |  Redis/PostgreSQL  | |
             | +----------------------+ +--------------------+ |
             +-------------------------------------------------+
                                      |
                           +---------------------+
                           | Azure Resources (Key Vault, ACR) |
                           +---------------------+

