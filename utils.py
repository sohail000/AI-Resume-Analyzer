import os
from datetime import datetime

class Utils:
    @staticmethod
    def validate_file(file_path, supported_formats, max_size):
        """Validate file format and size"""
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in supported_formats:
            raise ValueError(f"Unsupported file format. Supported formats: {supported_formats}")
        
        if os.path.getsize(file_path) > max_size:
            raise ValueError(f"File too large. Maximum size: {max_size/1024/1024}MB")
    
    @staticmethod
    def generate_report_filename(base_name):
        """Generate unique report filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.txt"
    
    def format_skills_for_display(skills_list):
        """Format skills for Streamlit display"""
        return [f"<span class='skill-tag'>{skill}</span>" for skill in skills_list]

    def create_progress_bar(value, max_value=100):
        """Create a styled progress bar"""
        percentage = (value / max_value) * 100
        return f"""
        <div class="progress">
            <div class="progress-bar" style="width: {percentage}%">
                {percentage:.1f}%
            </div>
        </div>
        """