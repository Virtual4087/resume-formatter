# Resume Parser Application

A sophisticated Flask-based web application that transforms plain text resumes into professionally formatted DOCX and PDF documents using Google Gemini AI for intelligent parsing.

## 🌟 Features

- **🤖 AI-Powered Parsing**: Uses Google Gemini API to intelligently extract and structure resume data
- **📄 Multiple Output Formats**: Generate professional documents in both DOCX and PDF formats
- **✏️ Interactive Preview**: Real-time editable preview with inline editing capabilities
- **🎯 Smart Categorization**: Automatically organizes technical skills, work experience, and certifications
- **📱 Responsive Design**: Bootstrap-based UI that works on all devices
- **🔗 Hyperlink Support**: Automatically creates clickable email and LinkedIn links
- **⚡ Live Editing**: Edit any section directly in the preview before downloading
- **📊 JSON Export**: View and export the parsed data in JSON format

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Google Gemini API key
- Microsoft Word (Windows) or LibreOffice (Linux/Mac) for PDF generation

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Virtual4087/resume-formatter
   cd resume-parser
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file with your API key
   GEMINI_API_KEY=your_google_gemini_api_key_here
   SECRET_KEY=your_flask_secret_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required: Google Gemini API Key
GEMINI_API_KEY=your_api_key_here

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=dev

# File Storage (Optional)
UPLOAD_FOLDER=uploads
```

### Configuration Options

The application supports multiple environment configurations:

- **Development** (`dev`): Debug mode enabled, detailed error messages
- **Production** (`prod`): Optimized for production deployment
- **Testing** (`test`): Configuration for running tests

Set the environment using:
```bash
export FLASK_ENV=prod  # or dev, test
```

## 📋 Usage Guide

### 1. Input Your Resume
- Paste your plain text resume into the text area
- Ensure your resume has clear section headings (e.g., "Technical Skills", "Work Experience")
- Include contact information, work experience, education, and skills

### 2. Process and Preview
- Click "Process Resume" to parse your text using AI
- Review the structured preview that appears
- All text fields are editable - click on any section to modify

### 3. Edit and Customize
- **Contact Info**: Click on name, email, phone, or LinkedIn to edit
- **Technical Skills**: Edit categories and skill lists directly
- **Work Experience**: Modify company names, roles, dates, and achievements
- **Add/Remove Items**: Use the "+" buttons to add certifications or achievements
- **Delete Items**: Use the "×" buttons to remove unwanted entries

### 4. Download
- **DOCX Format**: Click "Download DOCX" for Microsoft Word format
- **PDF Format**: Click "Download PDF" for PDF format (requires additional setup)
- **View JSON**: Click "View Raw JSON" to see the structured data

## 🔌 API Endpoints

### POST `/submit`
Process resume text and return structured JSON data.

**Request Body:**
```
resume=<plain_text_resume>
```

**Response:**
```json
{
  "status": "success",
  "message": "Resume successfully processed.",
  "data": {
    "contact": { ... },
    "title": "...",
    "summary": "...",
    "technical_skills": { ... },
    "work_experience": [ ... ],
    "education": { ... },
    "certifications": [ ... ]
  },
  "skill_order": ["category1", "category2", ...]
}
```

### POST `/generate`
Generate DOCX document from structured resume data.

**Request Body:**
```json
{
  "contact": { ... },
  "title": "...",
  "summary": "...",
  // ... other resume data
}
```

**Response:** Binary DOCX file download

### POST `/generate/pdf`
Generate PDF document from structured resume data.

**Request Body:** Same as `/generate`

**Response:** Binary PDF file download

## 🏗️ Project Structure

```
resume-parser-latest/
├── app.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
│
├── app/
│   ├── __init__.py               # Flask app factory
│   ├── config/
│   │   └── settings.py           # Configuration classes
│   ├── routes/
│   │   ├── __init__.py
│   │   └── route.py              # Application routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser_service.py     # Resume parsing logic
│   │   └── document_service.py   # Document generation
│   ├── templates/
│   │   └── index.html            # Main UI template
│   └── static/
│       ├── css/
│       │   └── style.css         # Custom styles
│       └── js/
│           └── script.js         # Frontend JavaScript
```

## 🧩 Core Components

### ResumeParser (`app/services/parser_service.py`)
- Interfaces with Google Gemini API
- Converts unstructured text to structured JSON
- Handles skill categorization and data validation

### DocumentGenerator (`app/services/document_service.py`)
- Creates professional DOCX documents
- Generates PDF files (with proper dependencies)
- Handles formatting, tables, and hyperlinks

### Route Handlers (`app/routes/route.py`)
- Flask routes for processing and document generation
- File streaming and download management
- Error handling and validation

### Frontend Interface (`app/templates/index.html`)
- Interactive preview with live editing
- Bootstrap-based responsive design
- Real-time updates and form handling

## 🔧 Dependencies

### Core Dependencies
- **Flask**: Web framework
- **python-docx**: DOCX document generation
- **google-genai**: Google Gemini API integration
- **python-dotenv**: Environment variable management

### Optional Dependencies
- **docx2pdf**: PDF conversion (requires Microsoft Word or LibreOffice)
- **pywin32**: Windows COM interface for PDF generation (Windows only)

### Frontend Libraries (CDN)
- **Bootstrap 5.3**: UI framework
- **Font Awesome 6.4**: Icons

## 🚀 Deployment

### Local Development
```bash
export FLASK_ENV=dev
python app.py
```

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_ENV=prod
EXPOSE 5000

CMD ["python", "app.py"]
```

#### Environment Setup for Production
```bash
export FLASK_ENV=prod
export GEMINI_API_KEY=your_production_api_key
export SECRET_KEY=your_secure_secret_key
```

### Cloud Deployment

#### Heroku
1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Set environment variables:
   ```bash
   heroku config:set GEMINI_API_KEY=your_api_key
   heroku config:set SECRET_KEY=your_secret_key
   ```

#### AWS/Google Cloud
- Use the Docker image or deploy as a Python web service
- Configure environment variables in your cloud platform
- Set up proper security groups and firewall rules

## 🔒 Security Considerations

### API Key Management
- Never commit API keys to version control
- Use environment variables for all sensitive data
- Rotate API keys regularly

### Input Validation
- Resume text is validated before processing
- File uploads are restricted by size and type
- SQL injection protection through parameterized queries

### Production Security
- Use HTTPS in production
- Set strong SECRET_KEY values
- Configure proper CORS policies
- Implement rate limiting for API endpoints

## 🐛 Troubleshooting

### Common Issues

#### PDF Generation Not Working
```bash
# Windows: Install Microsoft Word or
pip install pywin32

# Linux/Mac: Install LibreOffice
sudo apt-get install libreoffice  # Ubuntu/Debian
brew install libreoffice          # macOS
```

#### API Key Issues
- Verify your Google Gemini API key is valid
- Check API quota and billing status
- Ensure the API key has proper permissions

#### Memory Issues with Large Resumes
- Increase system memory allocation
- Consider implementing file size limits
- Use streaming for large document generation

#### Module Import Errors
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Debug Mode
Enable debug mode for detailed error messages:
```bash
export FLASK_ENV=dev
export FLASK_DEBUG=1
python app.py
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for all public functions
- Include type hints where appropriate

### Testing
```bash
# Run tests (when test suite is available)
python -m pytest tests/

# Manual testing
python -m app.services.parser_service  # Test parser directly
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for intelligent text parsing
- Flask community for the excellent web framework
- Bootstrap team for the responsive UI components
- python-docx library for document generation capabilities

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the API documentation for integration questions

---

**Made with ❤️ for better resume formatting**
