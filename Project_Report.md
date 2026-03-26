# Project Report: Cloud-Based Log Monitoring & Security Analyzer

**Course:** Cloud Computing Lab (CCL) Mini-Project  
**Project Title:** Cloud Log Analyzer  
**Developer:** Sarthak  
**Date:** March 23, 2026

---

## 1. Introduction
The **Cloud Log Analyzer** is a secure, interactive web application designed to monitor and analyze cloud infrastructure logs. It provides real-time insights into system health, traffic distribution, and potential security threats. The project is built to demonstrate the integration of various cloud computing services, including PaaS, DBaaS, Security, and Containerization.

## 2. Problem Statement
Managing and interpreting large volumes of server logs is a complex task. Manual log analysis is slow and prone to errors, making it difficult to identify security breaches or system failures in real-time. This project addresses these challenges by providing an automated, visual, and secure platform for log analysis.

## 3. Objectives
- To design a user-friendly **PaaS-based web application** for log monitoring.
- To implement **DBaaS (Database as a Service)** for persistent storage of analysis results.
- To incorporate **Advanced Security Features** such as WAF simulation (Suspicious IP Detection).
- To provide **Real-time Anomaly Detection** and interactive data visualizations.
- To ensure the application is **Cloud-Ready** using containerization (Docker).

## 4. Technical Stack
- **Frontend/Backend:** [Streamlit](https://streamlit.io/) (Python-based PaaS framework)
- **Data Visualization:** [Plotly Interactive Charts](https://plotly.com/) & Matplotlib
- **Data Manipulation:** Pandas
- **Database (DBaaS):** [MongoDB Atlas](https://www.mongodb.com/atlas/database) (Cloud-hosted NoSQL)
- **Security:** Python-dotenv (Environment Variable Management)
- **Containerization:** Docker

## 5. Cloud Services Mapping (CCL Syllabus)
This project covers the following core cloud computing concepts:

| Service Category | Implementation in Project |
| :--- | :--- |
| **PaaS (Platform as a Service)** | Built using Streamlit, which is designed for rapid cloud deployment. |
| **DBaaS (Database as a Service)** | Integrated with MongoDB Atlas for secure, cloud-hosted data persistence. |
| **Security** | Secure authentication using environment variables and Suspicious IP Detection. |
| **Containerization** | Fully Dockerized for deployment on any IaaS (AWS EC2, Azure VM, etc.). |
| **Storage as a Service** | Analysis results and timestamps are stored persistently in the cloud DB. |

## 6. Key Features
### 6.1. Secure Authentication
The system uses a multi-page flow (Home -> Login -> Dashboard) with credentials managed securely via environment variables.

### 6.2. Advanced Log Analysis
- **Error Tracking:** Automatically counts and visualizes HTTP 404 and 500 errors.
- **WAF Simulation:** Detects "Suspicious IPs" that attempt to access restricted paths (e.g., `/admin`, `/.env`) multiple times.
- **Anomaly Detection:** Triggers a high-priority alert (🚨) if server errors (500) exceed a critical threshold.

### 6.3. Interactive Dashboard
- **Plotly Visuals:** Interactive bar and donut charts that allow users to hover, zoom, and export data.
- **Metrics Overview:** Real-time counters for errors and security threats.
- **Reporting:** Generates and allows downloading of CSV-based analysis reports.

## 7. Project Architecture
1. **User Input:** Log file upload (.txt or .log).
2. **Processing Layer:** Python logic parses the log content and extracts IPs/Status codes.
3. **Storage Layer:** Results are pushed to MongoDB Atlas with a timestamped audit trail.
4. **Presentation Layer:** Streamlit renders an interactive, blue-and-white themed dashboard.
5. **Deployment Layer:** Docker encapsulates the entire environment for cloud portability.

## 8. Conclusion
The Cloud Log Analyzer successfully demonstrates a comprehensive cloud-integrated solution for infrastructure monitoring. By combining modern web frameworks with cloud database services and containerization, it provides a scalable and secure tool for developers and system administrators to safeguard their cloud resources.

---

## 9. Appendix: Viva Questions & Answers
**Q: How is this "Cloud-Based"?**  
A: "The application is designed for PaaS deployment, uses a DBaaS (MongoDB Atlas), and is containerized with Docker to run on any cloud IaaS."

**Q: What security features did you implement?**  
A: "Secure environment variable management for credentials and a built-in security analyzer that flags suspicious IP patterns similar to a WAF."

**Q: Why use Docker?**  
A: "Docker ensures that the application runs identically in any cloud environment, solving the 'it works on my machine' problem and making it easy to scale horizontally on AWS or Azure."
