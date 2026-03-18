"""
AI Mentor Persona Module
------------------------
Defines the Mentor class which acts as the voice of the application.
It handles user communication with different emotional tones (moods) 
and provides motivation/scolding based on user behavior.
"""

import random
import sys
from .ui import UI

class Mentor:
    """
    The AI Persona that interacts with the user.
    """

    def __init__(self, logger):
        """Initializes the mentor with a reference to the chat logger."""
        self.logger = logger
        self.scold_phrases = [
            "Let's stay focused. Your future self will thank you for this effort.",
            "Distractions are temporary, but knowledge is permanent.",
            "I know you have the potential to master this. Don't let it slip away.",
            "Consistency is the key to success. Shall we try again?",
            "Every minute of focus counts. Let's make this session meaningful.",
            "The path to mastery is built with focus. Stay on it! 🎯",
            "Your brain is a muscle. Give it a workout! 💪",
            "Stop scrolling, start growing. Your potential is waiting. 🚀"
        ]
        
        self.praise_phrases = [
            "One step closer to mastery. Excellent work! 🌟",
            "Your dedication is showing. Keep this momentum! 🔥",
            "Brilliant! That's how a true scholar works. 📚",
            "Consistency is your superpower. Stay strong! 💪",
            "I'm impressed. You're making real progress today. 💎"
        ]

        self.intent_responses = {
            "greeting": [
                "Hello! Ready to conquer some new concepts today?",
                "Welcome back! What shall we master today?",
                "Greetings! I'm ready if you are. Let's get to work.",
                "Hey there! Let's make today a productive one."
            ],
            "help": [
                "You can say 'Study [Subject]', 'Interview', 'Manage tasks', 'Journal', or 'Dashboard'.",
                "I'm here to guide you. Try 'study python', 'view tasks', or check your 'stats'.",
                "Need direction? You can start a 'study' session, do an 'interview', or 'log' your day.",
                "I can help with studying, interview prep, and task management. What's first?"
            ],
            "unknown": [
                "I'm not quite sure I follow. Try 'study [subject]', 'interview', or 'tasks'.",
                "Hmm, that's not in my database. Could you rephrase? Maybe try 'study' or 'stats'.",
                "I didn't catch that. How about we focus on a study session or interview prep?",
                "Let's stick to the plan! You can say 'study', 'interview', or 'pending tasks'."
            ],
            "gratitude": [
                "Happy to help! Keep pushing forward.",
                "You're very welcome. Now, back to greatness!",
                "Anytime. Your growth is my priority.",
                "No problem at all. Let's keep this energy going!"
            ],
            "apology": [
                "No apologies needed. Action is what counts! Ready to focus?",
                "That's fine. Mistakes are part of the journey. What's next?",
                "Focus on the next task, not the last mistake. Ready?",
                "Apology accepted. Let's turn that around with some progress!"
            ]
        }

    def speak(self, text, mood="neutral"):
        """
        Prints a message with a specific mood-based icon and color.
        
        Args:
            text: The message to be spoken.
            mood: The emotional tone (strict, firm, supportive, teacher, neutral).
        """
        self.logger.log("AI", text)
        icons = {"strict": "⚠️", "firm": "💡", "supportive": "🌟", "teacher": "📚", "neutral": "🤖"}
        color = UI.C.get(mood, "")
        icon = icons.get(mood, "🤖")
        sys.stdout.write(f"\n{color}{icon} Mentor › {UI.C['reset']}")
        UI.typewriter(text)

    def scold(self):
        """Randomly selects and speaks a motivational scolding phrase."""
        self.speak(random.choice(self.scold_phrases), "firm")

    def praise(self):
        """Provides a positive reinforcement message."""
        self.speak(random.choice(self.praise_phrases), "supportive")

    def respond(self, intent):
        """Provides a randomized response based on the detected intent."""
        if intent in self.intent_responses:
            self.speak(random.choice(self.intent_responses[intent]), "teacher")
        else:
            self.speak(f"I see. Let's move on to 'study', 'interview', or 'tasks'.", "neutral")
