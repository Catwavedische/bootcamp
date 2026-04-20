import requests
import json
import csv
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
    
    def load_questions_from_csv(self, csv_file='questions.csv'):
        """Load questions from CSV file"""
        questions = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0].strip():
                        questions.append(row[0].strip())
            print(f"Loaded {len(questions)} questions from {csv_file}")
            return questions
        except FileNotFoundError:
            print(f"❌ CSV file '{csv_file}' not found. Using default questions.")
            return [
                "What is the meaning of life?",
                "What is 42 in programming culture?",
                "Explain Git in one sentence"
            ]
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
            return []
    
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
    
    def demo_conversation(self, csv_file='questions.csv'):
        """Run a demo conversation with questions from CSV"""
        print("\n" + "="*50)
        print("🚀 OpenRouter API Demo with Git and .env")
        print("="*50)
        print(f"Using model: {self.model}")
        print(f"Site: {self.site_name} ({self.site_url})")
        print("="*50 + "\n")
        
        # Load questions from CSV
        questions = self.load_questions_from_csv(csv_file)
        
        if not questions:
            print("No questions to ask. Please check your CSV file.")
            return
        
        for i, question in enumerate(questions, 1):
            print(f"\nQuestion {i}/{len(questions)}:")
            self.ask_question(question)
            print("-"*50)

def main():
    """Main function to run the demo"""
    try:
        demo = OpenRouterDemo()
        
        demo.demo_conversation('questions.csv')
        
        print("\n✨ Demo completed successfully!")
        
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())