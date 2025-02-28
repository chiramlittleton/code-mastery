# Code Mastery

## Overview
Code Mastery is an **AI-powered coding proficiency platform** that provides **interactive learning**, **adaptive problem-solving**, and **skill tracking** using **FastAPI, React, and ChromaDB**. It helps developers enhance their coding skills by offering **AI-generated challenges**, **real-time feedback**, and **personalized recommendations**.

## **Architecture**
Code Mastery is designed as a **microservices-based architecture**, ensuring **scalability, modularity, and performance**. The system consists of multiple components that handle **problem generation, user submissions, AI-powered feedback, and data persistence**.

### **Architecture Diagram**
```mermaid
graph TD;
    A[Frontend (React)] -->|Requests| B[Backend API (FastAPI)];
    B -->|Fetches Problems| C[Question Generator (AI)];
    B -->|Stores User Data| D[PostgreSQL (User DB)];
    B -->|Embeddings Search| E[ChromaDB (Vector Storage)];
    B -->|Stores Code Submissions| F[Redis (Cache)];
```

### **Components**
#### **1️⃣ Frontend (React + TypeScript)**
- Built using **React and TypeScript** for an interactive UI.
- Communicates with the backend via **REST API & WebSockets**.
- Provides **real-time problem-solving and skill tracking**.

#### **2️⃣ Backend API (FastAPI)**
- Manages **user authentication, code evaluation, and progress tracking**.
- Serves problems from the AI-powered generator.
- Handles **submission grading and AI feedback**.

#### **3️⃣ Question Generator (AI)**
- Generates **custom coding challenges** based on skill level.
- Uses **GPT-based AI models** to create problem variations.
- Supports multiple programming languages.

#### **4️⃣ Database Layer**
- **PostgreSQL** stores **user progress, problem history, and scores**.
- **ChromaDB (Vector Database)** enables **efficient AI-powered search**.
- **Redis** caches frequently accessed user data for low-latency access.

## **Getting Started**

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/code-mastery.git
cd code-mastery
```

### 2️⃣ Build and Run with Docker Compose
```sh
docker compose up --build -d
```

### 3️⃣ Apply Database Migrations
```sh
docker compose exec backend alembic upgrade head
```

### 4️⃣ Test Health Check
```sh
curl -X GET http://localhost:8000/health
```

## **Environment Variables**
| Variable | Description |
|----------|------------|
| `PORT` | The port on which the FastAPI backend runs (default `8000`) |
| `DATABASE_URL` | PostgreSQL connection string |
| `VECTOR_DB_URL` | ChromaDB connection string |
| `AI_API_KEY` | API key for AI-powered problem generation |

## **Contributing**
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## **License**
This project is licensed under the MIT License - see the LICENSE file for details.

## **Contact**
For any questions or issues, please reach out to `chiram.littleton@gmail.com` or open an issue on GitHub.

