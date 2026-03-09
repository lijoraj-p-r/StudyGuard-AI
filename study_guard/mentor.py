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
    
    Attributes:
        logger: Handles logging of AI responses.
        scold_phrases: Collection of motivational prompts used when the user is distracted.
    """

    def __init__(self, logger):
        """Initializes the mentor with a reference to the chat logger."""
        self.logger = logger
        self.scold_phrases = [
            "Let's stay focused. Your future self will thank you for this effort.",
            "Distractions are temporary, but knowledge is permanent.",
            "I know you have the potential to master this. Don't let it slip away.",
            "Consistency is the key to success. Shall we try again?",
            "Every minute of focus counts. Let's make this session meaningful."
        ]

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
        self.speak("One step closer to mastery. Excellent work!", "supportive")
