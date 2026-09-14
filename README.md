🌾 Tamil Nadu Agriculture AI Assistant

An AI-powered Retrieval-Augmented Generation (RAG) application designed to help farmers access information about Tamil Nadu agriculture schemes, subsidies, irrigation assistance, farmer services, and crop-related information.

The application collects agriculture information from configured Tamil Nadu agriculture websites, processes the content into searchable chunks, creates embeddings, stores them in a vector database, and uses an OpenAI language model to provide answers grounded in the collected agriculture information.

📌 Project Overview

Farmers often need to search through multiple government pages to understand:

Available agriculture schemes

Subsidies and assistance

Eligibility information

Required documents

Application procedures

Irrigation-related assistance

Crop-related information

Farmer services

This application provides a simple farmer-friendly Streamlit interface where users can ask questions in natural language.

The application does not perform a live web search while answering a farmer's question. Answers are generated from the application's locally processed agriculture knowledge base.

✨ Key Features

🌐 Agriculture Website Scraping

Opens configured Tamil Nadu agriculture websites.

Extracts webpage content.

Downloads available PDF documents.

Stores collected information locally under data/schemes.

📄 Document Processing

Reads downloaded PDF files.

Extracts text using pypdf.

Combines webpage and PDF content.

Splits large content into smaller chunks.

🧠 RAG Pipeline

The application follows this flow:

Agriculture Website
        ↓
Web Scraping
        ↓
PDF Download + Webpage Content
        ↓
Text Extraction
        ↓
Text Splitter
        ↓
Document Chunks
        ↓
Embeddings
        ↓
Vector Store
        ↓
Retriever
        ↓
Relevant Agriculture Information
        ↓
Guardrails
        ↓
Self-RAG / Corrective RAG
        ↓
OpenAI LLM
        ↓
Farmer-friendly Answer

🛡️ Guardrails

NeMo Guardrails is used to help control the assistant's responses and keep the application focused on its intended agriculture domain.

🔎 Self-RAG

The application checks whether the retrieved information is relevant enough before generating an answer.

🔄 Corrective RAG

If the retrieved information is insufficient or not relevant, the application can perform corrective retrieval logic instead of blindly generating an answer.

💬 Streamlit UI

The front end provides:

Agriculture-focused design

Green agriculture theme

Search/chat interface

Quick-access agriculture service buttons

Farmer-friendly terminology

Clear answers

Source information when available

🏗️ Project Structure

A recommended project structure is:

Agriculture_RAG_Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── assets/
│   ├── agriculture1.jpg
│   ├── agriculture2.jpg
│   └── ...
│
├── data/
│   └── schemes/
│       ├── webpage_content/
│       ├── pdfs/
│       └── processed/
│
├── scraper/
│   ├── __init__.py
│   ├── scraper.py
│   └── pdf_extractor.py
│
├── ingestion/
│   ├── __init__.py
│   └── ingestion.py
│
├── retrieval/
│   ├── __init__.py
│   ├── vector_store.py
│   └── retriever.py
│
├── rag/
│   ├── __init__.py
│   ├── self_rag.py
│   ├── corrective_rag.py
│   ├── hybrid_retriever.py
│   └── hybrid_reranker.py
│
├── guardrails/
│   ├── config/
│   └── ...
│
└── vectorstore/
    └── ...

Your exact folder names may differ depending on the final implementation. Keep app.py as the Streamlit entry point.

🔑 Technologies Used

Technology

Purpose

Python

Application development

Streamlit

Front-end UI

Playwright

Website scraping

pypdf

PDF text extraction

LangChain

RAG/retrieval pipeline

OpenAI GPT-4o-mini

Answer generation

text-embedding-3-small

Text embeddings

FAISS

Vector storage/search

NeMo Guardrails

Response guardrails

BM25

Keyword-based retrieval

Cross-Encoder

Reranking

python-dotenv

Environment variable management

⚙️ Requirements

Recommended:

Python 3.10+

VS Code

Internet connection for initial website scraping and model/API access

OpenAI API key

Playwright browser installation

🚀 Installation

1. Clone or create the project

Open PowerShell in VS Code:

cd C:\Users\Dell\Documents\SocialEagle_AI_Learning\Week2

Create/open your project:

cd Agriculture_RAG_Assistant

2. Create a virtual environment

python -m venv venv

Activate it:

.\venv\Scripts\Activate.ps1

You should see:

(venv) PS C:\...\Agriculture_RAG_Assistant>

📦 Install Dependencies

Install the required packages:

pip install streamlit
pip install langchain
pip install langchain-openai
pip install langchain-community
pip install openai
pip install faiss-cpu
pip install pypdf
pip install python-dotenv
pip install playwright
pip install rank-bm25
pip install sentence-transformers
pip install nemoguardrails

Then install the Playwright browser:

python -m playwright install chromium

🔐 Configure OpenAI API Key

Create a file named:

.env

Add:

OPENAI_API_KEY=your_openai_api_key_here

The API key must never be hard-coded inside Python files.

The application should load it using:

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

🔒 Protect Your API Key

Create .gitignore:

venv/
.env
__pycache__/
*.pyc
.streamlit/
data/
vectorstore/
.vscode/

Never commit .env to GitHub.

🌐 Knowledge Base

The first version is designed around:

Tamil Nadu Agriculture / Agrisnet

Configured agriculture sources can be added to the scraper.

For example:

https://www.tnagrisnet.tn.gov.in/home/index/en

Additional approved Tamil Nadu agriculture sources can be configured in the scraping module.

The knowledge base should contain Tamil Nadu agriculture information only.

🕷️ Website Scraping

The scraper is responsible for:

Opening the agriculture website.

Reading webpage content.

Finding relevant scheme pages.

Finding downloadable PDF documents.

Downloading PDFs.

Saving webpage/PDF information under:

data/schemes/

Example:

data/
└── schemes/
    ├── webpage_content/
    │   ├── agriculture_schemes.txt
    │   └── farmer_services.txt
    │
    └── pdfs/
        ├── scheme_001.pdf
        ├── scheme_002.pdf
        └── ...

📄 PDF Processing

PDF documents are processed using pypdf.

Example:

from pypdf import PdfReader

reader = PdfReader("scheme.pdf")

for page in reader.pages:
    text = page.extract_text()
    print(text)

The extracted text is then passed to the document processing pipeline.

✂️ Text Splitting

Large documents are divided into smaller chunks before creating embeddings.

Typical configuration:

chunk_size = 1000
chunk_overlap = 150

The exact values can be adjusted based on retrieval quality.

🧠 Embeddings

The application uses:

text-embedding-3-small

to convert document chunks into numerical vectors.

Conceptually:

Agriculture Text
       ↓
Embedding Model
       ↓
Vector

🗄️ Vector Store

FAISS is used as the local vector database.

The vector store allows the application to find agriculture information semantically related to a farmer's question.

Example:

Question:
"What subsidy is available for drip irrigation?"

        ↓

Embedding

        ↓

FAISS Search

        ↓

Relevant irrigation chunks

        ↓

LLM

🔎 Retrieval

The retriever searches the vector store for relevant information.

The system can also combine semantic retrieval with keyword retrieval such as BM25.

Example:

Farmer Question
      ↓
Semantic Retrieval
      +
BM25 Retrieval
      ↓
Candidate Documents
      ↓
Reranking
      ↓
Best Relevant Context

🛡️ Guardrails

NeMo Guardrails is used to keep responses aligned with the application's purpose.

The assistant should primarily answer questions related to:

Tamil Nadu agriculture schemes

Farmer assistance

Agriculture subsidies

Irrigation

Crops

Seeds

Government agriculture services

Eligibility

Application procedures

Required documents

For unrelated questions, the assistant should politely explain that the information is outside the application's agriculture knowledge base.

Example:

User:
What is the current stock price of Apple?

Assistant:
Sorry, I can help with Tamil Nadu agriculture schemes,
farmer assistance, subsidies, crops and related
agriculture services.

🔄 Self-RAG

Self-RAG adds an additional relevance check.

Example:

Question
   ↓
Retrieve documents
   ↓
Check relevance
   ↓
Relevant?
 ┌───────┴────────┐
Yes               No
 ↓                 ↓
Generate       Corrective Retrieval
Answer              ↓
                 Check Again

This reduces the chance of generating answers from unrelated documents.

🔁 Corrective RAG

Corrective RAG helps when the first retrieval result is weak.

For example:

Question:
"What subsidy is available for sprinkler irrigation?"

        ↓

Initial Retrieval

        ↓

Weak Results?

        ↓

Corrective Retrieval

        ↓

Retrieve better irrigation information

        ↓

Generate answer

💬 Running the Application

From the project root:

streamlit run app.py

The Streamlit application will open in your browser.

🧪 Recommended Test Questions

Use these questions to test the application.

Agriculture Schemes

What agriculture schemes are available for farmers in Tamil Nadu?

What subsidies are available for farmers?

How can I apply for an agriculture scheme?

Irrigation

What subsidy is available for micro irrigation?

What subsidy is available for drip irrigation?

What subsidy is available for sprinkler irrigation?

What are the benefits of micro irrigation?

Who can apply for micro irrigation subsidy?

Documents

What documents are required to apply for micro irrigation subsidy?

Is Aadhaar required for the application?

Farmer Assistance

What assistance is available for small and marginal farmers?

What farmer services are available in Tamil Nadu?

🚫 Out-of-Scope Testing

Test the guardrails using unrelated questions:

What is today's gold price?

Who will win the next cricket match?

Give me a Python programming tutorial.

The assistant should politely indicate that it is designed for Tamil Nadu agriculture-related information.

🎨 User Interface

The Streamlit UI is designed to be simple and farmer friendly.

The interface focuses on agriculture terminology instead of exposing technical RAG terminology.

Example service areas:

🌾 Agriculture Schemes
👨‍🌾 Farmers Corner
🌱 Crop Information
💧 Irrigation

The user can either:

Click a service button.

Type a question.

Receive an answer from the local agriculture knowledge base.

The application uses a green agriculture-inspired theme.

🔐 Data Privacy

The application is designed to use a locally stored knowledge base.

The application does not perform live web searching for each farmer question.

Instead:

Website/PDF
    ↓
Local Knowledge Base
    ↓
Vector Store
    ↓
Retriever
    ↓
Answer

API credentials should always be stored in environment variables.

⚠️ Important Notes

API Key

Never write:

OPENAI_API_KEY = "sk-..."

inside the source code.

Use .env instead.

Knowledge Base

When agriculture website content changes, rerun the ingestion/scraping process so that the local knowledge base can be refreshed.

Storage

PDFs, extracted content and vector databases can consume significant disk space. If the system is running on a machine with limited disk space, periodically remove old generated files and rebuild the vector store.

🛠️ Troubleshooting

ModuleNotFoundError

Example:

ModuleNotFoundError: No module named 'langchain...'

Make sure the virtual environment is activated:

.\venv\Scripts\Activate.ps1

Then install the missing package.

Streamlit Not Found

pip install streamlit

Run:

streamlit run app.py

Playwright Browser Error

Run:

python -m playwright install chromium

OpenAI API Key Error

Check that .env exists in the project root:

Agriculture_RAG_Assistant/
├── app.py
└── .env

And contains:

OPENAI_API_KEY=your_key_here

No Relevant Answer

Check:

The scheme/PDF exists under data/schemes.

PDF text extraction is working.

Documents were split correctly.

Embeddings were generated.

FAISS/vector store was created.

Retriever is returning relevant chunks.

The question is related to the stored agriculture information.

📊 Expected Application Flow

When the user starts:

                    app.py
                      │
                      ▼
              Start Application
                      │
                      ▼
             Scrape Agriculture Site
                      │
                      ▼
           Download Web/PDF Content
                      │
                      ▼
              Process Documents
                      │
                      ▼
                Split Chunks
                      │
                      ▼
                Create Embeddings
                      │
                      ▼
                Build Vector Store
                      │
                      ▼
                  Start UI
                      │
                      ▼
             Farmer asks question
                      │
                      ▼
                  Retrieve
                      │
                      ▼
                Guardrails
                      │
                      ▼
             Self/Corrective RAG
                      │
                      ▼
                 OpenAI LLM
                      │
                      ▼
             Farmer-friendly answer

🎯 Project Objective

The main objective of this project is to provide farmers with a simple conversational interface for accessing Tamil Nadu agriculture information.

Instead of searching through multiple government webpages and documents, a farmer can ask:

"What subsidy is available for micro irrigation?"

and receive a relevant answer based on the application's agriculture knowledge base.

🚀 Future Enhancements

Possible future improvements include:

Tamil-language question and answer support

Voice-based farmer assistance

District-specific scheme filtering

Crop-specific recommendations

Eligibility checker

Subsidy calculator

Application-status integration

Multilingual UI

Mobile-friendly design

More Tamil Nadu government agriculture sources

Source document/page references

Admin dashboard for knowledge-base updates

Scheduled knowledge-base refresh

👩‍🌾 Target Users

The application is intended for:

Farmers

Small and marginal farmers

Agriculture students

Agriculture officers

Farmer-support teams

Agriculture-related service providers

📜 Disclaimer

This application is an AI-based information assistant. Information provided by the application is based on the agriculture documents and webpages available in its knowledge base.

Users should verify important scheme eligibility, subsidy amounts, application deadlines, and official procedures with the relevant Tamil Nadu government agriculture department before taking action.

🏆 Buildathon Highlights

This project demonstrates the following AI concepts:

Web Scraping
      +
Document Processing
      +
Text Chunking
      +
Embeddings
      +
Vector Database
      +
Semantic Retrieval
      +
Hybrid Retrieval
      +
Reranking
      +
Guardrails
      +
Self-RAG
      +
Corrective RAG
      +
LLM
      +
Streamlit

The final experience hides these technical components from the farmer and presents a simple agriculture-focused conversational assistant.

🌾 Conclusion

Tamil Nadu Agriculture AI Assistant combines government agriculture information with modern RAG techniques to make scheme and subsidy information easier to discover.

The goal is simple:

Ask an agriculture question → Retrieve trusted stored information → Provide a clear farmer-friendly answer.