import yaml
import os
import re
from pathlib import Path
import sys
from groqai import GenerateResume


def file(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"LaTeX file not found: {file_path}")
    
    with open(file_path, 'r') as file:
        return file.read()

# Suppress stderr output
sys.stderr = open(os.devnull, 'w')

class ConfigError(Exception):
    pass

class ConfigValidator:    
    @staticmethod
    def validate_yaml_file(yaml_path: Path) -> dict:
        try:
            with open(yaml_path, 'r') as stream:
                return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise ConfigError(f"Error reading file {yaml_path}: {exc}")
        except FileNotFoundError:
            raise ConfigError(f"File not found: {yaml_path}")

    @staticmethod
    def validate_secrets(secrets_yaml_path: Path) -> str:
        secrets = ConfigValidator.validate_yaml_file(secrets_yaml_path)
        mandatory_secrets = ['groq_ai_api_key']

        for secret in mandatory_secrets:
            if secret not in secrets:
                raise ConfigError(f"Missing secret '{secret}' in file {secrets_yaml_path}")
        if not secrets['groq_ai_api_key']:
            raise ConfigError(f"Groq Ai API key cannot be empty in secrets file {secrets_yaml_path}.")

        return secrets['groq_ai_api_key']

class FileManager:
    @staticmethod
    def find_file(name_containing: str, with_extension: str, at_path: Path) -> Path:
        return next((file for file in at_path.iterdir() if name_containing.lower() in file.name.lower() and file.suffix.lower() == with_extension.lower()), None)

    @staticmethod
    def validate_data_folder(app_data_folder: Path) -> tuple:
        if not app_data_folder.exists() or not app_data_folder.is_dir():
            raise FileNotFoundError(f"Data folder not found: {app_data_folder}")

        required_files = ['secrets.yaml', 'plain_text_resume.yaml', 'job_description.txt', 'resume_format.tex']
        missing_files = [file for file in required_files if not (app_data_folder / file).exists()]
        
        if missing_files:
            raise FileNotFoundError(f"Missing files in the data folder: {', '.join(missing_files)}")

        output_folder = app_data_folder / 'output'
        output_folder.mkdir(exist_ok=True)
        return (app_data_folder / 'secrets.yaml', app_data_folder / 'plain_text_resume.yaml', output_folder, app_data_folder / 'job_description.txt', app_data_folder / 'resume_format.tex')

    @staticmethod
    def file_paths_to_dict(resume_file: Path | None, plain_text_resume_file: Path) -> dict:
        if not plain_text_resume_file.exists():
            raise FileNotFoundError(f"Plain text resume file not found: {plain_text_resume_file}")

        result = {'plainTextResume': plain_text_resume_file}

        if resume_file:
            if not resume_file.exists():
                raise FileNotFoundError(f"Resume file not found: {resume_file}")
            result['resume'] = resume_file

        return result

def display_parsed_data(data: dict):
    if data:
        print("Personal Information:")
        for key, value in data.get('personal_information', {}).items():
            print(f"  {key}: {value}")

        print("\nEducation Details:")
        for edu in data.get('education_details', []):
            print(f"  Degree: {edu.get('degree', 'N/A')}")
            print(f"  University: {edu.get('university', 'N/A')}")
            print(f"  GPA: {edu.get('gpa', 'N/A')}")
            print(f"  Graduation Year: {edu.get('graduation_year', 'N/A')}")
            print(f"  Field of Study: {edu.get('field_of_study', 'N/A')}")
            print(f"  Exam: {edu.get('exam', 'N/A')}")
            print()

        print("Experience Details:")
        for exp in data.get('experience_details', []):
            print(f"  Position: {exp.get('position', 'N/A')}")
            print(f"  Company: {exp.get('company', 'N/A')}")
            print(f"  Employment Period: {exp.get('employment_period', 'N/A')}")
            print(f"  Location: {exp.get('location', 'N/A')}")
            print(f"  Industry: {exp.get('industry', 'N/A')}")
            print("  Key Responsibilities:")
            for resp in exp.get('key_responsibilities', []):
                print(f"    - {list(resp.values())[0]}")
            print("  Skills Acquired:")
            for skill in exp.get('skills_acquired', []):
                print(f"    - {skill}")
            print()

        print("Projects:")
        for proj in data.get('projects', []):
            print(f"  Name: {proj.get('name', 'N/A')}")
            print(f"  Description: {proj.get('description', 'N/A')}")
            print(f"  Link: {proj.get('link', 'N/A')}")
            print()

        print("Achievements:")
        for ach in data.get('achievements', []):
            print(f"  Name: {ach.get('name', 'N/A')}")
            print(f"  Description: {ach.get('description', 'N/A')}")
            print()

        print("Certifications:")
        if not data.get('certifications'):
            print("  No certifications listed.")
        print()

        print("Languages:")
        for lang in data.get('languages', []):
            print(f"  Language: {lang.get('language', 'N/A')}")
            print(f"  Proficiency: {lang.get('proficiency', 'N/A')}")
            print()

        print("Interests:")
        for interest in data.get('interests', []):
            print(f"  - {interest}")
        print()

        print("Availability:")
        print(f"  Notice Period: {data.get('availability', {}).get('notice_period', 'N/A')}")
        print()

        print("Salary Expectations:")
        print(f"  Salary Range (USD): {data.get('salary_expectations', {}).get('salary_range_usd', 'N/A')}")
        print()

        print("Self Identification:")
        for key, value in data.get('self_identification', {}).items():
            print(f"  {key}: {value}")
        print()

        print("Legal Authorization:")
        for key, value in data.get('legal_authorization', {}).items():
            print(f"  {key}: {value}")
        print()

        print("Work Preferences:")
        for key, value in data.get('work_preferences', {}).items():
            print(f"  {key}: {value}")
        print()


def main():
    try:
        data_folder = Path("data_folder")
        secrets_file, plain_text_resume_file, output_folder, resume_file, job_description_file = FileManager.validate_data_folder(data_folder)
        groq_ai_api_key = ConfigValidator.validate_secrets(secrets_file)
        parameters = ConfigValidator.validate_yaml_file(plain_text_resume_file)
        display_parsed_data(parameters)
        parameters['outputFileDirectory'] = output_folder
        latex_file_path = Path(resume_file)
        resume_format = file(latex_file_path)
        print("Read resume format")
        job_description = file(Path(job_description_file))
        print("Read Job Description")
        print("Started generating Resume")
        resume_generator = GenerateResume(groq_ai_api_key, parameters, resume_format, job_description)
        print("Completed generating Resume")
        resume_file_path = output_folder / "generated_resume.tex"
        print("started saving Resume")
        resume_generator.save_resume_to_file(resume_file_path)
        print("completed saving Resume")
        

    except ConfigError as ce:
        print(f"Configuration error: {str(ce)}")

    except FileNotFoundError as fnf:
        print(f"File not found: {str(fnf)}")
        print("Ensure all required files are present in the data folder.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")    

if __name__ == "__main__":
    main()
