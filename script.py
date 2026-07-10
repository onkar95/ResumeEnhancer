from pathlib import Path

folders = [
    "backend/app/api",
    "backend/app/schemas",
    "backend/app/services",
    "backend/app/core",
    "backend/uploads",
    "backend/generated",
]

files = [
    "backend/app/main.py",
    "backend/app/api/tailor.py",
    "backend/app/schemas/resume.py",
    "backend/app/services/pdf_extraction_service.py",
    "backend/app/services/llm_service.py",
    "backend/app/core/config.py",
    "backend/.env",
    "backend/requirements.txt",
]

# Create folders
for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

# Create files
for file in files:
    Path(file).touch(exist_ok=True)

print("✅ Backend project structure created successfully!")