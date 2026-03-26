# Cloud Log Analyzer Project

A secure, cloud-integrated log analysis dashboard built with Streamlit and MongoDB.

## Features
- **Security**: Login system using environment variables.
- **Log Analysis**: Analyzes HTTP error codes (404, 500) and extracts IP addresses.
- **Advanced Security**: Suspicious IP detection (WAF simulation) for high 404 frequencies.
- **Anomaly Detection**: Alerts for high frequency of server errors.
- **Cloud Database**: Stores analysis results in MongoDB Atlas.
- **Data Visualization**: Interactive charts using Matplotlib.
- **Reporting**: Downloadable CSV reports.

## Prerequisites
- Python 3.11+
- MongoDB Atlas account (free tier works great)

## Setup & Local Run

1. **Clone the repository** (if applicable).
2. **Create a `.env` file** in the root directory with the following variables:
   ```env
   APP_USERNAME=your_username
   APP_PASSWORD=your_password
   MONGO_USER=your_mongo_user
   MONGO_PASS=your_mongo_password
   MONGO_HOST=your_cluster_url
   MONGO_APP_NAME=your_app_name
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Docker Deployment (Recommended for Cloud)

This project is fully Dockerized for easy deployment on any cloud provider (AWS EC2, Azure VM, Render, etc.).

1. **Build the Docker Image**:
   ```bash
   docker build -t cloud-log-analyzer .
   ```
2. **Run the Docker Container**:
   Pass your `.env` file to the container:
   ```bash
   docker run -p 8501:8501 --env-file .env cloud-log-analyzer
   ```
3. Access the app at `http://localhost:8501`.

## Cloud Services Used (CCL Syllabus Mapping)
- **PaaS**: Streamlit (can be hosted on Streamlit Cloud).
- **DBaaS**: MongoDB Atlas.
- **Containerization**: Docker.
- **Security**: Environment variable-based authentication.
