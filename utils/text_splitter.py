from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(text, chunk_size=500, chunk_overlap=100):
    """
    Split a long text into overlapping chunks for better embedding coverage.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)
    return chunks
