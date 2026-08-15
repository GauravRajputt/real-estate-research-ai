import streamlit as st
from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse
import os
import time

from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_huggingface import HuggingFaceEmbeddings


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# CONSTANTS
# ============================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

VECTORSTORE_DIR = Path(__file__).parent / "resources" / "vectorstore"

COLLECTION_NAME = "real_estate"


# ============================================================
# GLOBAL VARIABLES
# ============================================================

llm = None
vector_store = None


# ============================================================
# URL CLEANER
# ============================================================

def clean_url(url):

    if not url:
        raise ValueError("URL cannot be empty.")

    url = url.strip()

    # Remove accidental Markdown URL formatting
    if url.startswith("[") and "](" in url and url.endswith(")"):
        url = url.split("](", 1)[1][:-1]

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"Invalid URL:\n{url}\n\n"
            "Please enter a complete URL beginning with "
            "http:// or https://"
        )

    if not parsed.netloc:
        raise ValueError(
            f"Invalid URL:\n{url}"
        )

    return url


# ============================================================
# INITIALIZE COMPONENTS
# ============================================================

def initialize_components():

    global llm, vector_store

    # --------------------------------------------------------
    # Initialize Mistral
    # --------------------------------------------------------

    if llm is None:

        mistral_api_key = os.getenv("MISTRAL_API_KEY")

        if not mistral_api_key:
            try: 
                mistral_api_key = st.secrets["MISTRAL_API_KEY"]
            except Exception:
                mistral_api_key = None

        if not mistral_api_key:


            raise ValueError(
                "MISTRAL_API_KEY is not configured. "
                "Add it to your .env file locally"
                "or Streamlit Cloud Secrets."
            )

        print("Initializing Mistral...")
        

        llm = ChatMistralAI(
            model="mistral-small-latest",
            temperature=0.2,
            max_tokens=300,
            api_key=mistral_api_key,
            max_retries=2
        )

    # --------------------------------------------------------
    # Initialize Vector Store
    # --------------------------------------------------------

    if vector_store is None:

        print("Initializing embeddings...")

        embedding_function = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        VECTORSTORE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embedding_function,
            persist_directory=str(VECTORSTORE_DIR)
        )


# ============================================================
# PROCESS URLS
# ============================================================

def process_urls(urls):

    if not urls:

        raise ValueError(
            "Please provide at least one URL."
        )

    # --------------------------------------------------------
    # Clean and validate URLs
    # --------------------------------------------------------

    cleaned_urls = []

    for url in urls:

        cleaned_urls.append(
            clean_url(url)
        )

    print("URLs to process:")

    for url in cleaned_urls:
        print(url)

    # --------------------------------------------------------
    # Initialize components
    # --------------------------------------------------------

    print("Initializing components...")

    initialize_components()

    # --------------------------------------------------------
    # Load webpages
    # --------------------------------------------------------

    print("Loading data...")

    try:

        loader = UnstructuredURLLoader(
            urls=cleaned_urls
        )

        data = loader.load()

    except Exception as e:

        raise RuntimeError(
            f"Could not load the provided URLs.\n\n"
            f"Error: {str(e)}"
        )

    if not data:

        raise RuntimeError(
            "No content could be extracted from the provided URLs."
        )

    # --------------------------------------------------------
    # Split documents
    # --------------------------------------------------------

    print("Splitting text into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    docs = text_splitter.split_documents(data)

    print(f"Created {len(docs)} chunks.")

    if not docs:

        raise RuntimeError(
            "No document chunks were created."
        )

    # --------------------------------------------------------
    # Add to vector database
    # --------------------------------------------------------

    print("Adding documents to vector database...")

    uuids = [
        str(uuid4())
        for _ in docs
    ]

    vector_store.add_documents(
        documents=docs,
        ids=uuids
    )

    print("Documents added successfully!")

    return len(docs)


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(query):

    if not query or not query.strip():

        return (
            "Please enter a question.",
            ""
        )

    initialize_components()

    print("\nSearching relevant documents...")

    # --------------------------------------------------------
    # Retrieve relevant documents
    # --------------------------------------------------------

    documents = vector_store.similarity_search(
        query,
        k=2
    )

    if not documents:

        return (
            "I couldn't find relevant information "
            "in the processed documents.",
            ""
        )

    # --------------------------------------------------------
    # Prepare context
    # --------------------------------------------------------

    context_parts = []

    sources = []

    for doc in documents:

        context_parts.append(
            doc.page_content
        )

        source = doc.metadata.get(
            "source",
            "Unknown source"
        )

        if source not in sources:

            sources.append(source)

    context = "\n\n--- DOCUMENT ---\n\n".join(
        context_parts
    )

    # --------------------------------------------------------
    # Create prompt
    # --------------------------------------------------------

    prompt = f"""
You are an AI research assistant.

Answer the user's question using ONLY the
information provided in the context.

Do not use outside knowledge.

Do not make up facts.

If the answer is not available in the context,
clearly say:

"The information is not available in the
provided sources."

Keep the answer clear, concise and factual.

CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    # --------------------------------------------------------
    # Call Mistral
    # --------------------------------------------------------

    print("Asking Mistral...")

    max_attempts = 5

    for attempt in range(1, max_attempts + 1):

        try:

            response = llm.invoke(prompt)

            answer = response.content

            # ------------------------------------------------
            # Handle unexpected empty response
            # ------------------------------------------------

            if not answer:

                raise RuntimeError(
                    "Mistral returned an empty response."
                )

            return (
                answer,
                "\n".join(sources)
            )

        except Exception as e:

            error_message = str(e)

            print(
                f"Mistral request failed "
                f"(attempt {attempt}/{max_attempts})"
            )

            print(error_message)

            # ------------------------------------------------
            # 503 - Service unavailable
            # ------------------------------------------------

            if "503" in error_message:

                if attempt < max_attempts:

                    wait_time = attempt * 5

                    print(
                        f"Mistral unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

            # ------------------------------------------------
            # 429 - Rate limit
            # ------------------------------------------------

            if "429" in error_message:

                if attempt < max_attempts:

                    wait_time = attempt * 10

                    print(
                        f"Rate limit reached. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

            # ------------------------------------------------
            # API key error
            # ------------------------------------------------

            if (
                "401" in error_message
                or "Unauthorized" in error_message
                or "authentication" in error_message.lower()
            ):

                raise RuntimeError(
                    "Mistral authentication failed. "
                    "Check your MISTRAL_API_KEY."
                )

            # ------------------------------------------------
            # Other errors
            # ------------------------------------------------

            raise RuntimeError(
                f"Mistral could not generate an answer.\n\n"
                f"{error_message}"
            )


# ============================================================
# TEST MODE
# ============================================================

if __name__ == "__main__":

    urls = [

        "https://www.thehindu.com/news/cities/mumbai/mumbai-to-get-a-batch-of-new-ac-local-train-rakes-by-2027-cm-fadnavis/article71341090.ece",

        "https://www.thehindu.com/news/cities/mumbai/bombay-high-court-tells-banks-vijay-mallya-to-end-dispute/article71339318.ece"

    ]

    process_urls(urls)

    answer, sources = generate_answer(
        "What is the flyover name that connects G Block of the Bandra-Kurla Complex?"
    )

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(answer)

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    print(sources) 