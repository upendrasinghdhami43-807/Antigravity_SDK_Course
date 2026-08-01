# Google Antigravity SDK Mastery Course 🚀

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OS](https://img.shields.io/badge/OS-Linux%20%7C%20macOS-green)

**🔗 GitHub Repository:** [https://github.com/upendrasinghdhami43-807/Antigravity_SDK_Course](https://github.com/upendrasinghdhami43-807/Antigravity_SDK_Course)


Welcome to the **Google Antigravity SDK Mastery Course**! This repository is a comprehensive, from-scratch bootcamp designed to take you from learning basic SDK usage to becoming a professional **AI Agent Engineer**.

Instead of isolated examples, this course builds production-grade applications from first principles, culminating in autonomous agents, multi-agent systems, and real-time streaming AI applications.

---

## 📖 Curriculum Overview

The course is divided into three distinct phases. 

### ✅ Phase 1: SDK Fundamentals (Completed)
This phase introduces the core concepts of building AI agents, managing state, and rendering tokens in real-time.

* **[Module 1: Hello Agent](./01_hello_agent/)** - Basic SDK usage, prompt execution, async generation, and error handling.
* **[Module 2: Interactive Chat](./02_interactive_chat/)** - Building a persistent CLI chat loop with graceful exits and input validation.
* **[Module 3: Conversation Memory](./03_conversation_memory/)** - Advanced state management, automatic summarization, and extracting facts to a long-term JSON memory.
* **[Module 4: Streaming API Pro](./04_streaming_pro/)** - A complete asynchronous architecture replicating ChatGPT's live typewriter effect, featuring token-by-token rendering, TTFB latency tracking, and interrupt (Ctrl+C) handling.

### 🚧 Phase 2: Autonomous Agents (In Progress)
* *Module 5: Tool Calling & Actions* (Coming Soon)
* *Module 6: RAG & Vector Databases* (Coming Soon)
* *Module 7: The Planning Agent* (Coming Soon)

### 🚧 Phase 3: Multi-Agent Systems
* *Advanced multi-agent orchestration projects* (Coming Soon)

---

## 🛠️ Getting Started (Cloning & Setup)

To use these projects locally, you will need **Python 3.10+** and a **Linux or macOS** environment.

### 1. Clone the Repository
```bash
git clone https://github.com/upendrasinghdhami43-807/Antigravity_SDK_Course.git
cd Antigravity_SDK_Course
```

### 2. Set Up the Environment
Each module is a standalone project. Navigate to the module you want to run (e.g., Module 4) and set up the virtual environment:
```bash
cd 04_streaming_pro
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Add Your API Key
Create a `.env` file in the module directory and add your Google Gemini API key:
```env
GEMINI_API_KEY="your_api_key_here"
```

### 4. Run the Application
```bash
python3 -m app.main
```

---

## 🎯 Use Cases
This repository serves as both a learning tool and a boilerplate for real-world projects. You can use the code here to:
- Build **Terminal-based ChatGPT alternatives** tailored to your workflow.
- Create **Personal AI Assistants** that remember your preferences across sessions.
- Learn **Production AI patterns** (Async streams, Token limit management, graceful degradation).
- Scaffold the foundation for complex **Autonomous Agents**.

---

## 🤝 Contributing
We welcome contributions! Whether it's fixing a bug, adding a new feature, or improving documentation. 

Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for detailed guidelines on how to submit pull requests and report issues.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
