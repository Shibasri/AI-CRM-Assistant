# AI-Powered CRM Assistant

A lightweight AI-powered CRM assistant built with Python, FastAPI, SQLite, HTML, CSS, and JavaScript.

The assistant allows sales and support teams to interact with CRM data using natural language through a simple chat interface.

## Features

- View customer details
- Count leads by status
- Find deals above a specific amount
- Find inactive/old deals
- Identify deals at risk of going cold
- View customer conversation history
- Update deal status
- Add notes to customers
- Assign leads to salespeople
- Handle unknown customers safely

## Tech Stack

- Python
- FastAPI
- SQLite
- Jinja2
- HTML
- CSS
- JavaScript
- Pydantic
- OpenAI API

## Project Structure

```text
AI-CRM-Assistant/
│
├── app.py
├── agent.py
├── tools.py
├── database.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```
## Architecture

```text
User
  |
  v
Chat UI
  |
  v
FastAPI
  |
  v
CRM Agent
  |
  +----> CRM Tools
  |          |
  |          v
  |       SQLite
  |
  v
Response
```
## How to Run

1. Clone the repository: `git clone https://github.com/Shibasri/AI-CRM-Assistant.git` and `cd AI-CRM-Assistant`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment on Windows: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python -m uvicorn app:app --reload`
6. Open your browser and go to: `http://127.0.0.1:8000`

## Example Queries

1. Show Arun Kumar details
2. How many leads are currently in Contacted status?
3. Show me all deals worth over 10000
4. Show me deals that are at risk of going cold
5. Show Arun Kumar's conversation history
6. Move Arun Kumar's deal to Won
7. Add a note to Arun Kumar: Follow up next Monday
8. Assign Arun Kumar's lead to Priya
9. Find customer XYZ