# Dealerships and Reviews - Full Stack Capstone Project

## Project Details
- **Project Name**: Dealerships and Reviews - Best Cars Application
- **Repository Name**: xrwvm-fullstack_developer_capstone

## Project Overview
**Best Cars Dealerships and Reviews Application** is a full-stack, cloud-native web application developed as part of the IBM Full Stack Software Developer Capstone Project. The platform enables users to browse nationwide car dealerships, filter dealerships by state, view detailed dealer profiles, read customer reviews with integrated AI sentiment analysis, and submit their own reviews.

## Architecture & Technology Stack
- **Frontend**: React.js, HTML5, CSS3, Bootstrap 5
- **Backend / Web Server**: Django 4.2 Web Framework (Python)
- **Database & Microservices**:
  - Express.js and Node.js REST API with MongoDB for dealerships and customer reviews data
  - Python Flask microservice using NLTK SentimentIntensityAnalyzer for sentiment analysis of customer reviews
  - SQLite database for Django Car Makes and Car Models
- **Containerization & CI/CD**:
  - Docker containerization for Express MongoDB service and Flask sentiment analyzer
  - GitHub Actions for automated linting, testing, and continuous integration
  - IBM Cloud Code Engine deployment