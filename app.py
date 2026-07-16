import os
import sys
import tempfile

import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

from models.embedding import EmbeddingModel
from database.chroma_db import ResumeDatabase
from utils.pdf_reader import PDFReader
from utils.docx_reader import read_docx
from utils.txt_reader import read_txt
from utils.text_splitter import split_text

# -----------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="Resume Search Engine",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------
# Custom CSS — Premium dark glassmorphism design
# -----------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

/* Dark gradient background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1040 40%, #0d1b2a 100%);
    min-height: 100vh;
}

/* Hero header */
.hero-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.10));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 20px;
    margin-bottom: 2rem;
    backdrop-filter: blur(12px);
}

.hero-header h1 {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem;
}

.hero-header p {
    color: rgba(200,200,220,0.75);
    font-size: 1.05rem;
    margin: 0;
}

/* Stat cards */
.stat-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.10));
    border: 1px solid rgba(99,102,241,0.30);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(99,102,241,0.25);
}

.stat-value {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-label {
    color: rgba(180,180,210,0.75);
    font-size: 0.85rem;
    margin-top: 0.3rem;
}

/* Section headings */
.section-title {
    color: #c4b5fd;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin: 1.5rem 0 0.75rem;
}

/* Result card */
.result-card {
    background: linear-gradient(135deg, rgba(30,25,60,0.90), rgba(20,20,50,0.85));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(12px);
    transition: transform 0.2s ease, border-color 0.2s ease;
    animation: fadeSlideIn 0.4s ease forwards;
}

.result-card:hover {
    transform: translateY(-3px);
    border-color: rgba(167,139,250,0.55);
}

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.rank-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 0.75rem;
}

.result-filename {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e0d7ff;
    margin-bottom: 0.5rem;
}

.result-distance {
    font-size: 0.82rem;
    color: rgba(160,160,200,0.7);
    margin-bottom: 1rem;
}

.result-preview {
    background: rgba(0,0,0,0.35);
    border-left: 3px solid #7c3aed;
    padding: 1rem;
    border-radius: 0 10px 10px 0;
    font-size: 0.88rem;
    color: rgba(210,210,240,0.85);
    white-space: pre-wrap;
    max-height: 220px;
    overflow-y: auto;
    line-height: 1.6;
}

/* Score bar */
.score-bar-container {
    margin: 0.5rem 0 1rem;
}

.score-bar-label {
    font-size: 0.78rem;
    color: rgba(160,160,200,0.7);
    margin-bottom: 0.25rem;
}

.score-bar-outer {
    background: rgba(255,255,255,0.08);
    border-radius: 8px;
    height: 8px;
    overflow: hidden;
}

.score-bar-inner {
    height: 100%;
    border-radius: 8px;
    background: linear-gradient(90deg, #7c3aed, #60a5fa);
    transition: width 0.8s ease;
}

/* Upload area */
.upload-section {
    background: rgba(99,102,241,0.06);
    border: 1px dashed rgba(99,102,241,0.35);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,12,41,0.97) 0%, rgba(26,16,64,0.97) 100%);
    border-right: 1px solid rgba(99,102,241,0.20);
}

/* Input & Button overrides */
.stTextArea textarea {
    background: rgba(20,18,50,0.85) !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    border-radius: 12px !important;
    color: #e0d7ff !important;
    font-size: 0.95rem !important;
}

.stTextArea textarea:focus {
    border-color: rgba(167,139,250,0.7) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.35) !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,58,237,0.55) !important;
}

.stSlider [data-testid="stSliderThumb"] { background: #7c3aed !important; }

/* Hide default Streamlit elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------
# Load model and database (cached)
# -----------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_resources():
    model = EmbeddingModel()
    database = ResumeDatabase()
    return model, database


with st.spinner("🔮 Initializing AI model..."):
    model, database = load_resources()


# -----------------------------------------------------------------------
# Sidebar — Upload & Ingest
# -----------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📥 Upload Resumes")
    st.markdown("Add resumes to the search index by uploading them here.")

    uploaded_files = st.file_uploader(
        "Choose resume files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Supports PDF, DOCX, and TXT formats"
    )

    if uploaded_files:
        if st.button("⚡ Index Uploaded Resumes"):
            resumes_to_store = []
            chunk_id_offset = database.count()

            with st.spinner("Processing resumes..."):
                for uploaded_file in uploaded_files:
                    try:
                        ext = uploaded_file.name.lower().split(".")[-1]
                        text = ""

                        # Save to temp file for reading
                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=f".{ext}"
                        ) as tmp:
                            tmp.write(uploaded_file.getbuffer())
                            tmp_path = tmp.name

                        if ext == "pdf":
                            reader = PDFReader(os.path.dirname(tmp_path))
                            text = reader.extract_text_from_pdf(tmp_path)
                        elif ext == "docx":
                            text = read_docx(tmp_path)
                        elif ext == "txt":
                            text = read_txt(tmp_path)

                        os.unlink(tmp_path)

                        if text.strip():
                            chunks = split_text(text)
                            for chunk in chunks:
                                embedding = model.create_embedding(chunk)
                                resumes_to_store.append({
                                    "id": str(chunk_id_offset),
                                    "filename": uploaded_file.name,
                                    "text": chunk,
                                    "embedding": embedding
                                })
                                chunk_id_offset += 1

                    except Exception as e:
                        st.error(f"Error reading {uploaded_file.name}: {e}")

            if resumes_to_store:
                database.add_multiple_resumes(resumes_to_store)
                st.success(f"✅ Indexed {len(uploaded_files)} file(s) — {len(resumes_to_store)} chunk(s) added!")
                st.rerun()
            else:
                st.warning("No text could be extracted from the uploaded files.")

    st.divider()

    st.markdown("### 🗄️ Database")
    count = database.count()
    st.metric("Chunks Indexed", count)

    if st.button("🗑️ Clear All Data", help="Remove all indexed resumes"):
        database.delete_all()
        st.success("Database cleared!")
        st.rerun()

    st.divider()
    st.markdown("""
    <div style='color: rgba(160,160,200,0.6); font-size: 0.78rem; line-height: 1.6;'>
    <b>How it works:</b><br>
    1. Upload or ingest resumes<br>
    2. Enter a job description<br>
    3. AI finds the closest matches using semantic embeddings
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------
# Main Content
# -----------------------------------------------------------------------
st.markdown("""
<div class="hero-header">
    <h1>📄 Resume Search Engine</h1>
    <p>Find the best candidates instantly using AI-powered semantic search</p>
</div>
""", unsafe_allow_html=True)

# Stats row
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{database.count()}</div>
        <div class="stat-label">Chunks Indexed</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">384</div>
        <div class="stat-label">Embedding Dimensions</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">3</div>
        <div class="stat-label">Supported Formats</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Search box
st.markdown('<div class="section-title">🔍 Search Query</div>', unsafe_allow_html=True)
query = st.text_area(
    "Enter Job Description",
    placeholder="Example: Senior Python Developer with Django, REST APIs, and AWS experience...",
    height=130,
    label_visibility="collapsed"
)

col_left, col_right = st.columns([3, 1])
with col_left:
    top_k = st.slider(
        "Number of results",
        min_value=1,
        max_value=min(10, max(database.count(), 1)),
        value=min(5, max(database.count(), 1)),
        help="How many top matching resumes to show"
    )
with col_right:
    st.markdown("<br>", unsafe_allow_html=True)

search_clicked = st.button("🔍  Search Resumes")

# -----------------------------------------------------------------------
# Search & Results
# -----------------------------------------------------------------------
if search_clicked:
    if not query.strip():
        st.warning("⚠️ Please enter a job description to search.")
    elif database.count() == 0:
        st.error("❌ No resumes indexed yet. Upload resumes using the sidebar.")
    else:
        with st.spinner("🤖 Finding best matches..."):
            query_embedding = model.create_embedding(query)
            results = database.search(query_embedding, top_k=top_k)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        if not documents:
            st.info("No results found.")
        else:
            st.markdown(f"<br>", unsafe_allow_html=True)
            st.markdown(
                f'<div class="section-title">🏆 Top {len(documents)} Matching Resume(s)</div>',
                unsafe_allow_html=True
            )

            # Normalize distances to similarity scores (lower distance = higher score)
            max_dist = max(distances) if max(distances) > 0 else 1
            min_dist = min(distances)

            for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
                # Convert distance to a 0-100 match score
                score = max(0, min(100, int((1 - (dist - min_dist) / (max_dist - min_dist + 1e-6)) * 100)))
                if len(documents) == 1:
                    score = max(0, int((1 - dist) * 100))

                bar_color = "#22c55e" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"

                st.markdown(f"""
                <div class="result-card" style="animation-delay: {i * 0.08}s;">
                    <span class="rank-badge">Rank #{i + 1}</span>
                    <div class="result-filename">📄 {meta['filename']}</div>
                    <div class="result-distance">Distance Score: {round(dist, 4)}</div>
                    <div class="score-bar-container">
                        <div class="score-bar-label">Match Relevance — {score}%</div>
                        <div class="score-bar-outer">
                            <div class="score-bar-inner" style="width: {score}%; background: linear-gradient(90deg, {bar_color}, #60a5fa);"></div>
                        </div>
                    </div>
                    <div class="result-preview">{doc[:800]}</div>
                </div>
                """, unsafe_allow_html=True)
