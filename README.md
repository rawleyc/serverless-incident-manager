# ⚡ Serverless Incident Management System

![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Serverless](https://img.shields.io/badge/Architecture-Serverless-blue)

A fully serverless IT support ticketing system built on AWS. This application utilizes an **Event-Driven Architecture** to handle support requests, store data, and trigger notifications without provisioning a single EC2 instance. The entire stack scales to zero, incurring **$0.00 cost** when idle.

## 🏗 Architecture

The application decouples the frontend, logic, and database layers into separate microservices:



1.  **Frontend:** A static Single Page Application (SPA) hosted on **Amazon S3**.
2.  **API Layer:** **Amazon API Gateway** (HTTP API) serves as the entry point, routing requests to specific Lambda functions.
3.  **Compute:** **AWS Lambda** (Python 3.9) handles business logic (creating tickets, generating IDs, scanning DB).
4.  **Database:** **Amazon DynamoDB** stores ticket data with sub-millisecond latency.
5.  **Notifications:** **Amazon SNS** triggers asynchronous email alerts to administrators immediately after ticket creation.

## 🛠 Tech Stack

* **Cloud Provider:** AWS
* **Infrastructure:** API Gateway, Lambda, DynamoDB, S3, SNS
* **Language:** Python 3.9 (Boto3 SDK), JavaScript (Frontend)
* **Security:** IAM Roles (Least Privilege), CORS Configuration

## 🚀 Key Features

* **RESTful API Design:** Implemented distinct microservices for `POST /ticket` (Creation) and `GET /ticket` (Retrieval).
* **NoSQL Data Modeling:** Designed a DynamoDB schema using unique UUIDs as partition keys for efficient data distribution.
* **Event-Driven Notifications:** Decoupled the notification logic using SNS, ensuring the user gets a fast response while the email sends asynchronously.
* **Serverless Hosting:** Frontend deployed via S3 Static Website Hosting, eliminating the need for web servers like Nginx/Apache.

## 🧠 Challenges & Solutions

### 1. The "Invisible Wall" (CORS)
* **Challenge:** The frontend (hosted on S3) could not talk to the backend (API Gateway) due to browser security policies blocking Cross-Origin requests.
* **Solution:** Configured CORS headers in API Gateway to explicitly allow `GET` and `POST` methods from the S3 bucket's origin.

### 2. Least Privilege Security
* **Challenge:** The Lambda function initially failed to write data.
* **Solution:** Instead of giving full Admin access, I created a custom IAM Role allowing only `dynamodb:PutItem` on the specific table and `sns:Publish` to the specific topic.

## 📂 Project Structure

```text
serverless-incident-manager/
├── backend/
│   ├── create_ticket.py    # Lambda: Ingests data, writes to DB, triggers SNS
│   └── get_tickets.py      # Lambda: Scans DB and returns JSON list
├── frontend/
│   └── index.html          # Client-side code (JS Fetch API)
└── README.md
