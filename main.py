"""
Main Entry Point for StudyGuard AI.
This script initializes the StudyGuardApp and starts the main application loop.
"""
from study_guard.app import StudyGuardApp

if __name__ == "__main__":
    # Initialize and start the application
    app = StudyGuardApp()
    app.start()
