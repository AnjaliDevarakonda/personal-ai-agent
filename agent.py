import json
import os
from datetime import datetime

class PersonalAssistant:
    def __init__(self):
        self.name = "Assistant"
        self.user_name = None
        self.memory = []
        self.topics = set()
        self.mood = "neutral"
        self.chat_history = []
        self.conversation_count = 0
        
        # Load saved memory if exists
        self.load_memory()
    
    def load_memory(self):
        """Load saved memory from file"""
        if os.path.exists("memory.json"):
            try:
                with open("memory.json", "r") as f:
                    data = json.load(f)
                    self.user_name = data.get("user_name")
                    self.topics = set(data.get("topics", []))
                    self.memory = data.get("memory", [])
                    print("📂 Memory loaded successfully!")
            except:
                print("⚠️ Could not load memory, starting fresh.")
    
    def save_memory(self):
        """Save memory to file"""
        data = {
            "user_name": self.user_name,
            "topics": list(self.topics),
            "memory": self.memory
        }
        with open("memory.json", "w") as f:
            json.dump(data, f, indent=2)
        print("💾 Memory saved!")
    
    def save_chat(self):
        """Save chat history to a text file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_log_{timestamp}.txt"
        with open(filename, "w") as f:
            f.write(f"Chat Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n")
            for entry in self.chat_history:
                f.write(f"{entry}\n")
        print(f"💾 Chat saved to {filename}")
    
    def respond(self, user_input):
        """Generate a response based on user input"""
        self.conversation_count += 1
        user_input_lower = user_input.lower()
        
        # Store user's name if not known
        if "my name is" in user_input_lower:
            parts = user_input_lower.split("my name is")
            if len(parts) > 1:
                name = parts[1].strip().split()[0].capitalize()
                self.user_name = name
                self.memory.append(f"User name: {name}")
                self.save_memory()
                return f"Nice to meet you, {name}! I'll remember that."
        
        # Extract topics
        topic_words = ["code", "python", "ai", "data", "github", "learning", "project", "agent"]
        for word in topic_words:
            if word in user_input_lower:
                self.topics.add(word)
                self.memory.append(f"Discussed: {word}")
        
        # Respond based on input type
        if "?" in user_input:
            return self.ask_response(user_input)
        elif "hello" in user_input_lower or "hi" in user_input_lower:
            return self.greeting()
        elif "thank" in user_input_lower:
            return "You're welcome! Is there anything else I can help with?"
        elif user_input_lower == "stats":
            return self.get_stats()
        # ----- ADD THIS NEW SECTION -----
        elif "python" in user_input_lower:
            return "Python is a versatile programming language. It's great for data analysis, AI, and automation. What specific part of Python are you interested in?"
        elif "rainbow" in user_input_lower:
            return "A rainbow has 7 colors: Red, Orange, Yellow, Green, Blue, Indigo, and Violet."
        # ----- END OF NEW SECTION -----
        else:
            return self.general_response(user_input)
    
    def greeting(self):
        """Generate a personalized greeting"""
        if self.user_name:
            return f"Hello again, {self.user_name}! How can I help you today?"
        else:
            return "Hello! I'm your personal assistant. What's your name?"
    
    def ask_response(self, user_input):
        """Response for questions"""
        greetings = ["Great question!", "Good question!", "I'm glad you asked!"]
        import random
        greeting = random.choice(greetings)
        return f"{greeting} Could you tell me more about what you're looking for?"
    
    def general_response(self, user_input):
        """General fallback response"""
        if "python" in user_input.lower():
            return "Python is a great language for AI! It's used for data science, web development, and automation. What would you like to learn about Python?"
        if "code" in user_input.lower():
            return "I love coding! What language are you working with?"
        elif "project" in user_input.lower():
            return "Projects are the best way to learn. What are you building?"
        elif "learn" in user_input.lower():
            return "Learning is a journey. What skill are you focusing on right now?"
        elif "github" in user_input.lower():
            return "GitHub is great for sharing code. Have you pushed your first repo yet?"
        else:
            responses = [
                "That's interesting! Tell me more.",
                "I see. Could you elaborate on that?",
                "Good to know! How does that relate to your goals?",
                "That's helpful context. What would you like to explore next?"
            ]
            import random
            return random.choice(responses)
    
    def get_stats(self):
        """Display conversation statistics"""
        topics_str = ", ".join(self.topics) if self.topics else "None"
        return f"""
📊 Conversation Stats:
   Messages: {self.conversation_count}
   User name: {self.user_name or 'Unknown'}
   Topics: {topics_str}
   Memory items: {len(self.memory)}
   Mood: {self.mood}
        """
    
    def chat(self):
        """Main chat loop"""
        print("\n" + "=" * 50)
        print("🤖 Personal AI Assistant")
        print("=" * 50)
        print("Commands: 'quit', 'clear', 'stats', 'save'")
        print("-" * 50)
        
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() == "quit":
                self.save_memory()
                print("👋 Goodbye! Remember your skills are growing every day.")
                break
            elif user_input.lower() == "clear":
                # Clear terminal
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            elif user_input.lower() == "save":
                self.save_chat()
                continue
            
            elif user_input.lower() == "who am i":
                if self.user_name:
                    print(f"\n🤖 Assistant: You are {self.user_name}. Topics we've discussed: {', '.join(self.topics) or 'none yet'}.")
                else:
                    print("\n🤖 Assistant: I don't know your name yet. Tell me!")
                # Don't save to chat history for this command
                continue
            # Store in chat history
            self.chat_history.append(f"👤 You: {user_input}")
            
            # Generate and store response
            response = self.respond(user_input)
            self.chat_history.append(f"🤖 Assistant: {response}")
            
            print(f"\n🤖 Assistant: {response}")

    # Add this with your other keyword checks


# Run the assistant
if __name__ == "__main__":
    assistant = PersonalAssistant()
    assistant.chat()