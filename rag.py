from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path
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
            raise ValueError(
                "MISTRAL_API_KEY not found. "
                "Please add it to your .env file."
            )

        print("Initializing Mistral...")

        llm = ChatMistralAI(
            model="mistral-small-latest",
            temperature=0.2,
            max_tokens=300,
            api_key=mistral_api_key,
            max_retries=5
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

    print("Initializing components...")

    initialize_components()

    print("Loading data...")

    loader = UnstructuredURLLoader(
        urls=urls
    )

    data = loader.load()

    if not data:
        print("No data was loaded from the URLs.")
        return

    print("Splitting text into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    docs = text_splitter.split_documents(data)

    print(f"Created {len(docs)} chunks.")

    if not docs:
        print("No documents were created.")
        return

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


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(query):

    initialize_components()

    print("\nSearching relevant documents...")

    # Retrieve relevant documents
    documents = vector_store.similarity_search(
        query,
        k=2
    )

    if not documents:
        return "I couldn't find relevant information.", ""

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
You are a helpful AI assistant for a news and
real estate information system.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context,
say that the information is not available in the
provided documents.

Do not make up information.

CONTEXT:
{context}

USER QUESTION:
{query}

Give a clear and concise answer.
"""

    # --------------------------------------------------------
    # Call Mistral with retry
    # --------------------------------------------------------

    print("Asking Mistral...")

    max_attempts = 5

    for attempt in range(1, max_attempts + 1):

        try:

            response = llm.invoke(prompt)

            answer = response.content

            return answer, "\n".join(sources)

        except Exception as e:

            error_message = str(e)

            print(
                f"\nMistral request failed "
                f"(attempt {attempt}/{max_attempts})"
            )

            print(error_message)

            # ------------------------------------------------
            # Retry 503 errors
            # ------------------------------------------------

            if "503" in error_message:

                if attempt < max_attempts:

                    wait_time = attempt * 5

                    print(
                        "Mistral is temporarily unavailable."
                    )

                    print(
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

            # ------------------------------------------------
            # Retry 429 errors
            # ------------------------------------------------

            if "429" in error_message:

                if attempt < max_attempts:

                    wait_time = attempt * 10

                    print(
                        "Mistral rate limit reached."
                    )

                    print(
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

            # ------------------------------------------------
            # Other errors
            # ------------------------------------------------

            raise


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # ========================================================
    # THE HINDU URLS
    # ========================================================

    urls = [

        "https://www.thehindu.com/news/cities/mumbai/mumbai-to-get-a-batch-of-new-ac-local-train-rakes-by-2027-cm-fadnavis/article71341090.ece",

        "https://www.thehindu.com/news/cities/mumbai/bombay-high-court-tells-banks-vijay-mallya-to-end-dispute/article71339318.ece"

    ]

    # --------------------------------------------------------
    # Step 1: Load URLs and create vector database
    # --------------------------------------------------------

    process_urls(urls)

    # --------------------------------------------------------
    # Step 2: Ask question
    # --------------------------------------------------------

    answer, sources = generate_answer(
        "What is the flyover name that connects   G Block of the Bandra-Kurla Complex?"
    )

    # --------------------------------------------------------
    # Step 3: Print answer
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(answer)

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    print(sources)
