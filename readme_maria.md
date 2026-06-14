---
title: "Untitled"
author: "Aurora González Vidal"
date: "2026-03-29"
output: html_document
---

# FestAI — Open Source Festival Assistant

This notebook creates a smart assistant that can answer questions about music festivals using only open-source tools. It is the first step to building a chatbot that gives helpful, accurate answers based on real festival information.

## What does it do?

- **Loads festival information:** It reads text files with details about a festival (like transportation, schedules, and FAQs).
- **Understands questions:** It uses AI to understand questions you ask about the festival.
- **Finds relevant information:** It searches the festival documents for the most relevant pieces of information.
- **Generates answers:** It combines the found information and uses a language model to write a clear answer in Spanish.
- **Works on any computer:** You can run it on a regular computer (using a small model) or a more powerful server (using a larger model for better answers).

## How does it work?

1. **Setup:** You create a Python environment and install the required packages.
2. **Choose mode:** Select if you want to run it locally (for testing) or on a server (for production).
3. **Prepare data:** The notebook loads and processes the festival documents.
4. **AI models:** It loads two types of AI models:
   - One to turn text into numbers (so the computer can search and compare).
   - Another to generate human-like answers.
5. **Ask questions:** You can type a question (e.g., "What buses go to the festival?") and the assistant will answer using only the official festival information.
6. **Clean up:** When finished, it frees up your computer’s memory.



In order to turn this notebook into a real chatbot for festival attendees (we will create one per festival), consider the following steps:

1. **Prepare Your Data:** Organize all relevant festival documents (FAQs, schedules, transport info) in text format inside the `festival_txts` folder. // We have this although it can be improved
2. **Test the Notebook:** Run the notebook with your real data to ensure it answers questions correctly.
3. **Build a User Interface:** Create a simple web or chat interface (using tools like Streamlit, Gradio, or a web framework) so users can interact with the assistant easily.
4. **Deploy the Backend:** Convert the notebook logic into Python scripts or a web API (using FastAPI or Flask) to handle user questions and return answers.
5. **Connect Frontend and Backend:** Link your user interface to the backend so questions are sent to the AI and answers are displayed to users.
6. **Host the Application:** Deploy your chatbot on a server or cloud platform (like AWS, Azure, or Heroku) for public access.
7. **Monitor and Improve:** Collect feedback, monitor performance, and update your data and models as needed.

