import requests
import json
from config import Config

class OpenRouterDemo:
    """Demonstration class for OpenRouter API integration"""
    
    def __init__(self):
        """Initialize with configuration from .env file"""
        try:
            self.api_key = Config.get_openrouter_api_key()
            self.site_url = Config.get_site_url()
            self.site_name = Config.get_site_name()
            self.model = Config.get_model()
            print("Configuration loaded successfully from .env file")
        except ValueError as e:
            print(f"Configuration error: {e}")
            print("Please make sure you have a valid .env file with OPENROUTER_API_KEY")
            raise
    
    def ask_question(self, question):
        """Send a question to OpenRouter API and get response"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.site_url,
            "X-OpenRouter-Title": self.site_name,
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
        
        try:
            print(f"🤔 Asking: {question}")
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content']
                print(f"💡 Answer: {answer}")
                return answer
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
    
    def demo_conversation(self):
        """Run a demo conversation"""
        print("\n" + "="*50)
        print("🚀 OpenRouter API Demo with Git and .env")
        print("="*50)
        print(f"Using model: {self.model}")
        print(f"Site: {self.site_name} ({self.site_url})")
        print("="*50 + "\n")
        
        # Demo questions
        questions = [
            "What is the meaning of life?",
            "What is 42 in programming culture?",
            "Explain Git in one sentence"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\nQuestion {i}/{len(questions)}:")
            self.ask_question(question)
            print("-"*50)

def main():
    """Main function to run the demo"""
    try:
        # Create demo instance
        demo = OpenRouterDemo()
        
        # Run demonstration
        demo.demo_conversation()
        
        print("\n✨ Demo completed successfully!")
        
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())