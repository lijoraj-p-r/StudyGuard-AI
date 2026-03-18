"""
StudyGuardApp Module
-------------------
The orchestrator of the StudyGuard AI application. This file defines the main 
StudyGuardApp class which manages the flow between different features like 
study sessions, interview prep, and task management.
"""

import sys
from .core import StatsManager, ChatLogger, KNOWN_SUBJECTS
from .ui import UI, Interpreter
from .mentor import Mentor
from .features import StudySession, InterviewPrep, TaskManager, DailyJournal

class StudyGuardApp:
    """
    Main application class that coordinates all system components.
    
    Attributes:
        stats_manager: Handles loading and saving of study statistics.
        logger: Manages the chat history and logging.
        mentor: The AI persona that interacts with the user.
        study_session: Feature for focused study intervals.
        interview_prep: Feature for mock interview questions.
        task_manager: Feature for managing academic checklists.
        journal: Feature for daily documentation of achievements.
    """

    def __init__(self):
        """Initializes the application components and updates the study streak."""
        self.stats_manager = StatsManager()
        self.logger = ChatLogger()
        self.mentor = Mentor(self.logger)
        
        self.study_session = StudySession(self.mentor, self.stats_manager)
        self.interview_prep = InterviewPrep(self.mentor, self.stats_manager)
        self.task_manager = TaskManager(self.mentor, self.stats_manager, self.study_session)
        self.journal = DailyJournal(self.mentor, self.stats_manager)
        
        # Mark the user as active for today
        self.stats_manager.update_streak()

    def start(self):
        """
        Starts the main application loop.
        Displays the dashboard and handles user input via the Interpreter.
        """
        UI.clear_screen()
        print(f"\033[1;38;5;198m◈ STUDYGUARD AI: MODULAR MENTOR ◈\033[0m")
        UI.show_dashboard(self.stats_manager.stats, self.stats_manager.get_rank())
        self.mentor.speak("Welcome back! I'm ready to help you study. What's on the agenda?", "supportive")
        
        while True:
            try:
                user_input = UI.get_input()
                intent, subject = Interpreter.analyze(user_input, KNOWN_SUBJECTS)
                
                # Intent-based routing
                if intent == "exit":
                    if UI.get_input("Would you like to log your achievements for today before leaving? (y/n) › ").lower() == 'y':
                        self.journal.run()
                    self.mentor.speak("Goodbye! Rest well and come back stronger.", "supportive")
                    break
                elif intent == "help":
                    self.mentor.speak("You can say 'Study [Subject]', 'Interview', 'Manage tasks', 'Journal', or 'Dashboard'.", "teacher")
                elif intent == "stats":
                    UI.show_dashboard(self.stats_manager.stats, self.stats_manager.get_rank())
                elif intent == "pending":
                    self.task_manager.run()
                elif intent == "interview":
                    self.interview_prep.run()
                elif intent == "journal":
                    self.journal.run()
                elif intent == "sprint":
                    self.study_session.run(None, is_sprint=True)
                elif intent == "apology":
                    self.mentor.speak("Focus on action, not words. Ready to study?", "supportive")
                elif intent == "gratitude":
                    self.mentor.speak("Happy to help. Keep pushing!", "supportive")
                elif intent == "greeting":
                    self.mentor.speak("Hello! Let's make some progress today.", "supportive")
                elif intent == "distracted":
                    self.mentor.scold()
                elif intent == "studying":
                    self.study_session.run(subject)
                else:
                    self.mentor.speak("Try 'study [subject]', 'interview', or 'tasks'.", "teacher")
                    
            except KeyboardInterrupt:
                # Ensure stats are saved on abrupt exit
                self.stats_manager.save_stats()
                sys.exit()
