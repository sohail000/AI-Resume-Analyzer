import streamlit as st
import plotly.express as px
from pathlib import Path
import json
import os
from dotenv import load_dotenv
from resume_parser import ResumeParser

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css():
    st.markdown("""
    <style>
    .main-summary {
        background: linear-gradient(135deg, #4c72b0, #2e4482);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #6a98e0, #4c72b0);
        color: white;
        border-radius: 15px;
        padding: 5px 15px;
        margin: 5px;
        font-size: 0.9em;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .achievement-card {
        background: linear-gradient(135deg, #43cea2, #185a9d);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .experience-card {
        background: linear-gradient(135deg, #614385, #516395);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .rating-circle {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: conic-gradient(from 0deg, #4CAF50 var(--progress), #e0e0e0 var(--progress));
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 10px auto;
    }
    
    .rating-number {
        font-size: 24px;
        font-weight: bold;
        color: white;
    }
    
    .section-title {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        margin: 20px 0;
    }
    
    .suggestion-card {
        background: linear-gradient(135deg, #FF8008, #FFC837);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }

    .stApp {
        background: #f8f9fa;
    }

    .skills-section {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .expertise-level {
        margin: 15px 0;
        padding: 10px;
        border-radius: 5px;
    }

    .expert {
        background: linear-gradient(135deg, #FF416C, #FF4B2B);
    }

    .intermediate {
        background: linear-gradient(135deg, #f2994a, #f2c94c);
    }

    .beginner {
        background: linear-gradient(135deg, #56CCF2, #2F80ED);
    }
    </style>
    """, unsafe_allow_html=True)

class StreamlitApp:
    def __init__(self):
        self.parser = ResumeParser(os.getenv('GEMINI_API_KEY'))

    def render_sidebar(self):
        with st.sidebar:
            st.title("📄 Resume Analyzer")
            st.markdown("---")
            st.markdown("""
            ### Features:
            - 📊 Detailed Skills Analysis
            - 🎯 AI Matching Score
            - 💼 Career Insights
            - 📈 Market Analysis
            - 💡 Smart Suggestions
            """)
            st.markdown("---")
            st.markdown("### How to use:")
            st.markdown("""
            1. Upload your resume (PDF/DOCX)
            2. (Optional) Add job description
            3. Get AI-powered insights
            """)
            st.markdown("---")
            st.markdown("Made with ❤️ using Gemini AI")

    def render_file_upload(self):
        st.header("📄 Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose your resume (PDF/DOCX)", 
            type=["pdf", "docx"],
            help="Upload your resume in PDF or DOCX format"
        )
        return uploaded_file

    def render_job_description(self):
        st.header("💼 Job Description (Optional)")
        job_desc = st.text_area(
            "Paste the job description for matching analysis",
            height=150,
            help="Add a job description to see how well your resume matches"
        )
        return job_desc

    def display_summary_section(self, summary_data):
        st.markdown('<div class="main-summary">', unsafe_allow_html=True)
        st.markdown("### 📋 Professional Summary")
        st.markdown(f"{summary_data.get('brief', '')}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Years of Experience**")
            st.markdown(f"### {summary_data.get('years_of_experience', '0')}")
        
        with col2:
            st.markdown("**AI Rating**")
            rating = summary_data.get('ai_rating', {}).get('overall', '0')
            st.markdown(
                f'<div class="rating-circle" style="--progress: {rating}%">'
                f'<div class="rating-number">{rating}%</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown("**Expert Level Skills**")
            expert_skills = summary_data.get('skills', {}).get('expertise_level', {}).get('expert', [])
            for skill in expert_skills[:3]:
                st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def display_skills_section(self, skills_data):
        st.markdown('<div class="section-title">🎯 Skills Analysis</div>', unsafe_allow_html=True)
        
        expertise_levels = {
            "Expert": ("🔥", "expert"),
            "Intermediate": ("⭐", "intermediate"),
            "Beginner": ("📚", "beginner")
        }
        
        for level, (emoji, class_name) in expertise_levels.items():
            skills = skills_data.get('expertise_level', {}).get(level.lower(), [])
            if skills:
                st.markdown(
                    f'<div class="expertise-level {class_name}">',
                    unsafe_allow_html=True
                )
                st.markdown(f"##### {emoji} {level} Level Skills")
                for skill in skills:
                    st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    def display_achievements_section(self, achievements_data):
        st.markdown('<div class="section-title">🏆 Key Achievements</div>', unsafe_allow_html=True)
        
        for achievement in achievements_data:
            st.markdown(
                f'<div class="achievement-card">'
                f'<h4>{achievement.get("title", "")}</h4>'
                f'<p>{achievement.get("description", "")}</p>'
                f'<p><strong>Impact:</strong> {achievement.get("impact", "")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

    def display_experience_section(self, experience_data):
        st.markdown('<div class="section-title">💼 Professional Experience</div>', unsafe_allow_html=True)
        
        total_years = experience_data.get('total_years', '0')
        st.markdown(f"### Total Experience: {total_years}")
        
        for exp in experience_data.get('experiences', []):
            st.markdown(
                f'<div class="experience-card">'
                f'<h4>{exp.get("title")} at {exp.get("company")}</h4>'
                f'<p><strong>Duration:</strong> {exp.get("duration")}</p>'
                f'<p><strong>Key Responsibilities:</strong></p>'
                f'<ul>{"".join([f"<li>{r}</li>" for r in exp.get("responsibilities", [])])}</ul>'
                f'<p><strong>Achievements:</strong></p>'
                f'<ul>{"".join([f"<li>{a}</li>" for a in exp.get("key_achievements", [])])}</ul>'
                f'</div>',
                unsafe_allow_html=True
            )

    def display_market_insights(self, insights_data):
        st.markdown('<div class="section-title">📊 Market Insights</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("##### Salary Insights")
            st.markdown(f"**Industry Average:** {insights_data.get('salary_range', {}).get('average')}")
            st.markdown(f"**Expected Range:** {insights_data.get('salary_range', {}).get('range')}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("##### Industry Demand")
            st.markdown(f"**Current Trend:** {insights_data.get('demand', {}).get('trend')}")
            st.markdown(f"**Growth Rate:** {insights_data.get('demand', {}).get('growth_rate')}")
            st.markdown('</div>', unsafe_allow_html=True)

    def display_improvement_suggestions(self, suggestions):
        st.markdown('<div class="section-title">💡 Suggestions for Improvement</div>', unsafe_allow_html=True)
        
        categories = {
            "Resume Improvements": "📝",
            "Skill Improvements": "🎯",
            "Career Growth": "📈"
        }
        
        for category, emoji in categories.items():
            key = category.lower().replace(" ", "_")
            items = suggestions.get(key, [])
            if items:
                with st.expander(f"{emoji} {category}"):
                    for item in items:
                        st.markdown(f'<div class="suggestion-card">{item}</div>', unsafe_allow_html=True)

    def main(self):
        local_css()
        self.render_sidebar()

        st.title("AI Resume Analyzer")
        st.markdown("Get detailed insights powered by AI")

        uploaded_file = self.render_file_upload()
        job_desc = self.render_job_description()

        if uploaded_file:
            with st.expander("📄 Preview uploaded file", expanded=False):
                file_details = {
                    "Filename": uploaded_file.name,
                    "File size": f"{uploaded_file.size/1024:.2f} KB",
                    "File type": uploaded_file.type
                }
                for key, value in file_details.items():
                    st.write(f"**{key}:** {value}")

        if uploaded_file and st.button("🔍 Analyze Resume", type="primary"):
            try:
                with st.spinner("🔄 Analyzing your resume... This may take a moment."):
                    analysis_result = self.parser.analyze_resume(uploaded_file, job_desc)
                    
                    # Display summary first
                    self.display_summary_section(analysis_result.get('summary', {}))
                    
                    # Create tabs for different sections
                    tabs = st.tabs([
                        "🎯 Skills", 
                        "🏆 Achievements", 
                        "💼 Experience", 
                        "📈 Insights",
                        "💡 Suggestions"
                    ])
                    
                    with tabs[0]:
                        self.display_skills_section(analysis_result.get('skills', {}))
                    
                    with tabs[1]:
                        self.display_achievements_section(analysis_result.get('achievements', []))
                    
                    with tabs[2]:
                        self.display_experience_section(analysis_result.get('experience', {}))
                    
                    with tabs[3]:
                        self.display_market_insights(analysis_result.get('market_insights', {}))
                    
                    with tabs[4]:
                        self.display_improvement_suggestions(analysis_result.get('suggestions', {}))
                    
                    # Add download button for full report
                    st.download_button(
                        label="📥 Download Full Report",
                        data=json.dumps(analysis_result, indent=2),
                        file_name="resume_analysis_report.json",
                        mime="application/json",
                    )
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.markdown("Please try again with a different file or contact support if the problem persists.")

if __name__ == "__main__":
    app = StreamlitApp()
    app.main()