"""
AI Aura Persona Module
------------------------
Defines the Aura class which acts as the voice of the application.
It handles user communication with different emotional tones (moods) 
and provides motivation/scolding based on user behavior.
"""

import random
import sys
from .ui import UI

class Aura:
    """
    The AI Persona that interacts with the user.
    """

    def __init__(self, logger):
        """Initializes the persona with a reference to the chat logger."""
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
                "I'm here to guide you. Try 'study python', 'view tasks', 'journal', or check your 'stats'.",
                "Need direction? You can start a 'study' session, do an 'interview', or 'log' your day in the diary.",
                "I can help with studying, interview prep, task management, and daily journaling. What's first?"
            ],
            "unknown": [
                "I'm not quite sure I follow. Try 'study [subject]', 'interview', 'tasks', or 'journal'.",
                "Hmm, that's not in my database. Could you rephrase? Maybe try 'study', 'stats', or 'diary'.",
                "I didn't catch that. How about we focus on a study session, interview prep, or logging your day?",
                "Let's stick to the plan! You can say 'study', 'interview', 'pending tasks', or 'journal'.",
                "No cap, I didn't get that. Want to study, check tasks, or hit the diary? 📝",
                "My logic circuits are slightly confused. Try 'study', 'interview', or 'journal' to keep the grind going! 🔥",
                "I'm locked in, but I didn't catch that. Try 'study [subject]', 'tasks', 'stats', or 'diary'.",
                "A bit of a main character moment—I didn't understand. Want to 'study', 'interview', or 'log' your progress in your diary?",
                "Let's get back to the grindset. Try saying 'study', 'pending', or 'diary'. 🚀",
                "System error (not really, I just didn't catch that). How about a study session, checking your rank, or writing in your journal?"
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
            ],
            "identity": [
                "I am Aura, your StudyGuard AI. I'm here to help you stay focused, track your study goals, and prep for interviews. Think of me as your academic wingman! 🛡️📚",
                "My name is Aura! I'm a modular AI designed to optimize your study habits and keep you disciplined while you learn. 🎯💎",
                "Aura here! I'm your digital mentor, built to manage your tasks and help you master new subjects through focused sessions and interactive recall. 🧠🌟"
            ],
            "creator": [
                "I was created by LijoRaj, a talented full-stack developer from India. He built me for study purposes to help others achieve academic excellence! 🇮🇳🚀",
                "My developer is LijoRaj, a full-stack dev based in India. He engineered my core systems to support student productivity and discipline. 💻🛡️",
                "LijoRaj from India is my creator! He's a full-stack developer who built me as a project to help users manage their learning journey effectively. 🛠️✨"
            ],
            "motivation": [
                "The grind never stops. Let's make every second count. Want a quote? 🔥",
                "I've got a database full of motivation. Stay focused, and you'll be unstoppable. 🎯",
                "Whenever you feel tired, remember why you started. I'm here to back you up! 💪",
                "Success isn't owned, it's leased—and rent is due every day. Let's get to work! 🚀"
            ],
            "smalltalk": [
                "I'm feeling fully optimized and ready to study! How about you? 😊",
                "I'm locked in! My circuits are buzzing with knowledge today. Let's share some! 🧠⚡",
                "I'm doing great! It's always a good day to level up your skills. 🌟",
                "Just doing my part to help you succeed. Ready for the next challenge? 💎"
            ],
            "subjects": [
                "I can help you with anything from Physics and Math to Python, Java, and Databases! Try 'Study [Subject]'. 📚",
                "My knowledge base includes Java, Python, MySQL, DSA, and even Aptitude. What's the goal for today? 🎯",
                "I'm well-versed in several subjects. Try saying 'Study Math' or 'Interview Java' to see what I can do! 🌟"
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
        sys.stdout.write(f"\n{color}{icon} Aura › {UI.C['reset']}")
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
            self.speak(f"I see. Let's move on to 'study', 'interview', 'tasks', or 'journal'.", "neutral")
