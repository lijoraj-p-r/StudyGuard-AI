# 🛡️ StudyGuard AI: Your Modular Academic Aura

**StudyGuard AI** is a professional terminal-based study companion designed to optimize academic productivity. Guided by **Aura**, your AI persona, it transforms the solitary experience of studying into an interactive, gamified journey with a focus on long-term retention and career readiness.

---

## 🚀 Enhanced Features

### 📋 Advanced Task Hub
Stay organized with a structured academic checklist that supports:
- **Priority Levels**: Categorize tasks as **High**, **Medium**, or **Low**.
- **Status Tracking**: Toggle between `Pending` and `Completed`.
- **Batch Cleanup**: Instantly clear finished tasks to keep your workspace tidy.
- **Deep Integration**: Launch a focused **Study Session** directly from any task on your list.

### ⏱️ High-Focus Study Sessions
- **Goal-Oriented**: Requires a specific goal for every session to ensure intent-based learning.
- **Dynamic Motivation**: Features a curated list of **Motivational Quotes** that automatically refresh every 60 seconds to maintain high morale.
- **Active Recall**: Mandates a varied summary at the end of every session to solidify memory.
- **Sprint Mode**: A 10-minute "pure focus" mode for quick bursts of productivity.

### 🎓 Interview & Expertise
- **Mock Interviews**: Interactive Q&A sessions covering **Java, Python, SQL, DATABASE, DSA, and Aptitude**.
- **Expert Explanations**: Every question includes a deep-dive "PROFESSIONAL EXPLANATION" to build conceptual clarity.
- **Effort-Based Rewards**: Earn more Knowledge Points (KP) for detailed, thoughtful answers.
- **Progressive Difficulty**: Tracks your expertise and identifies your top subjects based on time investment.

### 📖 Daily Achievement Diary (New!)
- **Journaling**: Document what you did today to stay disciplined and track your growth.
- **History**: View your past achievements to see how far you've come.
- **Exit Prompts**: Aura proactively asks if you'd like to log your day before you leave.

### 🤖 Conversational Aura
- **Natural Language**: Aura understands typos (e.g., "inderview") and natural phrasing.
- **Personality**: Engage in small talk, ask for on-demand motivation, or list available study subjects.
- **Dynamic Responses**: Randomized and varied responses ensure every interaction feels fresh and supportive.

---

## 🛠️ Technical Overview

### Project Architecture
The codebase is modularized for clarity and maintainability:
- **`main.py`**: Application bootstrap and entry point.
- **`study_guard/app.py`**: Core orchestrator and natural language intent interpreter.
- **`study_guard/core.py`**: Data persistence, statistics logic, and knowledge databases.
- **`study_guard/features.py`**: Implementation of Study, Interview, Task, and Journal modules.
- **`study_guard/aura.py`**: AI persona logic with multiple "mood" profiles and randomized styles.
- **`study_guard/ui.py`**: Terminal UI engine (ANSI colors, typewriter effects, live dashboards).

---

## 📖 Quick Start Guide

1. **Launch Aura**:
   ```bash
   python3 main.py
   ```

2. **Common Commands**:
   - `study [subject]` — Start a focused session.
   - `tasks` — Open the Academic Task Hub.
   - `interview` — Start a mock interview.
   - `journal` or `diary` — Log your achievements.
   - `motivation` — Get an instant motivational quote.
   - `subjects` — See what you can study with Aura.
   - `who are you` — Learn about Aura's purpose.
   - `who made you` — Find out about the developer.
   - `dashboard` — View your rank and expertise.
   - `sprint` — Start a 10-minute quick session.

---

## 👤 Who is Aura?
Aura was created by **LijoRaj**, a full-stack developer from India, for study and productivity purposes. It is designed to be a "modular mentor" that combines technical depth with a Gen Z-friendly aesthetic to make studying less of a chore and more of a mission.

---

## 💾 Data Management
- **Statistics**: Persisted in `study_stats.json`.
- **Logs**: Conversation history recorded in `chat_history.json`.
- **Automatic Migration**: The system automatically upgrades older data formats to the latest structured version on startup.
