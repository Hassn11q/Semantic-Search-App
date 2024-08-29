# Semantic Search App

## Overview
semantic search application for arXiv papers. It uses an ETL (Extract, Transform, Load) process to fetch recent papers about RAG from arXiv, process them using a llama3, and store the results in a Supabase database. The application is designed to run automatically on a weekly basis using GitHub Actions.

## Features
- Fetches recent papers from arXiv based on specified keywords
- Processes paper abstracts using llama3 to extract key information
- Generates embeddings for efficient semantic search
- Stores processed data in a Supabase database
- Runs automatically every week using GitHub Actions

## Technologies Used
- Python 3.9
- arXiv API
- Groq API (LLM processing)
- Supabase (database)
- GitHub Actions (automation)
- Hugging Face Transformers (for embeddings)

## Setup

### Prerequisites
- Python 3.9
- A Groq API key
- A Supabase account and project

### Environment Variables
Set up the following environment variables:
- `GROQ_API_KEY`: Your Groq API key
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase project API key

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/YourUsername/Semantic-Search-App.git
   cd Semantic-Search-App
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the ETL Process
To run the ETL process manually:
```
cd etl
python etl.py
```

## GitHub Actions Workflow
The project includes a GitHub Actions workflow that runs the ETL process automatically every Monday. The workflow is defined in `.github/workflows/etl.yml`.

To enable the workflow:
1. Go to your GitHub repository settings
2. Navigate to "Actions" > "General"
3. Ensure that "Allow all actions and reusable workflows" is selected
4. Save the changes
