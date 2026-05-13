import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super_secret_expense_key')
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'expenses.db')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
