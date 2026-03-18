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
from .aura import Aura
from .features import StudySession, InterviewPrep, TaskManager, DailyJournal

class StudyGuardApp:
    """
    Main application class that coordinates all system components.
    
    Attributes:
        stats_manager: Handles loading and saving of study statistics.
        logger: Manages the chat history and logging.
        aura: The AI persona that interacts with the user.
        study_session: Feature for focused study intervals.
        interview_prep: Feature for mock interview questions.
        task_manager: Feature for managing academic checklists.
        journal: Feature for daily documentation of achievements.
    """

    def __init__(self):
        """Initializes the application components and updates the study streak."""
        self.stats_manager = StatsManager()
        self.logger = ChatLogger()
        self.aura = Aura(self.logger)
        
        self.study_session = StudySession(self.aura, self.stats_manager)
        self.interview_prep = InterviewPrep(self.aura, self.stats_manager)
        self.task_manager = TaskManager(self.aura, self.stats_manager, self.study_session)
        self.journal = DailyJournal(self.aura, self.stats_manager)
        
        # Mark the user as active for today
        self.stats_manager.update_streak()

    def start(self):
        """
        Starts the main application loop.
        Displays the dashboard and handles user input via the Interpreter.
        """
        UI.clear_screen()
        print(f"\033[1;38;5;198m◈ STUDYGUARD AI: MODULAR AURA ◈\033[0m")
        UI.show_dashboard(self.stats_manager.stats, self.stats_manager.get_rank())
        self.aura.speak("Welcome back! I'm ready to help you study. What's on the agenda?", "supportive")
        
        while True:
            try:
                user_input = UI.get_input()
                intent, subject = Interpreter.analyze(user_input, KNOWN_SUBJECTS)
                
                # Intent-based routing
                if intent == "exit":
                    if UI.get_input("Would you like to log your achievements for today before leaving? (y/n) › ").lower() == 'y':
                        self.journal.run()
                    self.aura.speak("Goodbye! Rest well and come back stronger.", "supportive")
                    break
                elif intent == "help":
                    self.aura.respond("help")
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
                elif intent in ["apology", "gratitude", "greeting"]:
                    self.aura.respond(intent)
                elif intent == "distracted":
                    self.aura.scold()
                elif intent == "studying":
                    self.study_session.run(subject)
                else:
                    self.aura.respond("unknown")
                    
            except KeyboardInterrupt:
                # Ensure stats are saved on abrupt exit
                self.stats_manager.save_stats()
                sys.exit()
