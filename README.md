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