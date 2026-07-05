 # 🚀 CareerForge AI

> **A Multi-Agent Career Development Platform built with Google Agent Development Kit (Google ADK)**

CareerForge AI is an intelligent multi-agent platform that helps students and aspiring software engineers prepare for internships and entry-level software engineering roles through personalized AI-powered career guidance.

Using multiple specialized AI agents, the platform generates personalized learning roadmaps, recommends portfolio projects, reviews resumes, prepares users for technical interviews, and tracks learning progress.

---

# 📌 Problem Statement

Students preparing for software engineering careers often struggle with:

- Choosing the right technologies to learn
- Building industry-relevant portfolio projects
- Creating ATS-friendly resumes
- Preparing for technical interviews
- Following a structured learning roadmap

CareerForge AI solves these challenges through collaborative AI agents that work together to provide personalized career guidance.

---

# ✨ Features

- 🤖 Multi-Agent Architecture using Google ADK
- 🛡️ Security Checkpoint for Prompt Injection Detection
- 📚 Personalized Learning Roadmaps
- 💻 Portfolio Project Recommendations
- 📄 Resume Review & Suggestions
- 🎯 Technical & Behavioral Interview Preparation
- 📈 Learning Progress Tracking
- 🔧 MCP Server Integration
- 🌐 Interactive Google ADK Web Interface

---

# 🏗️ System Architecture

```
                     User
                       │
                       ▼
            Security Checkpoint
                       │
                       ▼
              Orchestrator Agent
                       │
 ┌────────────┬─────────────┬────────────┐
 │            │             │            │
Planner   Learning     Resume      Interview
 Agent      Agent        Agent         Agent
 │
 │
Project Agent
 │
Progress Agent
 │
 ▼
MCP Server
 │
 ▼
Personalized Career Guidance
```

---

# 🤖 AI Agents

### 🎯 Orchestrator Agent
Coordinates the workflow and routes every request to the appropriate specialist agent.

### 🗺️ Planner Agent
Creates personalized career roadmaps.

### 📚 Learning Agent
Recommends learning resources and study plans.

### 💻 Project Agent
Suggests real-world portfolio projects.

### 📄 Resume Agent
Analyzes resumes and provides improvement suggestions.

### 🎤 Interview Agent
Generates technical and behavioral interview practice.

### 📈 Progress Agent
Tracks completed milestones and recommends next learning goals.

---

# 🔒 Security

Every user request passes through a Security Checkpoint that performs:

- Prompt Injection Detection
- Input Validation
- Secure Request Routing
- Security Monitoring

---

# 🔧 MCP Server

The integrated MCP Server provides reusable tools for:

- Career Resources
- Learning Recommendations
- Interview Questions
- Portfolio Projects
- Career Roadmaps

---

# 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| AI Framework | Google Agent Development Kit (Google ADK) |
| Backend | Python, FastAPI |
| Frontend | Google ADK Web UI |
| AI Model | Google Gemini |
| Protocol | MCP (Model Context Protocol) |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```
careerforge-ai/
├── app/
│   ├── agent.py
│   ├── fast_api_app.py
│   └── app_utils/
├── tests/
├── deployment/
├── GEMINI.md
├── pyproject.toml
├── Dockerfile
├── README.md
└── agents-cli-manifest.yaml
```

---

# 🚀 Getting Started

## Prerequisites

Before running the project, install:

- Python 3.11+
- uv
- Google Agent Development Kit (ADK)
- Google Gemini API Key

---

## Clone Repository

```bash
git clone https://github.com/Harishni-TechWorld/CareerForgeAI-Capstone.git

cd CareerForgeAI-Capstone
```

---

## Install Dependencies

```bash
uv sync
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Run the Application

Start the Google ADK server.

```bash
uv run adk web
```

---

## 🌐 Open the Application

After the server starts successfully, open the Google ADK Web Interface:

```
http://localhost:18081
```

---

# 📋 Useful Commands

| Command | Description |
|----------|-------------|
| `uv sync` | Install dependencies |
| `uv run adk web` | Start CareerForge AI |
| `uv run pytest tests` | Run tests |

---

# 🎥 Demo

CareerForge AI demonstrates:

- Multi-Agent Collaboration
- Secure AI Workflows
- Personalized Career Roadmaps
- Resume Analysis
- Interview Preparation
- Portfolio Project Recommendations
- MCP Server Integration

---

# 🚀 Future Improvements

- Authentication
- Resume Upload
- Persistent User Profiles
- Cloud Deployment
- Analytics Dashboard
- Real-time Progress Tracking

---

# 👩‍💻 Author

**Harishni C**

Google Agent Development Kit (Google ADK) Capstone Project

---

# 🙏 Acknowledgements

This project was built using:

- Google Agent Development Kit (Google ADK)
- Google Gemini
- FastAPI
- Python
- MCP (Model Context Protocol)

---

# 📜 License

This project is licensed under the MIT License.
