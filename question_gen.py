class QuestionGenerator:
    def __init__(self, model):
        self.model = model
    
    def generate_technical_questions(self, skills):
        """Generate technical interview questions"""
        prompt = f"""
        Generate technical interview questions for these skills:
        {skills}
        
        Include:
        1. Basic concept questions
        2. Problem-solving scenarios
        3. Experience-based questions
        """
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_behavioral_questions(self, experience):
        """Generate behavioral interview questions"""
        prompt = f"""
        Based on this experience:
        {experience}
        
        Generate relevant behavioral interview questions.
        """
        response = self.model.generate_content(prompt)
        return response.text