"""
User Interface and Input Interpretation Module
----------------------------------------------
Manages the visual presentation in the terminal (colors, typing effects, 
dashboard layout) and the logic to parse user commands into system intents.
"""

import sys
import time
import random
import os
import re

class UI:
    """
    Static class containing terminal UI utilities.
    
    Attributes:
        C: Dictionary of ANSI color and style escape codes.
    """
    
    C = {
        "strict": "\033[1;91m",
        "firm": "\033[38;5;214m",
        "supportive": "\033[38;5;82m",
        "teacher": "\033[38;5;45m",
        "dim": "\033[38;5;240m",
        "reset": "\033[0m",
        "bold": "\033[1m",
        "cyan": "\033[1;36m",
        "gold": "\033[38;5;220m"
    }

    @staticmethod
    def clear_screen():
        """Clears the terminal screen based on the operating system."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def typewriter(text, base_speed=0.015):
        """
        Simulates a human typing effect for the aura's speech.
        
        Args:
            text: The string to be printed.
            base_speed: Delay between characters.
        """
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(max(0.001, base_speed + random.uniform(-0.003, 0.003)))
        print()

    @staticmethod
    def get_input(prompt="You › "):
        """
        Collects user input with a styled prompt.
        
        Returns:
            The trimmed user input string.
        """
        sys.stdout.write(f"{UI.C['cyan']}{UI.C['bold']}{prompt}{UI.C['reset']}")
        sys.stdout.flush()
        return input().strip()

    @staticmethod
    def format_time(seconds):
        """Converts total seconds into a human-readable 'Hh Mm' format."""
        total_m = int(seconds // 60)
        h, m = divmod(total_m, 60)
        return f"{h}h {m}m" if h > 0 else f"{m}m"

    @staticmethod
    def show_dashboard(stats, rank):
        """
        Prints the main visual dashboard with user progress, rank, and expertise.
        
        Args:
            stats: The global stats dictionary.
            rank: The string rank of the user.
        """
        total_time = UI.format_time(stats['lifetime_seconds'])
        print(f"\n{UI.C['dim']}╭──────────────────────────────────────────────────╮")
        print(f"  {UI.C['bold']}RANK: {rank.upper()} | STREAK: {stats['study_streak']} Days")
        print(f"  {UI.C['gold']}Knowledge: {stats['knowledge_points']} KP | Total: {total_time}")
        
        # Determine expertise based on subject with most time spent
        if stats["subject_breakdown"]:
            top = max(stats["subject_breakdown"], key=stats["subject_breakdown"].get)
            print(f"  Expertise: {top.capitalize()}")
        
        # Display only tasks that are not completed
        pending_count = sum(1 for t in stats['pending_tasks'] if t.get('status') == 'pending')
        print(f"  Pending Tasks: {pending_count}")
        print(f"{UI.C['dim']}╰──────────────────────────────────────────────────╯{UI.C['reset']}")

class Interpreter:
    """
    Parses natural language input to determine the user's intended action.
    """

    @staticmethod
    def analyze(user_input, known_subjects):
        """
        Maps user input to a specific 'intent' and optional 'subject'.
        
        Args:
            user_input: The raw string from the user.
            known_subjects: List of valid subjects for session matching.
            
        Returns:
            A tuple of (intent, subject).
        """
        inp = user_input.lower().strip()
        if not inp: return "none", None
        
        # Command Keyword Mapping with typo tolerance
        if any(w in inp for w in ["exit", "quit", "done", "bye", "stop"]): return "exit", None
        if any(w in inp for w in ["stats", "dashboard", "rank", "progress", "score", "kp"]): return "stats", None
        if any(w in inp for w in ["pending", "tasks", "todo", "homework", "check", "list"]): return "pending", None
        if any(w in inp for w in ["help", "guide", "commands", "what can i do"]): return "help", None
        if any(w in inp for w in ["sorry", "apology", "my bad"]): return "apology", None
        if any(w in inp for w in ["thanks", "thank you", "thx", "cool", "great"]): return "gratitude", None
        if any(w in inp for w in ["hello", "hi", "hey", "greet", "morning", "evening"]): return "greeting", None
        if any(w in inp for w in ["interview", "prep", "mock", "question", "inderview", "intrvw"]): return "interview", None
        if any(w in inp for w in ["sprint", "quick", "fast", "10m"]): return "sprint", None
        if any(w in inp for w in ["journal", "log", "diary", "achievement", "today", "done today"]): return "journal", None
        if any(w in inp for w in ["back", "menu", "return", "ok", "next", "continue"]): return "stats", None # Default to dashboard for 'back/ok'

        # Anti-distraction logic
        distractions = ["scroll", "insta", "game", "lazy", "netflix", "youtube", "tiktok", "reels"]
        if any(d in inp for d in distractions): return "distracted", None
        
        # Subject detection logic (more robust)
        study_patterns = ["study", "read", "learn", "start", "ready", "revise", "studdy", "stdy", "revising", "learning"]
        found_subject = None
        
        # 1. Check for explicit subject mentions with boundary check
        for s in known_subjects.keys():
            if re.search(r'\b' + s + r'\b', inp):
                found_subject = s
                break
        
        # 2. Extract subject using expanded regex patterns
        if not found_subject:
            # Matches 'study python', 'let's learn math', 'revision on java'
            patterns = [
                r'(?:study|studying|read|reading|revise|revising|learn|learning|stdy|studdy|on)\s+([a-zA-Z0-9]+)',
                r'^([a-zA-Z0-9]+)$' # Just the subject name
            ]
            for p in patterns:
                match = re.search(p, inp)
                if match:
                    potential = match.group(1)
                    if potential in known_subjects or len(potential) > 2:
                        found_subject = potential
                        break

        if found_subject or any(p in inp for p in study_patterns):
            return "studying", found_subject
            
        return "unknown", None
