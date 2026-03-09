# 🛡️ StudyGuard AI: Your Modular Academic Mentor

**StudyGuard AI** is a professional terminal-based study companion designed to optimize academic productivity. It transforms the solitary experience of studying into an interactive, gamified journey with a focus on long-term retention and career readiness.

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
- **Active Recall**: Mandates a one-sentence summary at the end of every session to solidify memory.
- **Sprint Mode**: A 10-minute "pure focus" mode for quick bursts of productivity.

### 🎓 Interview & Expertise
- **Mock Interviews**: Interactive Q&A sessions covering **Java, Python, SQL, DSA, and Aptitude**.
- **Expert Explanations**: Every question includes a deep-dive explanation to build conceptual clarity.
- **Progressive Difficulty**: Tracks your expertise and identifies your top subjects based on time investment.

### 🎮 Gamification & Stats
- **Knowledge Points (KP)**: Earn points based on time studied and session quality.
- **Scholar Ranking**: Level up from **Novice Scholar** to **Master Scholar**.
- **Streaks**: Encourages consistency with a daily study streak tracker.

---

## 🛠️ Technical Overview

### Project Architecture
The codebase is modularized for clarity and maintainability:
- **`main.py`**: Application bootstrap and entry point.
- **`study_guard/app.py`**: Core orchestrator and natural language intent interpreter.
- **`study_guard/core.py`**: Data persistence, statistics logic, and knowledge databases.
- **`study_guard/features.py`**: Implementation of Study, Interview, and Task modules.
- **`study_guard/mentor.py`**: AI persona logic with multiple "mood" profiles.
- **`study_guard/ui.py`**: Terminal UI engine (ANSI colors, typewriter effects, live dashboards).

### Documentation Standard
Every file, class, and method is fully documented with:
- **Module Headers**: Explaining the role of each file in the system.
- **Docstrings**: Detailing class attributes, method parameters, and return types.
- **Technical Comments**: Explaining complex terminal manipulations and data migration paths.

---

## 📖 Quick Start Guide

1. **Launch the Mentor**:
   ```bash
   python3 main.py
   ```

2. **Common Commands**:
   - `study [subject]` — Start a focused session.
   - `tasks` — Open the Academic Task Hub.
   - `interview` — Start a mock interview.
   - `dashboard` — View your rank and expertise.
   - `sprint` — Start a 10-minute quick session.

3. **Task Hub Navigation**:
   - `[A]` — Add a new task with priority.
   - `[T]` — Toggle a task as completed.
   - `[S]` — Select a task and start studying it immediately.
   - `[C]` — Clear all completed tasks.

---

## 💾 Data Management
- **Statistics**: Persisted in `study_stats.json`.
- **Logs**: Conversation history recorded in `chat_history.json`.
- **Automatic Migration**: The system automatically upgrades older data formats to the latest structured version on startup.
