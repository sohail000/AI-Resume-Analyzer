class JobMatcher:
    def __init__(self, model):
        self.model = model
    
    def match_job(self, resume_text, job_description):
        """Match resume with job description"""
        prompt = f"""
        Resume:
        {resume_text}
        
        Job Description:
        {job_description}
        
        Provide a detailed analysis of the match.
        """
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_improvement_suggestions(self, match_analysis):
        """Generate suggestions for improvement"""
        prompt = f"Based on this job match analysis: {match_analysis}\n\nProvide specific suggestions for improvement."
        response = self.model.generate_content(prompt)
        return response.text