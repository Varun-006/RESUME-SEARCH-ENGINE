# 📄 Resume Search Engine

An AI-powered semantic resume search engine that finds the best candidate matches using vector embeddings and ChromaDB.

---

## 🚀 Quick Start

### 1. Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Resumes

Drop your resume files into `data/resumes/`:
```
data/
└── resumes/
    ├── john_doe.pdf
    ├── jane_smith.docx
    └── alex_jones.txt
```

### 4. Index Resumes

```bash
python ingest.py
```

### 5. Search via CLI

```bash
python search.py
```

### 6. Launch Web App

```bash
streamlit run app.py
```

---

## 🏗️ Project Structure

```
resume-search-engine/
│
├── data/
│   └── resumes/             ← Drop resumes here (PDF, DOCX, TXT)
│
├── chroma_db/               ← Auto-created vector database
│
├── utils/
│   ├── pdf_reader.py        ← PDF text extraction
│   ├── docx_reader.py       ← DOCX text extraction
│   ├── txt_reader.py        ← TXT text extraction
│   └── text_splitter.py     ← LangChain text chunking
│
├── models/
│   └── embedding.py         ← SentenceTransformer wrapper
│
├── database/
│   └── chroma_db.py         ← ChromaDB operations (add/search/delete)
│
├── ingest.py                ← Bulk indexing pipeline
├── search.py                ← CLI semantic search
├── app.py                   ← Streamlit web app
├── requirements.txt         ← Python dependencies
└── README.md
```

---

## 🛠️ How It Works

1. **Ingestion** — Resumes are read, split into chunks, and converted into 384-dimensional vectors using `all-MiniLM-L6-v2`
2. **Storage** — Vectors + text are stored in a local ChromaDB persistent database
3. **Search** — A job description is embedded the same way, then the closest vectors are returned using cosine similarity
4. **UI** — Results are displayed ranked by relevance with a match score bar

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| chromadb | 1.0.15 | Vector database |
| sentence-transformers | 5.0.0 | Embedding model |
| pypdf | 5.7.0 | PDF reading |
| streamlit | 1.47.0 | Web UI |
| torch | latest | ML backend |
| python-docx | latest | DOCX reading |
| langchain-text-splitters | latest | Text chunking |

---

## 💡 Tips

- Run `python ingest.py` any time you add new resumes to re-index
- The web app also supports direct upload from the sidebar
- Longer, more descriptive job descriptions give better results
