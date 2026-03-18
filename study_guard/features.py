"""
Feature Implementation Module
---------------------------
Contains the core functional modules of the application:
1. StudySession: Handles timed focus sessions with goal tracking and point rewards.
2. InterviewPrep: Provides interactive mock interview questions.
3. TaskManager: Manages a structured academic checklist.
"""

import time
import random
import sys
from datetime import datetime
from .ui import UI
from .core import INTERVIEW_DB, KNOWN_SUBJECTS, MOTIVATIONAL_QUOTES

class StudySession:
    """
    Manages a focused study period where the user tracks a specific goal.
    
    Attributes:
        mentor: The AI mentor for feedback and encouragement.
        stats_manager: For updating KP and study time.
    """

    def __init__(self, mentor, stats_manager):
        """Initializes the study session with necessary managers."""
        self.mentor = mentor
        self.stats_manager = stats_manager

    def run(self, subject, is_sprint=False):
        """
        Executes the main study loop.
        
        Args:
            subject: The topic being studied.
            is_sprint: If True, the session is capped at 10 minutes.
        """
        subject = subject or "General Revision"
        UI.clear_screen()
        self.mentor.speak(f"Session: {subject.upper()}", "teacher")
        
        # Display subject-specific encouragement if known
        if subject.lower() in KNOWN_SUBJECTS:
            self.mentor.speak(KNOWN_SUBJECTS[subject.lower()], "supportive")
        
        # Force the user to set a specific goal
        while True:
            goal = UI.get_input("What is your ONE specific goal for this session? › ")
            if len(goal) < 3 or any(w in goal.lower() for w in ["nothing", "none", "idk"]):
                self.mentor.speak("A specific goal keeps your mind sharp. Try something like 'Read 3 pages' or 'Solve 5 problems'.", "firm")
            else: break
            
        self.mentor.speak(f"Target locked: '{goal}'. Focus mode active.", "supportive")
        if is_sprint: self.mentor.speak("SPRINT MODE: 10 minutes of pure focus. Let's go!", "firm")
        
        start_time = datetime.now()
        current_quote = random.choice(MOTIVATIONAL_QUOTES)
        print(f"\n  {UI.C['dim']}💡 {current_quote}{UI.C['reset']}")
        
        try:
            while True:
                delta = (datetime.now() - start_time).total_seconds()
                m, s = divmod(int(delta), 60)
                
                # Refresh motivational quote every 1 minute
                if s == 0 and delta >= 60:
                    current_quote = random.choice(MOTIVATIONAL_QUOTES)
                    sys.stdout.write(f"\033[F\033[K  {UI.C['dim']}💡 {current_quote}{UI.C['reset']}\n")
                
                # Live Timer Display
                sys.stdout.write(f"\r  {UI.C['bold']}📚 {subject.upper()} | {m}m {s}s{UI.C['reset']} | Goal: {goal} (Ctrl+C when done) \033[K")
                sys.stdout.flush()
                time.sleep(1)
                if is_sprint and m >= 10: break
        except KeyboardInterrupt: pass # Normal exit on Ctrl+C
        
        self.process_end(subject, (datetime.now() - start_time).total_seconds(), goal)

    def process_end(self, subject, duration, goal):
        """
        Handles post-session logic: rewards KP, updates stats, and asks for a summary.
        
        Args:
            subject: The topic studied.
            duration: Total seconds elapsed.
            goal: The goal set at the start.
        """
        UI.clear_screen()
        mins = int(duration // 60)
        self.stats_manager.stats["lifetime_seconds"] += duration
        
        # Update breakdown for specific subjects
        clean_sub = subject.split()[0].lower()
        self.stats_manager.stats["subject_breakdown"][clean_sub] = self.stats_manager.stats["subject_breakdown"].get(clean_sub, 0) + duration
        
        self.mentor.speak(f"Well done. You spent {mins} minutes on your studies.", "supportive")
        
        # Force active recall with a variety of prompts
        recall_prompts = [
            "In one sentence, what's the most important thing you just learned? › ",
            "What's one key takeaway from this session? › ",
            "If you had to explain this to a friend, what would you say? › ",
            "Summarize your main breakthrough from this session. › ",
            "What's the one thing that clicked for you just now? › "
        ]
        
        while True:
            summary = UI.get_input(random.choice(recall_prompts))
            if len(summary) < 5 or any(w in summary.lower() for w in ["nothing", "forgot", "idk", "none"]):
                self.mentor.speak("Active recall is vital! What's one thing you remember?", "firm")
            else: break
            
        self.stats_manager.stats["summary_history"].append({"date": str(datetime.now()), "sub": subject, "sum": summary})
        
        # Knowledge Points (KP) Logic
        bonus_kp = 0
        if mins >= 60: bonus_kp = 50
        elif mins >= 45: bonus_kp = 30
        elif mins >= 25: bonus_kp = 15
        
        total_kp = (mins * 5) + bonus_kp
        self.stats_manager.stats["knowledge_points"] += total_kp
        self.stats_manager.save_stats()
        self.mentor.speak(f"Session finished. +{total_kp} KP earned.", "supportive")

class InterviewPrep:
    """
    Facilitates a mock interview session.
    """

    def __init__(self, mentor, stats_manager):
        """Initializes the interview manager."""
        self.mentor = mentor
        self.stats_manager = stats_manager

    def run(self):
        """Starts the interactive interview loop."""
        UI.clear_screen()
        self.mentor.speak("INTERVIEW PREP MODE: Let's sharpen your career skills.", "teacher")
        subjects = list(INTERVIEW_DB.keys())
        
        self.mentor.speak(f"Available Subjects: {', '.join([s.upper() for s in subjects])}", "teacher")
        choice = UI.get_input("Which subject? (or 'exit') › ").lower()
        if "exit" in choice: return
        
        # Subject matching logic
        if choice not in INTERVIEW_DB:
            matches = [s for s in subjects if s in choice]
            choice = matches[0] if matches else random.choice(subjects)
        
        self.mentor.speak(f"TARGET LOCKED: {choice.upper()}. Type 'exit' to finish.", "supportive")
        asked = []
        
        while True:
            available = [i for i in INTERVIEW_DB[choice] if i['q'] not in asked]
            if not available: asked = []; available = INTERVIEW_DB[choice]
            
            item = random.choice(available)
            asked.append(item['q'])
            
            self.mentor.speak(f"QUESTION: {item['q']}", "teacher")
            user_ans = UI.get_input("Your Answer › ")
            if "exit" in user_ans.lower(): break
            
            # Constructive feedback and points based on effort
            if len(user_ans) < 15:
                self.mentor.speak("That's a bit brief for an interview. Try to be more descriptive next time!", "firm")
                earned_kp = 5
            elif len(user_ans) > 50:
                self.mentor.speak("Excellent level of detail. This kind of thoroughness impresses recruiters!", "supportive")
                earned_kp = 15
            else:
                earned_kp = 10

            # Show the expert explanation
            print(f"\n  {UI.C['bold']}PROFESSIONAL EXPLANATION:{UI.C['reset']}")
            UI.typewriter(item['a'])
            
            self.stats_manager.stats["knowledge_points"] += earned_kp
            self.stats_manager.save_stats()
            
            cont = UI.get_input(f"\n{UI.C['dim']}Continue to next question? (y/n) › {UI.C['reset']}")
            if cont.lower() != 'y': break
            UI.clear_screen()

class TaskManager:
    """
    Manages a persistent, structured checklist of academic tasks.
    """

    def __init__(self, mentor, stats_manager, study_session):
        """Initializes the task manager with session cross-links."""
        self.mentor = mentor
        self.stats_manager = stats_manager
        self.study_session = study_session

    def run(self):
        """Main loop for task management (Add, Delete, Toggle, Study)."""
        while True:
            UI.clear_screen()
            self.mentor.speak("Academic Task Hub", "teacher")
            tasks = self.stats_manager.stats["pending_tasks"]
            
            # Table Display
            if not tasks:
                print(f"\n  {UI.C['dim']}(No tasks found. Add some to stay organized.){UI.C['reset']}")
            else:
                print(f"\n  {UI.C['bold']}{'#':<3} {'Task':<25} {'Priority':<10} {'Status':<10}{UI.C['reset']}")
                print(f"  {UI.C['dim']}{'-'*50}{UI.C['reset']}")
                
                for i, t in enumerate(tasks, 1):
                    p_color = UI.C['strict'] if t['priority'] == 'High' else (UI.C['firm'] if t['priority'] == 'Medium' else UI.C['dim'])
                    s_color = UI.C['supportive'] if t['status'] == 'completed' else UI.C['firm']
                    status_icon = "✓" if t['status'] == 'completed' else "…"
                    
                    print(f"  {UI.C['cyan']}{i:<3}{UI.C['reset']} {t['text'][:25]:<25} {p_color}{t['priority']:<10}{UI.C['reset']} {s_color}{status_icon} {t['status'].capitalize():<10}{UI.C['reset']}")
            
            print(f"\n{UI.C['dim']}[A]dd | [D]elete | [S]tudy | [T]oggle | [C]lear Completed | [B]ack{UI.C['reset']}")
            c = UI.get_input().lower()
            
            if any(w in c for w in ['a', 'add']):
                t_text = UI.get_input("Task Description › ")
                if t_text:
                    priority = UI.get_input("Priority ([H]igh/[M]ed/[L]ow) › ").lower()
                    p_map = {'h': 'High', 'm': 'Medium', 'l': 'Low'}
                    p_val = p_map.get(priority[0] if priority else 'm', 'Medium')
                    
                    new_task = {
                        "text": t_text,
                        "priority": p_val,
                        "status": "pending",
                        "created_at": datetime.now().strftime("%Y-%m-%d")
                    }
                    self.stats_manager.stats["pending_tasks"].append(new_task)
                    self.stats_manager.save_stats()
            
            elif any(w in c for w in ['d', 'delete']) and tasks:
                val = UI.get_input("Task # to delete › ")
                if val.isdigit() and 0 < int(val) <= len(tasks):
                    self.stats_manager.stats["pending_tasks"].pop(int(val)-1)
                    self.stats_manager.save_stats()
            
            elif any(w in c for w in ['t', 'toggle']) and tasks:
                val = UI.get_input("Task # to toggle › ")
                if val.isdigit() and 0 < int(val) <= len(tasks):
                    task = self.stats_manager.stats["pending_tasks"][int(val)-1]
                    task['status'] = 'completed' if task['status'] == 'pending' else 'pending'
                    self.stats_manager.save_stats()
                    
            elif any(w in c for w in ['c', 'clear']) and tasks:
                self.stats_manager.stats["pending_tasks"] = [t for t in tasks if t['status'] == 'pending']
                self.stats_manager.save_stats()
                
            elif any(w in c for w in ['s', 'study']) and tasks:
                val = UI.get_input("Task # to focus on › ")
                if val.isdigit() and 0 < int(val) <= len(tasks):
                    # Launch a study session directly from a task
                    self.study_session.run(self.stats_manager.stats["pending_tasks"][int(val)-1]['text'])
            
            elif any(w in c for w in ['b', 'back']):
                break

class DailyJournal:
    """
    Manages a daily achievement log where users document their progress.
    """

    def __init__(self, mentor, stats_manager):
        """Initializes the journal manager."""
        self.mentor = mentor
        self.stats_manager = stats_manager

    def run(self):
        """Main loop for documenting achievements."""
        while True:
            UI.clear_screen()
            self.mentor.speak("DAILY LOG: What did you achieve today?", "teacher")
            logs = self.stats_manager.stats.get("daily_logs", [])
            
            # Display recent logs (last 5)
            if logs:
                print(f"\n  {UI.C['bold']}Recent Log Entries:{UI.C['reset']}")
                for l in logs[-5:]:
                    print(f"  {UI.C['dim']}[{l['date'][:10]}]{UI.C['reset']} {l['achievement']}")
            else:
                print(f"\n  {UI.C['dim']}(No entries yet. Start documenting your growth.){UI.C['reset']}")
            
            print(f"\n{UI.C['dim']}[A]dd Entry | [V]iew History | [B]ack{UI.C['reset']}")
            c = UI.get_input().lower()
            
            if any(w in c for w in ['a', 'add']):
                achievement = UI.get_input("What did you do today? › ")
                if len(achievement) > 3:
                    entry = {
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "achievement": achievement
                    }
                    if "daily_logs" not in self.stats_manager.stats:
                        self.stats_manager.stats["daily_logs"] = []
                    self.stats_manager.stats["daily_logs"].append(entry)
                    self.stats_manager.save_stats()
                    self.mentor.speak("Achievement recorded. Documentation is key to discipline.", "supportive")
                else:
                    self.mentor.speak("Be more specific. Every bit of progress counts.", "firm")
            
            elif any(w in c for w in ['v', 'view']):
                UI.clear_screen()
                self.mentor.speak("FULL LOG HISTORY", "teacher")
                for l in reversed(logs):
                    print(f"  {UI.C['dim']}[{l['date']}]{UI.C['reset']} {l['achievement']}")
                UI.get_input("\nPress Enter to return...")
            
            elif any(w in c for w in ['b', 'back']):
                break
