import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class to manage API keys and settings"""
    
    @staticmethod
    def get_openrouter_api_key():
        """Get OpenRouter API key from environment variables"""
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key or api_key == 'your-api-key-here':
            raise ValueError("OpenRouter API key not found or invalid. Please check your .env file")
        return api_key
    
    @staticmethod
    def get_site_url():
        """Get site URL for OpenRouter"""
        return os.getenv('OPENROUTER_SITE_URL', 'http://localhost:3000')
    
    @staticmethod
    def get_site_name():
        """Get site name for OpenRouter"""
        return os.getenv('OPENROUTER_SITE_NAME', 'Git Demo Project')
    
    @staticmethod
    def get_model():
        """Get default model for API calls"""
        return os.getenv('DEFAULT_MODEL', 'openrouter/elephant-alpha')