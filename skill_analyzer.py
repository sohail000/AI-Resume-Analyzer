class SkillAnalyzer:
    def __init__(self, model):
        self.model = model
    
    def extract_skills(self, text):
        """Extract and categorize skills"""
        prompt = f"""
        Extract and categorize skills from this text:
        {text}
        
        Categorize into:
        1. Technical Skills
        2. Soft Skills
        3. Domain Knowledge
        4. Tools & Technologies
        """
        response = self.model.generate_content(prompt)
        return response.text
    
    def analyze_skill_market_demand(self, skills):
        """Analyze market demand for skills"""
        prompt = f"""
        Analyze market demand for these skills:
        {skills}
        
        Provide:
        1. Current market demand
        2. Future growth potential
        3. Industry preferences
        """
        response = self.model.generate_content(prompt)
        return response.text