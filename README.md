# SLM_TRANSLATOR

English to Tamil Translation using a Small Language Model.

## Project Description

SLM_TRANSLATOR is a simple AI-powered translation
application that converts English sentences into Tamil.

## Technologies Used

- Python
- FastAPI
- HTML
- CSS
- JavaScript
- Helsinki-NLP OPUS-MT via Hugging Face, with MyMemory fallback

## Features

1. English text input.
2. English to Tamil translation.
3. AI-powered translation.
4. Simple user interface.
5. FastAPI backend.
6. REST API integration.

## Installation

### Step 1: Create virtual environment

python -m venv venv

### Step 2: Activate environment

Windows:

venv\Scripts\activate

### Step 3: Install requirements

python -m pip install --upgrade pip

python -m pip install -r requirements.txt

### Step 4: Optional Hugging Face access

To use Helsinki-NLP's model when inference credits are available, create a
Hugging Face token with **Inference Providers** permission and save it in a
`.env` file in the project root:

```text
HF_TOKEN=hf_your_actual_token
```

The app loads `.env` automatically when it starts. Keep your real token private;
`.env` is excluded from version control.

When no token is set, or Hugging Face returns HTTP 402 for unavailable
credits, the app uses MyMemory's free English-to-Tamil service. The fallback
has usage limits and may provide lower-quality translations. Text is sent to
the provider used, so do not translate sensitive text unless you are
comfortable sending it to that provider.

### Step 5: Run application

python -m uvicorn backend.main:app --reload

### Step 6: Open browser

http://127.0.0.1:8000

## API Documentation

http://127.0.0.1:8000/docs

## API Endpoint

POST /translate

Input:

{
    "text": "How are you?"
}

Output:

{
    "english": "How are you?",
    "tamil": "நீங்கள் எப்படி இருக்கிறீர்கள்?"
}

## Model

Helsinki-NLP/opus-mt-en-dra through Hugging Face Inference Providers, with a
MyMemory fallback. Neither path requires PyTorch or local model files on
Windows.