# BIA Work Placement Pre-Approval Checker

Live demo: https://bia-project.onrender.com/

A FastAPI-based web application that semantically evaluates internship job responsibilities against approved **Business Insights & Analytics (BIA)** work placement role requirements using sentence embeddings and cosine similarity. The tool is designed to support work placement pre-approval decisions, not to automate final approval.

## How It Works
1. Student selects an intended BIA role  
2. Student pastes internship job responsibilities  
3. Text is embedded using a transformer-based model  
4. Cosine similarity is computed against role requirements  
5. The result is compared to a configurable threshold and displayed to the student  

## Technology
- FastAPI and Uvicorn  
- Sentence-Transformers (`all-MiniLM-L6-v2`)  
  https://www.sbert.net/docs/pretrained_models.html  
- Cosine similarity for semantic matching  

## Project Structure
api.py – FastAPI routes and HTML UI  
matcher.py – Embedding and similarity logic  
config.py – Role definitions, thresholds, future weighting  

## Run Locally
pip install -r requirements.txt  
uvicorn api:app --reload  

Open: http://127.0.0.1:8000

## Notes & Future Work
- Role requirements are currently static and will be refined  
- Planned enhancements include weighted scoring (role/company), multi-step workflows, and saving results  
- The application provides guidance and transparency, not final approval  

## License
Apache License 2.0
