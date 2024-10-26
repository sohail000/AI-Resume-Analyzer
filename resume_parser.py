import google.generativeai as genai
from pdfminer.high_level import extract_text
from docx import Document
import os
import json

class ResumeParser:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def parse_file(self, uploaded_file):
        """Parse uploaded file content"""
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Save the uploaded file temporarily
        with open("temp_file" + file_extension, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            if file_extension == '.pdf':
                text = self.parse_pdf("temp_file" + file_extension)
            elif file_extension == '.docx':
                text = self.parse_docx("temp_file" + file_extension)
            else:
                raise ValueError("Unsupported file format")
            
            # Remove temporary file
            os.remove("temp_file" + file_extension)
            return text
            
        except Exception as e:
            # Clean up temporary file in case of error
            if os.path.exists("temp_file" + file_extension):
                os.remove("temp_file" + file_extension)
            raise e
    
    def parse_pdf(self, file_path):
        """Extract text from PDF"""
        try:
            text = extract_text(file_path)
            return text
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def parse_docx(self, file_path):
        """Extract text from DOCX"""
        try:
            doc = Document(file_path)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")

    def analyze_resume(self, uploaded_file, job_desc=None):
        """Main analysis function"""
        try:
            # First parse the file
            resume_text = self.parse_file(uploaded_file)
            
            # Prepare the analysis prompt
            prompt = """
            Analyze this resume and provide a detailed analysis in the following JSON format. Be specific, comprehensive and factual:
            {
                "summary": {
                    "brief": "A concise 2-3 sentence professional summary highlighting key strengths",
                    "years_of_experience": "Total years of experience as a number",
                    "ai_rating": {
                        "overall": "Score 0-100",
                        "skills_rating": "Score 0-100",
                        "experience_rating": "Score 0-100",
                        "education_rating": "Score 0-100"
                    }
                },
                "skills": {
                    "expertise_level": {
                        "expert": ["List of expert-level skills"],
                        "intermediate": ["List of intermediate-level skills"],
                        "beginner": ["List of beginner-level skills"]
                    }
                },
                "achievements": [
                    {
                        "title": "Achievement title",
                        "description": "Detailed achievement description",
                        "impact": "Quantifiable impact if available"
                    }
                ],
                "experience": {
                    "total_years": "X years Y months",
                    "experiences": [
                        {
                            "title": "Job Title",
                            "company": "Company Name",
                            "duration": "Duration",
                            "responsibilities": ["Key responsibility 1", "Key responsibility 2"],
                            "key_achievements": ["Achievement 1", "Achievement 2"]
                        }
                    ]
                },
                "education": {
                    "education": [
                        {
                            "degree": "Degree Name",
                            "institution": "Institution Name",
                            "year": "Year",
                            "achievements": ["Academic achievement 1", "Academic achievement 2"]
                        }
                    ]
                },
                "certifications": [
                    {
                        "name": "Certification Name",
                        "issuer": "Issuing Organization",
                        "year": "Year"
                    }
                ],
                "market_insights": {
                    "salary_range": {
                        "average": "Average salary for this profile",
                        "range": "Expected salary range"
                    },
                    "demand": {
                        "trend": "Current market trend",
                        "growth_rate": "Expected growth rate"
                    }
                },
                "suggestions": {
                    "resume_improvements": ["Specific suggestion 1", "Specific suggestion 2"],
                    "skill_improvements": ["Skill improvement 1", "Skill improvement 2"],
                    "career_growth": ["Career growth suggestion 1", "Career growth suggestion 2"]
                }
            }

            Resume text to analyze:
            """ + resume_text

            # Get the analysis from Gemini
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Parse the response
            try:
                # First try to parse the response directly
                analysis = json.loads(response_text)
            except json.JSONDecodeError:
                # If direct parsing fails, try to find JSON content
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx != 0:
                    json_str = response_text[start_idx:end_idx]
                    analysis = json.loads(json_str)
                else:
                    raise Exception("Could not parse the analysis response")

            # If job description is provided, add job match analysis
            if job_desc:
                job_match = self.analyze_job_match(resume_text, job_desc)
                analysis['job_match'] = job_match

            return analysis

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            # Return a structured error response
            return {
                "error": str(e),
                "summary": {
                    "brief": "Error analyzing resume",
                    "years_of_experience": "0",
                    "ai_rating": {
                        "overall": "0",
                        "skills_rating": "0",
                        "experience_rating": "0",
                        "education_rating": "0"
                    }
                },
                "skills": {
                    "expertise_level": {
                        "expert": [],
                        "intermediate": [],
                        "beginner": []
                    }
                },
                "achievements": [],
                "experience": {
                    "total_years": "0",
                    "experiences": []
                },
                "education": {
                    "education": []
                },
                "certifications": [],
                "market_insights": {
                    "salary_range": {
                        "average": "Not available",
                        "range": "Not available"
                    },
                    "demand": {
                        "trend": "Not available",
                        "growth_rate": "Not available"
                    }
                },
                "suggestions": {
                    "resume_improvements": [],
                    "skill_improvements": [],
                    "career_growth": []
                }
            }

    def analyze_job_match(self, resume_text, job_description):
        """Analyze job match and return structured data"""
        try:
            prompt = f"""
            Compare this resume and job description. Provide analysis in this exact JSON format:
            {{
                "match_percentage": "Overall match score 0-100",
                "skills_match": "Skills match score 0-100",
                "experience_match": "Experience match score 0-100",
                "missing_skills": ["Required skill 1 that's missing", "Required skill 2 that's missing"],
                "matching_skills": ["Matching skill 1", "Matching skill 2"],
                "recommendations": ["Specific recommendation 1", "Specific recommendation 2"]
            }}

            Resume:
            {resume_text}

            Job Description:
            {job_description}
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx != 0:
                    json_str = response_text[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    return {
                        "match_percentage": "0",
                        "skills_match": "0",
                        "experience_match": "0",
                        "missing_skills": ["Could not analyze skills match"],
                        "matching_skills": [],
                        "recommendations": ["Could not generate recommendations"]
                    }

        except Exception as e:
            print(f"Error in analyze_job_match: {str(e)}")
            return {
                "match_percentage": "0",
                "skills_match": "0",
                "experience_match": "0",
                "missing_skills": [],
                "matching_skills": [],
                "recommendations": []
            }