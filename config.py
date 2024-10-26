import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    SUPPORTED_FORMATS = ['.pdf', '.docx', '.txt']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # API Templates
    RESUME_ANALYSIS_PROMPT = """
    Analyze this resume and provide:
    1. Key skills and expertise
    2. Experience summary
    3. Education details
    4. Suggested improvements
    """
    
    JOB_MATCH_PROMPT = """
    Compare this resume with the job description and provide:
    1. Match percentage
    2. Missing required skills
    3. Relevant experience
    4. Suggestions for improvement
    """