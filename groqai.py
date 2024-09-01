import os
from groq import Groq
        
class GenerateResume:
    def __init__(self, key, parameters, resume_format, job_description):
        self.client = Groq(api_key=key)
        self.parameters = parameters
        self.resume_format = resume_format
        self.job_description = job_description
        self.chat_completion = self.generate_resume()

    def generate_resume(self):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "I will give you my details, resume format, and job description. Please generate a resume in the given LaTeX format for the given job description with my details.",
                },
                {
                    "role": "user",
                    "content": f'Here are the details: {self.parameters}',
                },
                {
                    "role": "user",
                    "content": f'Here is the resume format: {self.resume_format}',
                },
                {
                    "role": "user",
                    "content": f'Here is the job description: {self.job_description}',
                },{
                    "role": "user",
                    "content": "Now By using all the above data generate me a resume int latex. Note: can u please only generate the latex code. Because ur response is directed to a automated process which only knows latex code and it dont have intelligence to evaluate th resume and dont use ''' or 'here is ur latex code'",
                },
            ],
            model="llama3-70b-8192",
            temperature=1,
            max_tokens=8192,
            top_p=1,
            stop=None,
        )
        return chat_completion.choices[0].message.content

    def save_resume_to_file(self, file_path):
        resume_content = self.generate_resume()
        with open(file_path, 'w') as file:
            file.write(resume_content)
        print(f"Resume saved to {file_path}")
