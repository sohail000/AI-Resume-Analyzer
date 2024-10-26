class MarketInsightAnalyzer:
    def __init__(self, model):
        self.model = model
    
    def analyze_market_trends(self, profile):
        """Analyze market trends for the profile"""
        prompt = f"""
        Analyze market trends for this profile:
        {profile}
        
        Provide:
        1. Salary ranges
        2. In-demand skills
        3. Industry growth areas
        4. Career progression paths
        """
        response = self.model.generate_content(prompt)
        return response.text