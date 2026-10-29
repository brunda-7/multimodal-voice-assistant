import os
from groq import Groq

class LLMService:
    def __init__(self, api_key=None):
        self.client_initialized = False
        self.client = None
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
    
    def initialize_client(self):
        """Initialize Groq client with real API connection"""
        if not self.api_key:
            raise ValueError("Groq API key not found. Please set GROQ_API_KEY environment variable.")
        
        self.client = Groq(api_key=self.api_key)
        self.client_initialized = True
        print("✅ Groq client initialized successfully")
    
    def generate_response(self, prompt, conversation_history=None, model="llama-3.1-8b-instant", max_tokens=1024):
        """Generate AI response with conversation context"""
        if not self.client_initialized:
            self.initialize_client()
        
        try:
            # Build messages with conversation history
            messages = []
            
            # Add system message for context
            system_message = """You are a helpful AI assistant. Use the conversation history to provide context-aware responses. 
            If the user refers to previous messages, use that context to give better answers."""
            messages.append({"role": "system", "content": system_message})
            
            # Add conversation history if available
            if conversation_history and conversation_history.get('documents'):
                for i, document in enumerate(conversation_history['documents'][0]):
                    metadata = conversation_history['metadatas'][0][i]
                    role = "user" if metadata['is_user'] else "assistant"
                    messages.append({"role": role, "content": document})
                    print(f"📝 Adding context: {role}: {document[:50]}...")
            
            # Add current prompt
            messages.append({"role": "user", "content": prompt})
            
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=model,
                max_tokens=max_tokens,
                temperature=0.7,
            )
            
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            error_msg = f"Error calling Groq API: {str(e)}"
            print(error_msg)
            return "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."