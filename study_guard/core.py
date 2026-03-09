"""
Core Logic and Data Management Module
-------------------------------------
Handles the foundational data structures, persistence, and logic of the system.
Contains the subject databases, interview question pool, motivational quotes,
and manager classes for stats and chat logging.
"""

import json
import os
from datetime import datetime, timedelta

# --- Configuration & Databases ---

# Collection of subjects with unique motivational focus messages.
KNOWN_SUBJECTS = {
    "physics": "Focus on the laws of nature. You've got this!",
    "math": "Logic and precision. Solve one problem at a time.",
    "java": "Think in objects. Debugging is part of the process.",
    "python": "Keep it clean and readable. Code is poetry.",
    "mysql": "Queries are just questions. Get the data!",
    "database": "Structure is everything. Understand normalization.",
    "dsa": "Efficiency is key. Optimize your thinking.",
    "aptitude": "Speed and accuracy. Sharpen your mind.",
    "history": "Understand the past to build the future.",
    "biology": "The science of life. Explore the details.",
    "chemistry": "It's all about the reactions. Stay balanced.",
    "english": "Expression matters. Refine your voice.",
    "economics": "Supply, demand, and logic. Analyze the trends."
}

# Questions and comprehensive explanations for various interview topics.
INTERVIEW_DB = {
    "java": [
        {"q": "What is the difference between JDK, JRE, and JVM?", "a": "The JVM is the engine that executes bytecode. JRE bundles JVM with libraries. JDK is the full toolkit (compiler + debugger + JRE)."},
        {"q": "Explain 'public static void main(String[] args)'.", "a": "Start point: 'Public' is accessible; 'Static' allows the JVM to call it without instantiation; 'Void' returns nothing; 'String[] args' accepts CLI input."},
        {"q": "What is an Abstract Class vs Interface?", "a": "Abstract classes can hold state and concrete methods; Interfaces are blueprints/contracts (only abstract methods/constants in classic Java)."},
        {"q": "How does Garbage Collection work in Java?", "a": "It automatically clears memory by scanning the heap for unreferenced objects, preventing leaks."},
        {"q": "What is the difference between '==' and '.equals()' in Java?", "a": "'==' checks identity (memory address); '.equals()' checks structural equality (content)."},
        {"q": "Explain the 'final', 'finally', and 'finalize' keywords.", "a": "'Final' prevents change; 'Finally' block always runs after try-catch; 'Finalize' is a pre-GC cleanup method (deprecated)."},
        {"q": "What is the Java Collections Framework?", "a": "Standard architecture for storing/manipulating groups of objects (List, Set, Map)."}
    ],
    "python": [
        {"q": "What is the difference between List and Tuple?", "a": "Lists are mutable (changeable whiteboards); Tuples are immutable (stone tablets). Tuples are faster."},
        {"q": "What is a Decorator in Python?", "a": "A function that wraps another to extend its behavior without modifying the source (like gift wrap)."},
        {"q": "Explain PEP 8.", "a": "The official style guide for Python code formatting, ensuring readability."},
        {"q": "How is memory managed in Python?", "a": "Via a private heap, reference counting, and a cyclic garbage collector."},
        {"q": "What are Python Generators and why use them?", "a": "Lazy iterators that yield items one by one, saving memory for large datasets."},
        {"q": "What is the difference between 'is' and '=='?", "a": "'==' compares value; 'is' compares identity (memory location)."},
        {"q": "Explain List Comprehension in Python.", "a": "An elegant, one-line way to create lists based on existing iterables."}
    ],
    "mysql": [
        {"q": "What is the difference between DELETE and TRUNCATE?", "a": "DELETE is DML (surgical, rollable-back); TRUNCATE is DDL (resets table, faster, no undo)."},
        {"q": "What are Joins and their types?", "a": "Methods to link tables. Inner (matches both), Left (all left + matches), etc."},
        {"q": "What is an Index and why is it used?", "a": "Data structure to speed up data retrieval (like a book index)."},
        {"q": "What is a Primary Key vs Unique Key?", "a": "Primary Key (unique, no nulls, one per table); Unique Key (unique, allows one null)."},
        {"q": "What is the difference between 'GROUP BY' and 'ORDER BY'?", "a": "Group By aggregates/summarizes data; Order By sorts it."},
        {"q": "Explain 'UNION' vs 'UNION ALL' in MySQL.", "a": "UNION removes duplicates; UNION ALL keeps them and is faster."},
        {"q": "What are Aggregate Functions in MySQL?", "a": "Calculations on sets of values returning one value (COUNT, SUM, AVG, MAX)."}
    ],
    "database": [
        {"q": "What is Database Normalization?", "a": "Organizing data to reduce redundancy and improve integrity."},
        {"q": "Explain ACID properties.", "a": "Atomicity, Consistency, Isolation, Durability – the gold standard for reliable transactions."},
        {"q": "What is a Foreign Key?", "a": "A column that links to a Primary Key in another table, enforcing referential integrity."},
        {"q": "Explain NoSQL vs SQL.", "a": "SQL (relational, fixed schema); NoSQL (flexible, document/key-value, horizontally scalable)."},
        {"q": "What is a Database Transaction?", "a": "A single unit of work (all-or-nothing)."},
        {"q": "Explain Data Integrity and its types.", "a": "Accuracy/consistency (Entity, Domain, and Referential Integrity)."},
        {"q": "What is the CAP Theorem?", "a": "Consistency, Availability, and Partition Tolerance – pick two in a distributed system."}
    ],
    "aptitude": [
        {"q": "A train 150m long crosses a pole in 9s. Speed?", "a": "150/9 = 16.67 m/s (60 km/h)."},
        {"q": "5 workers take 12 days. 10 workers?", "a": "Inverse proportion: double workers = half time (6 days)."},
        {"q": "Probability of sum of 7 on 2 dice?", "a": "6 combinations (1,6; 2,5; 3,4...) out of 36 = 1/6."},
        {"q": "Item sold for $120 (20% profit). Cost?", "a": "1.2 * Cost = 120 -> Cost = $100."},
        {"q": "A (10d) and B (15d) work together?", "a": "Rates: 1/10 + 1/15 = 5/30 = 1/6 -> 6 days."},
        {"q": "How to calculate 15% of 200 mentally?", "a": "10% is 20, 5% is 10. Total 30."}
    ]
}

# Inspirational quotes that rotate every minute during study sessions.
MOTIVATIONAL_QUOTES = [
    "The only way to do great work is to love what you do. — Steve Jobs",
    "Don't stop when you're tired. Stop when you're done.",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. — Winston Churchill",
    "Believe you can and you're halfway there. — Theodore Roosevelt",
    "It always seems impossible until it's done. — Nelson Mandela",
    "Your focus determines your reality. — Qui-Gon Jinn",
    "The expert in anything was once a beginner. — Helen Hayes",
    "Focus on being productive instead of busy. — Tim Ferriss",
    "Small steps in the right direction can turn out to be the biggest steps of your life.",
    "The secret of getting ahead is getting started. — Mark Twain",
    "You don't have to be great to start, but you have to start to be great. — Zig Ziglar",
    "Study while others are sleeping; work while others are loafing; prepare while others are playing; and dream while others are reaching. — William Arthur Ward"
]

# --- Data Management ---

class StatsManager:
    """
    Manages the persistence and updates of user statistics.
    
    Attributes:
        stats_file: Path to the JSON file for data storage.
        stats: Dictionary containing points, time, streak, and tasks.
    """
    
    def __init__(self, stats_file="study_stats.json"):
        """Initializes the manager and loads existing stats."""
        self.stats_file = stats_file
        self.stats = {
            "lifetime_seconds": 0,
            "knowledge_points": 0,
            "study_streak": 0,
            "last_study_date": None,
            "subject_breakdown": {},
            "pending_tasks": [],
            "summary_history": []
        }
        self.load_stats()
        self._migrate_tasks()

    def _migrate_tasks(self):
        """Migrates old string-based tasks to the new structured format."""
        updated = False
        new_tasks = []
        for task in self.stats.get("pending_tasks", []):
            if isinstance(task, str):
                new_tasks.append({
                    "id": len(new_tasks) + 1,
                    "text": task,
                    "priority": "Medium",
                    "due_date": None,
                    "status": "pending",
                    "created_at": datetime.now().strftime("%Y-%m-%d")
                })
                updated = True
            else:
                new_tasks.append(task)
        
        if updated:
            self.stats["pending_tasks"] = new_tasks
            self.save_stats()

    def load_stats(self):
        """Loads data from the JSON file."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats.update(json.load(f))
            except: pass

    def save_stats(self):
        """Saves current statistics to the JSON file using an atomic swap."""
        try:
            temp_file = self.stats_file + ".tmp"
            with open(temp_file, 'w') as f:
                json.dump(self.stats, f, indent=4)
            os.replace(temp_file, self.stats_file)
        except: pass

    def update_streak(self):
        """Calculates and updates the daily study streak."""
        today = datetime.now().strftime("%Y-%m-%d")
        last = self.stats["last_study_date"]
        if last == today: return
        if last:
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            self.stats["study_streak"] = self.stats["study_streak"] + 1 if last == yesterday else 1
        else:
            self.stats["study_streak"] = 1
        self.stats["last_study_date"] = today
        self.save_stats()

    def get_rank(self):
        """Returns the user's rank based on Knowledge Points (KP)."""
        kp = self.stats["knowledge_points"]
        if kp < 100: return "Novice Scholar"
        if kp < 500: return "Dedicated Student"
        if kp < 1500: return "Honor Student"
        return "Master Scholar"

class ChatLogger:
    """
    Maintains a record of interactions between the AI and user.
    """
    
    def __init__(self, log_file="chat_history.json"):
        """Initializes the logger path."""
        self.log_file = log_file

    def log(self, role, message):
        """Appends a new entry to the chat log file."""
        log_entry = {"timestamp": str(datetime.now()), "role": role, "message": message}
        try:
            logs = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f: logs = json.load(f)
            logs.append(log_entry)
            with open(self.log_file, 'w') as f: json.dump(logs, f, indent=4)
        except: pass
