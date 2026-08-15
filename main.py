import streamlit as st
from rag import process_urls, generate_answer


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResearchAI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM UI CSS
# ============================================================

st.html("""
<style>

    /* ========================================================
       GLOBAL
    ======================================================== */

    html, body, [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 0% 0%,
                rgba(99, 102, 241, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 100% 20%,
                rgba(6, 182, 212, 0.07),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #f8fafc 0%,
                #f4f7ff 45%,
                #faf8ff 100%
            );

        color: #172033 !important;
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 35px;
        padding-bottom: 70px;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ========================================================
       REMOVE DEFAULT STREAMLIT DECORATIONS
    ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #ffffff 0%,
                #f8faff 100%
            ) !important;

        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] > div {
        padding: 25px 20px;
    }

    section[data-testid="stSidebar"] * {
        color: #1e293b;
    }

    /* ========================================================
       BRAND
    ======================================================== */

    .brand-container {
        text-align: center;
        padding: 8px 0 28px 0;
    }

    .brand-logo {
        width: 64px;
        height: 64px;

        margin: 0 auto 13px auto;

        border-radius: 19px;

        display: flex;
        align-items: center;
        justify-content: center;

        background:
            linear-gradient(
                135deg,
                #4f46e5 0%,
                #7c3aed 50%,
                #0891b2 100%
            );

        color: #ffffff !important;

        font-size: 29px;

        box-shadow:
            0 14px 35px rgba(79, 70, 229, 0.27);

        position: relative;
    }

    .brand-title {
        font-size: 22px;
        font-weight: 800;

        color: #111827 !important;

        letter-spacing: -0.5px;
    }

    .brand-subtitle {
        font-size: 12px;

        color: #64748b !important;

        margin-top: 5px;
    }

    /* ========================================================
       SIDEBAR HEADINGS
    ======================================================== */

    section[data-testid="stSidebar"] h3 {
        color: #111827 !important;
        font-weight: 750 !important;
    }

    section[data-testid="stSidebar"] p {
        color: #64748b !important;
    }

    /* ========================================================
       INPUTS
    ======================================================== */

    .stTextInput label {
        color: #475569 !important;
        font-weight: 600 !important;
    }

    .stTextInput input {

        background: #ffffff !important;

        color: #172033 !important;

        -webkit-text-fill-color: #172033 !important;

        border: 1px solid #d7deea !important;

        border-radius: 11px !important;

        min-height: 44px !important;

        padding: 10px 13px !important;

        font-size: 14px !important;

        box-shadow:
            0 2px 7px rgba(15, 23, 42, 0.03) !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease,
            transform 0.2s ease !important;
    }

    .stTextInput input::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    .stTextInput input:hover {
        border-color: #a5b4fc !important;
    }

    .stTextInput input:focus {
        border-color: #6366f1 !important;

        box-shadow:
            0 0 0 3px rgba(99, 102, 241, 0.12),
            0 5px 15px rgba(79, 70, 229, 0.06) !important;
    }

    /* ========================================================
       PREMIUM BUTTON
    ======================================================== */

    .stButton > button {

        width: 100% !important;

        min-height: 46px !important;

        border: 1px solid #4f46e5 !important;

        border-radius: 11px !important;

        background:
            linear-gradient(
                135deg,
                #4f46e5 0%,
                #6366f1 50%,
                #7c3aed 100%
            ) !important;

        color: #ffffff !important;

        -webkit-text-fill-color: #ffffff !important;

        font-size: 14px !important;

        font-weight: 700 !important;

        letter-spacing: 0.1px;

        box-shadow:
            0 8px 20px rgba(79, 70, 229, 0.22) !important;

        transition:
            all 0.22s ease !important;
    }

    /* VERY IMPORTANT:
       Keep text white when hovering */

    .stButton > button:hover {

        background:
            linear-gradient(
                135deg,
                #4338ca 0%,
                #4f46e5 50%,
                #6d28d9 100%
            ) !important;

        color: #ffffff !important;

        -webkit-text-fill-color: #ffffff !important;

        border-color: #4338ca !important;

        transform: translateY(-2px) !important;

        box-shadow:
            0 12px 28px rgba(79, 70, 229, 0.32) !important;
    }

    .stButton > button:active {

        background:
            linear-gradient(
                135deg,
                #3730a3,
                #5b21b6
            ) !important;

        color: #ffffff !important;

        transform: translateY(0px) !important;
    }

    .stButton > button p {
        color: #ffffff !important;
    }

    .stButton > button span {
        color: #ffffff !important;
    }

    /* ========================================================
       HERO
    ======================================================== */

    .hero-container {

        position: relative;

        overflow: hidden;

        background:
            linear-gradient(
                135deg,
                #eef2ff 0%,
                #f5f3ff 42%,
                #ecfeff 100%
            );

        border: 1px solid #dbe4ff;

        border-radius: 26px;

        padding: 48px;

        margin-bottom: 28px;

        box-shadow:
            0 20px 60px rgba(79, 70, 229, 0.10);
    }

    .hero-container::before {

        content: "";

        position: absolute;

        width: 320px;
        height: 320px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(99,102,241,0.15),
                transparent 70%
            );

        top: -180px;
        right: -80px;
    }

    .hero-container::after {

        content: "";

        position: absolute;

        width: 230px;
        height: 230px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(6,182,212,0.12),
                transparent 70%
            );

        bottom: -140px;
        left: -60px;
    }

    .hero-content {
        position: relative;
        z-index: 5;
    }

    .hero-badge {

        display: inline-block;

        padding: 7px 14px;

        border-radius: 999px;

        background: rgba(255,255,255,0.82);

        border: 1px solid #d8defe;

        color: #4f46e5 !important;

        font-size: 11px;

        font-weight: 800;

        letter-spacing: 1px;

        margin-bottom: 17px;
    }

    .hero-title {

        font-size: 48px;

        line-height: 1.08;

        font-weight: 850;

        letter-spacing: -2px;

        color: #111827 !important;

        margin: 0;
    }

    .hero-highlight {

        background:
            linear-gradient(
                90deg,
                #4f46e5,
                #7c3aed,
                #0891b2
            );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;
    }

    .hero-description {

        max-width: 720px;

        margin-top: 18px;

        color: #64748b !important;

        font-size: 16px;

        line-height: 1.75;
    }

    /* ========================================================
       STAT CARDS
    ======================================================== */

    .stat-card {

        background: rgba(255,255,255,0.92);

        border: 1px solid #e5e7eb;

        border-radius: 18px;

        padding: 20px;

        box-shadow:
            0 8px 30px rgba(15,23,42,0.05);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            border-color 0.2s ease;
    }

    .stat-card:hover {

        transform: translateY(-3px);

        border-color: #c7d2fe;

        box-shadow:
            0 15px 35px rgba(79,70,229,0.10);
    }

    .stat-icon {

        width: 40px;
        height: 40px;

        border-radius: 11px;

        display: flex;

        align-items: center;

        justify-content: center;

        font-size: 18px;

        margin-bottom: 13px;
    }

    .icon-purple {
        background: #ede9fe;
        color: #7c3aed !important;
    }

    .icon-blue {
        background: #dbeafe;
        color: #2563eb !important;
    }

    .icon-cyan {
        background: #cffafe;
        color: #0891b2 !important;
    }

    .stat-number {

        font-size: 26px;

        font-weight: 850;

        color: #111827 !important;
    }

    .stat-label {

        font-size: 12px;

        color: #64748b !important;

        margin-top: 3px;
    }

    /* ========================================================
       QUESTION SECTION
    ======================================================== */

    .question-card {

        background: #ffffff;

        border: 1px solid #e5e7eb;

        border-radius: 20px;

        padding: 26px;

        margin-top: 26px;

        box-shadow:
            0 8px 30px rgba(15,23,42,0.05);
    }

    .section-heading {

        font-size: 20px;

        font-weight: 800;

        color: #111827 !important;
    }

    .section-description {

        font-size: 13px;

        color: #64748b !important;

        margin-top: 5px;

        margin-bottom: 18px;
    }

    /* ========================================================
       QUESTION INPUT - SPECIAL
    ======================================================== */

    div[data-testid="stTextInput"] input {

        background: #ffffff !important;

        color: #172033 !important;

        -webkit-text-fill-color: #172033 !important;
    }

    /* ========================================================
       ANSWER CARD
    ======================================================== */

    .answer-card {

        background:
            linear-gradient(
                135deg,
                #ffffff 0%,
                #fafbff 100%
            );

        border: 1px solid #dbe4ff;

        border-left: 5px solid #6366f1;

        border-radius: 20px;

        padding: 30px;

        margin-top: 26px;

        box-shadow:
            0 14px 45px rgba(79,70,229,0.08);
    }

    .answer-badge {

        color: #4f46e5 !important;

        font-size: 11px;

        font-weight: 850;

        letter-spacing: 1.1px;

        text-transform: uppercase;

        margin-bottom: 10px;
    }

    .answer-title {

        font-size: 23px;

        font-weight: 800;

        color: #111827 !important;

        margin-bottom: 16px;
    }

    .answer-content {

        color: #334155 !important;

        font-size: 16px;

        line-height: 1.85;

        white-space: pre-wrap;

        word-wrap: break-word;
    }

    .answer-content * {

        color: #334155 !important;
    }

    /* ========================================================
       SOURCES
    ======================================================== */

    .sources-header {

        margin-top: 32px;

        font-size: 20px;

        font-weight: 800;

        color: #111827 !important;
    }

    .sources-description {

        color: #64748b !important;

        font-size: 13px;

        margin-top: 4px;

        margin-bottom: 16px;
    }

    .source-card {

        background: #ffffff;

        border: 1px solid #e5e7eb;

        border-radius: 14px;

        padding: 16px 18px;

        margin-bottom: 10px;

        box-shadow:
            0 5px 20px rgba(15,23,42,0.035);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .source-card:hover {

        transform: translateX(4px);

        border-color: #c7d2fe;

        box-shadow:
            0 8px 25px rgba(79,70,229,0.08);
    }

    .source-number {

        color: #7c3aed !important;

        font-size: 10px;

        font-weight: 850;

        letter-spacing: 1px;

        text-transform: uppercase;

        margin-bottom: 5px;
    }

    .source-text {

        color: #2563eb !important;

        font-size: 13px;

        word-break: break-all;
    }

    /* ========================================================
       STATUS
    ======================================================== */

    .status-ready {

        background:
            linear-gradient(
                135deg,
                #ecfdf5,
                #f0fdf4
            );

        border: 1px solid #bbf7d0;

        color: #15803d !important;

        border-radius: 11px;

        padding: 12px;

        text-align: center;

        font-size: 12px;

        font-weight: 700;

        box-shadow:
            0 5px 15px rgba(22,163,74,0.06);
    }

    .status-waiting {

        background:
            linear-gradient(
                135deg,
                #fff7ed,
                #fffbeb
            );

        border: 1px solid #fed7aa;

        color: #c2410c !important;

        border-radius: 11px;

        padding: 12px;

        text-align: center;

        font-size: 12px;

        font-weight: 700;
    }

    /* ========================================================
       SUCCESS MESSAGE
    ======================================================== */

    div[data-testid="stAlert"] {

        border-radius: 11px !important;
    }

    /* ========================================================
       SPINNER
    ======================================================== */

    div[data-testid="stSpinner"] {

        color: #4f46e5 !important;
    }

    /* ========================================================
       FOOTER
    ======================================================== */

    .footer {

        text-align: center;

        margin-top: 55px;

        padding-top: 25px;

        border-top: 1px solid #e5e7eb;

        color: #94a3b8 !important;

        font-size: 12px;
    }

    /* ========================================================
       MOBILE
    ======================================================== */

    @media (max-width: 768px) {

        .hero-container {
            padding: 30px;
        }

        .hero-title {
            font-size: 34px;
            letter-spacing: -1px;
        }

    }

</style>
""")


# ============================================================
# SESSION STATE
# ============================================================

if "processed" not in st.session_state:
    st.session_state.processed = False

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "sources" not in st.session_state:
    st.session_state.sources = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html("""
    <div class="brand-container">

        <div class="brand-logo">
            🔎
        </div>

        <div class="brand-title">
            ResearchAI
        </div>

        <div class="brand-subtitle">
            Intelligent web research assistant
        </div>

    </div>
    """)

    st.markdown("### Knowledge Sources")

    st.caption(
        "Add up to three articles or web pages."
    )

    url1 = st.text_input(
        "Source 1",
        placeholder="Paste article URL..."
    )

    url2 = st.text_input(
        "Source 2",
        placeholder="Paste article URL..."
    )

    url3 = st.text_input(
        "Source 3",
        placeholder="Paste article URL..."
    )

    st.write("")

    process_button = st.button(
        "Process Sources",
        use_container_width=True
    )

    st.write("")

    if st.session_state.processed:

        st.html("""
        <div class="status-ready">
            ✓ Sources are ready for research
        </div>
        """)

    else:

        st.html("""
        <div class="status-waiting">
            Waiting for sources
        </div>
        """)


# ============================================================
# PROCESS SOURCES
# ============================================================

if process_button:

    urls = [
        url.strip()
        for url in [url1, url2, url3]
        if url and url.strip()
    ]

    if not urls:

        st.sidebar.error(
            "Please enter at least one URL."
        )

    else:

        try:

            with st.sidebar:

                with st.spinner(
                    "Processing sources..."
                ):

                    process_urls(urls)

            st.session_state.processed = True

            st.session_state.answer = ""

            st.session_state.sources = []

            st.sidebar.success(
                f"{len(urls)} source(s) processed successfully."
            )

        except Exception as e:

            st.session_state.processed = False

            st.sidebar.error(
                f"Processing failed: {str(e)}"
            )


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero-container">

    <div class="hero-content">

        <div class="hero-badge">
            AI RESEARCH PLATFORM
        </div>

        <div class="hero-title">
            Turn web sources into
            <span class="hero-highlight">
                clear answers.
            </span>
        </div>

        <div class="hero-description">
            Research multiple articles, retrieve the most relevant
            information, and ask questions using an intelligent
            source-grounded research assistant.
        </div>

    </div>

</div>
""")


# ============================================================
# STAT CARDS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.html("""
    <div class="stat-card">

        <div class="stat-icon icon-purple">
            🌐
        </div>

        <div class="stat-number">
            03
        </div>

        <div class="stat-label">
            Maximum web sources
        </div>

    </div>
    """)


with col2:

    st.html("""
    <div class="stat-card">

        <div class="stat-icon icon-blue">
            ✦
        </div>

        <div class="stat-number">
            AI
        </div>

        <div class="stat-label">
            Intelligent answers
        </div>

    </div>
    """)


with col3:

    st.html("""
    <div class="stat-card">

        <div class="stat-icon icon-cyan">
            ◈
        </div>

        <div class="stat-number">
            RAG
        </div>

        <div class="stat-label">
            Source-grounded research
        </div>

    </div>
    """)


# ============================================================
# QUESTION CARD
# ============================================================

st.html("""
<div class="question-card">

    <div class="section-heading">
        Ask your research question
    </div>

    <div class="section-description">
        Ask anything about the information contained
        in your processed sources.
    </div>

</div>
""")


query = st.text_input(
    "Research question",
    placeholder=(
        "Example: What are the major developments "
        "mentioned in these articles?"
    ),
    label_visibility="collapsed"
)


# ============================================================
# GENERATE ANSWER
# ============================================================

if query:

    if not st.session_state.processed:

        st.warning(
            "Please process your sources first."
        )

    else:

        try:

            with st.spinner(
                "AI is analyzing your sources..."
            ):

                answer, sources = generate_answer(query)

            st.session_state.answer = answer

            st.session_state.sources = [
                source.strip()
                for source in sources.split("\n")
                if source.strip()
            ]

        except Exception as e:

            st.error(
                f"Unable to generate answer: {str(e)}"
            )


# ============================================================
# ANSWER
# ============================================================

if st.session_state.answer:

    # Escape basic HTML characters so the model's answer
    # doesn't accidentally break our UI.
    import html

    safe_answer = html.escape(
        st.session_state.answer
    )

    st.html(f"""
    <div class="answer-card">

        <div class="answer-badge">
            AI RESEARCH RESULT
        </div>

        <div class="answer-title">
            Here's what I found
        </div>

        <div class="answer-content">
            {safe_answer}
        </div>

    </div>
    """)


# ============================================================
# SOURCES
# ============================================================

if st.session_state.sources:

    st.html("""
    <div class="sources-header">
        Research Sources
    </div>

    <div class="sources-description">
        These sources were retrieved and used to generate the answer.
    </div>
    """)

    for i, source in enumerate(
        st.session_state.sources,
        start=1
    ):

        import html

        safe_source = html.escape(source)

        st.html(f"""
        <div class="source-card">

            <div class="source-number">
                SOURCE {i}
            </div>

            <div class="source-text">
                {safe_source}
            </div>

        </div>
        """)


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">
    ResearchAI &nbsp;•&nbsp;
    AI-powered source-grounded research
</div>
""")