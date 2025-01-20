# Shortlist AI  
An AI-powered resume builder that tailors resumes to specific job descriptions, improving relevance and readability for job seekers. Built with cutting-edge technologies like FastAPI, React, and Llama 8B (via Groq LLM interface).  

## Features  
- **AI-Powered Optimization**: Extracts keywords from job descriptions and optimizes resumes using Llama 8B LLM.  
- **Dynamic Templates**: Generates tailored resumes with customizable, exportable formats (PDF, Word).  
- **Seamless Integration**: Built with FastAPI and React for a smooth user experience.  
- **Scalable Architecture**: Designed for flexibility and scalability, supporting multiple templates and use cases.  

## Tech Stack  
- **Backend**: FastAPI, Python, Jinja2, ReportLab, Llama 8B (Groq LLM)  
- **Frontend**: React, TailwindCSS  
- **NLP**: spaCy, Hugging Face Transformers  

## How It Works  
1. **Input Details**: Users input personal details or upload an existing resume.  
2. **Upload Job Description**: The system analyzes job requirements using advanced NLP models.  
3. **Resume Generation**: Shortlist AI tailors a resume to match the job description, highlighting relevant skills and achievements.  
4. **Export**: Users can preview and download their optimized resumes in PDF or Word format.  

## Installation  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/YourUsername/shortlist-ai.git  
   cd shortlist-ai  
   ```  
2. Set up the backend:  
   ```bash  
   cd backend  
   pip install -r requirements.txt  
   uvicorn main:app --reload  
   ```  

## Contributions  
Contributions are welcome! Feel free to open issues or submit pull requests.  

## License  
This project is licensed under the [MIT License](LICENSE).  

## Demo  (will be uploaded soon)
- [YouTube Demo](https://youtu.be/YourVideoLink)  
- [Live Preview](https://your-live-link.com)  
