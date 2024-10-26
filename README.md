# AI Resume Analyzer 📄

An advanced resume analysis tool powered by Google's Gemini AI that provides detailed insights, skill analysis, and job matching capabilities.

## 📸 Screenshots

### Upload & Analysis Interface
![Upload Interface](https://github.com/user-attachments/assets/5f9a7b80-8a1d-414f-8b88-161f7d761ec9)

### Skills Analysis
![Skills Analysis](https://github.com/user-attachments/assets/c35443c3-99be-416d-9548-886340ee9d33)

### Market Insights
![Market Insights](https://github.com/user-attachments/assets/0f6ea0e5-f5e3-4029-8c38-89cc52f28b72)

### Improvement Suggestions
![Suggestions](https://github.com/user-attachments/assets/91a9a2c1-bed2-4e81-9e37-7580f0b3c182)

## 🌟 Features

- **📊 Comprehensive Resume Analysis**
  - Detailed skills assessment
  - Experience evaluation
  - Achievement highlighting
  - Education analysis
  - Professional summary generation

- **💼 Job Matching**
  - Match percentage with job descriptions
  - Missing skills identification
  - Relevant experience mapping
  - Tailored improvement suggestions

- **📈 Market Insights**
  - Salary range estimations
  - Industry demand analysis
  - Career growth opportunities
  - Skill market trends

- **💡 Smart Suggestions**
  - Resume improvement tips
  - Skill development recommendations
  - Career growth strategies

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Engine**: Google Gemini Pro
- **Document Processing**: 
  - PDFMiner (PDF parsing)
  - python-docx (DOCX parsing)
- **Additional Libraries**:
  - python-dotenv (Environment management)
  - pandas (Data handling)
  - NLTK (Text processing)


## 🚀 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Upload your resume (PDF or DOCX format)

4. (Optional) Add a job description for matching analysis

5. Click "Analyze Resume" to get detailed insights

## 📁 Project Structure

```
ai-resume-analyzer/
├── app.py              # Main Streamlit application
├── config.py           # Configuration settings
├── resume_parser.py    # Core resume parsing logic
├── job_matcher.py      # Job matching functionality
├── market_insights.py  # Market analysis features
├── question_gen.py     # Interview question generator
├── skill_analyzer.py   # Skills analysis module
├── utils.py           # Utility functions
└── requirements.txt   # Project dependencies
.env is removed from this directory
```

## 🎯 Key Components

- **Resume Parser**: Extracts and structures information from PDF and DOCX resumes
- **Skill Analyzer**: Identifies and categorizes professional skills
- **Job Matcher**: Compares resumes with job descriptions
- **Market Insight Analyzer**: Provides industry and career insights
- **Question Generator**: Creates relevant interview questions

## 🔒 Privacy & Security

- Files are processed locally and not stored permanently
- No resume data is saved or shared
- Secure API communication with Google Gemini

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powering the analysis engine
- Streamlit for the interactive web interface
- All contributors and users of this tool

## 📫 Contact

For any queries or suggestions, please open an issue in the GitHub repository.

---
