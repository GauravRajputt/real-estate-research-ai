import streamlit as st
from rag import process_urls, generate_answer
import html


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
# SESSION STATE
# ============================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "processed" not in st.session_state:
    st.session_state.processed = False

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "sources" not in st.session_state:
    st.session_state.sources = []

if "source_count" not in st.session_state:
    st.session_state.source_count = 0


# ============================================================
# THEME
# ============================================================

dark = st.session_state.theme == "dark"


if dark:

    BG = "#07111F"
    BG_SECONDARY = "#0B1728"

    CARD = "#101D2F"
    CARD_SECONDARY = "#132238"

    INPUT_BG = "#0D1B2E"

    TEXT = "#F8FAFC"
    TEXT_SECONDARY = "#B7C3D4"
    TEXT_MUTED = "#8493A8"

    BORDER = "#263A54"

    PRIMARY = "#6366F1"
    PRIMARY_HOVER = "#818CF8"

    PURPLE = "#8B5CF6"
    CYAN = "#06B6D4"

    GREEN = "#22C55E"
    YELLOW = "#F59E0B"

else:

    BG = "#F4F7FB"
    BG_SECONDARY = "#FFFFFF"

    CARD = "#FFFFFF"
    CARD_SECONDARY = "#F8FAFC"

    INPUT_BG = "#FFFFFF"

    TEXT = "#111827"
    TEXT_SECONDARY = "#475569"
    TEXT_MUTED = "#64748B"

    BORDER = "#D7E0EB"

    PRIMARY = "#4F46E5"
    PRIMARY_HOVER = "#6366F1"

    PURPLE = "#7C3AED"
    CYAN = "#0891B2"

    GREEN = "#16A34A"
    YELLOW = "#D97706"


# ============================================================
# PREMIUM CSS
# ============================================================

st.html(
    f"""
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

* {{
    box-sizing: border-box;
}}

html,
body,
[class*="css"] {{
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}}

.stApp {{
    background:
        radial-gradient(
            circle at 0% 0%,
            rgba(99,102,241,0.12),
            transparent 25%
        ),
        radial-gradient(
            circle at 100% 10%,
            rgba(6,182,212,0.09),
            transparent 25%
        ),
        {BG} !important;

    color: {TEXT} !important;
}}


/* ============================================================
   MAIN CONTAINER
   ============================================================ */

.main .block-container {{
    max-width: 1300px;

    padding-top: 30px;
    padding-bottom: 70px;
}}


/* ============================================================
   STREAMLIT HEADER
   ============================================================ */

[data-testid="stHeader"] {{
    background: transparent !important;
}}


/* ============================================================
   HIDE STREAMLIT DEFAULT UI
   ============================================================ */

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {{
    background:
        linear-gradient(
            180deg,
            {BG_SECONDARY},
            {BG}
        ) !important;

    border-right:
        1px solid {BORDER} !important;
}}

section[data-testid="stSidebar"] > div {{
    padding:
        25px 18px !important;
}}

section[data-testid="stSidebar"] * {{
    color:
        {TEXT} !important;
}}

section[data-testid="stSidebar"] p {{
    color:
        {TEXT_MUTED} !important;
}}

section[data-testid="stSidebar"] label {{
    color:
        {TEXT_SECONDARY} !important;
}}


/* ============================================================
   SIDEBAR BRAND
   ============================================================ */

.brand {{
    text-align: center;

    padding:
        5px 0 20px 0;
}}

.brand-icon {{
    width: 58px;
    height: 58px;

    margin:
        0 auto 12px auto;

    border-radius:
        17px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    font-size:
        27px;

    background:
        linear-gradient(
            135deg,
            {PRIMARY},
            {PURPLE},
            {CYAN}
        );

    box-shadow:
        0 12px 30px rgba(99,102,241,0.25);
}}

.brand-name {{
    font-size:
        22px;

    font-weight:
        850;

    color:
        {TEXT} !important;
}}

.brand-subtitle {{
    margin-top:
        4px;

    font-size:
        11px;

    line-height:
        1.5;

    color:
        {TEXT_MUTED} !important;
}}


/* ============================================================
   SIDEBAR THEME BUTTON
   ============================================================ */

section[data-testid="stSidebar"] .stButton > button {{
    min-height:
        48px !important;

    border-radius:
        12px !important;

    background:
        linear-gradient(
            135deg,
            {PRIMARY},
            {CYAN}
        ) !important;

    border:
        none !important;

    color:
        #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;

    font-weight:
        750 !important;
}}


/* ============================================================
   SIDEBAR STAT SECTION
   ============================================================ */

.sidebar-stats-title {{
    font-size:
        15px;

    font-weight:
        800;

    margin-top:
        12px;

    margin-bottom:
        12px;

    color:
        {TEXT} !important;
}}


/* ============================================================
   COMPACT SIDEBAR STAT CARDS
   ============================================================ */

.sidebar-stat {{
    display:
        flex;

    align-items:
        center;

    gap:
        12px;

    background:
        {CARD};

    border:
        1px solid {BORDER};

    border-radius:
        13px;

    padding:
        11px 13px;

    margin-bottom:
        9px;

    min-height:
        62px;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.05);
}}

.sidebar-stat-icon {{
    width:
        38px;

    height:
        38px;

    min-width:
        38px;

    border-radius:
        10px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    font-size:
        17px;
}}

.sidebar-purple {{
    background:
        rgba(139,92,246,0.15);
}}

.sidebar-blue {{
    background:
        rgba(59,130,246,0.15);
}}

.sidebar-green {{
    background:
        rgba(34,197,94,0.15);
}}

.sidebar-stat-content {{
    display:
        flex;

    flex-direction:
        column;
}}

.sidebar-stat-number {{
    font-size:
        18px;

    line-height:
        1.1;

    font-weight:
        850;

    color:
        {TEXT} !important;
}}

.sidebar-stat-label {{
    font-size:
        10px;

    margin-top:
        3px;

    color:
        {TEXT_MUTED} !important;
}}


/* ============================================================
   SIDEBAR STATUS
   ============================================================ */

.ready {{
    background:
        rgba(34,197,94,0.10);

    border:
        1px solid rgba(34,197,94,0.28);

    color:
        {GREEN} !important;

    border-radius:
        10px;

    padding:
        10px;

    text-align:
        center;

    font-size:
        11px;

    font-weight:
        750;

    margin-top:
        12px;
}}

.waiting {{
    background:
        rgba(245,158,11,0.10);

    border:
        1px solid rgba(245,158,11,0.28);

    color:
        {YELLOW} !important;

    border-radius:
        10px;

    padding:
        10px;

    text-align:
        center;

    font-size:
        11px;

    font-weight:
        750;

    margin-top:
        12px;
}}


/* ============================================================
   MAIN HERO
   ============================================================ */

.hero {{
    position:
        relative;

    overflow:
        hidden;

    background:
        linear-gradient(
            135deg,
            {CARD},
            {CARD_SECONDARY}
        );

    border:
        1px solid {BORDER};

    border-radius:
        25px;

    padding:
        45px;

    margin-bottom:
        25px;

    box-shadow:
        0 20px 55px rgba(0,0,0,0.10);
}}

.hero::before {{
    content:
        "";

    position:
        absolute;

    width:
        300px;

    height:
        300px;

    border-radius:
        50%;

    background:
        radial-gradient(
            circle,
            rgba(99,102,241,0.17),
            transparent 70%
        );

    top:
        -170px;

    right:
        -80px;
}}

.hero::after {{
    content:
        "";

    position:
        absolute;

    width:
        220px;

    height:
        220px;

    border-radius:
        50%;

    background:
        radial-gradient(
            circle,
            rgba(6,182,212,0.12),
            transparent 70%
        );

    bottom:
        -130px;

    left:
        -60px;
}}

.hero-content {{
    position:
        relative;

    z-index:
        2;
}}

.badge {{
    display:
        inline-block;

    padding:
        7px 13px;

    border-radius:
        999px;

    background:
        rgba(99,102,241,0.12);

    border:
        1px solid rgba(99,102,241,0.28);

    color:
        {PRIMARY} !important;

    font-size:
        11px;

    font-weight:
        850;

    letter-spacing:
        1px;

    margin-bottom:
        15px;
}}

.hero-title {{
    font-size:
        47px;

    line-height:
        1.08;

    font-weight:
        850;

    letter-spacing:
        -1.8px;

    color:
        {TEXT} !important;
}}

.gradient-text {{
    background:
        linear-gradient(
            90deg,
            {PRIMARY},
            {PURPLE},
            {CYAN}
        );

    -webkit-background-clip:
        text;

    -webkit-text-fill-color:
        transparent;
}}

.hero-description {{
    max-width:
        850px;

    margin-top:
        17px;

    color:
        {TEXT_SECONDARY} !important;

    font-size:
        15px;

    line-height:
        1.75;
}}


/* ============================================================
   MAIN SOURCE SECTION
   ============================================================ */

.source-section {{
    background:
        {CARD};

    border:
        1px solid {BORDER};

    border-radius:
        20px;

    padding:
        25px;

    margin-top:
        20px;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.06);
}}

.section-title {{
    font-size:
        21px;

    font-weight:
        800;

    color:
        {TEXT} !important;

    margin-bottom:
        5px;
}}

.section-description {{
    font-size:
        13px;

    color:
        {TEXT_MUTED} !important;

    margin-bottom:
        18px;
}}


/* ============================================================
   MAIN URL INPUTS
   ============================================================ */

.source-section + div .stTextInput input,
.main .stTextInput input {{
    background:
        {INPUT_BG} !important;

    color:
        {TEXT} !important;

    -webkit-text-fill-color:
        {TEXT} !important;

    border:
        1px solid {BORDER} !important;

    border-radius:
        13px !important;

    min-height:
        52px !important;

    padding:
        13px 15px !important;

    font-size:
        14px !important;

    box-shadow:
        0 4px 14px rgba(0,0,0,0.04) !important;
}}

.stTextInput input::placeholder {{
    color:
        {TEXT_MUTED} !important;

    opacity:
        1 !important;
}}

.stTextInput input:focus {{
    border:
        2px solid {PRIMARY} !important;

    box-shadow:
        0 0 0 3px rgba(99,102,241,0.13) !important;
}}


/* ============================================================
   MAIN BUTTONS
   ============================================================ */

.stButton > button {{
    width:
        100% !important;

    min-height:
        50px !important;

    border:
        none !important;

    border-radius:
        13px !important;

    background:
        linear-gradient(
            135deg,
            {PRIMARY},
            {PURPLE},
            {CYAN}
        ) !important;

    color:
        #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;

    font-size:
        14px !important;

    font-weight:
        800 !important;

    box-shadow:
        0 8px 22px rgba(99,102,241,0.24) !important;

    transition:
        all 0.2s ease !important;
}}

.stButton > button:hover {{
    transform:
        translateY(-2px) !important;

    box-shadow:
        0 12px 30px rgba(99,102,241,0.34) !important;

    color:
        #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;
}}

.stButton > button p,
.stButton > button span {{
    color:
        #FFFFFF !important;

    -webkit-text-fill-color:
        #FFFFFF !important;
}}


/* ============================================================
   QUESTION SECTION
   ============================================================ */

.question-section {{
    background:
        {CARD};

    border:
        1px solid {BORDER};

    border-radius:
        21px;

    padding:
        27px;

    margin-top:
        25px;

    box-shadow:
        0 10px 35px rgba(0,0,0,0.07);
}}

.question-title {{
    font-size:
        23px;

    font-weight:
        800;

    color:
        {TEXT} !important;
}}

.question-description {{
    font-size:
        13px;

    color:
        {TEXT_MUTED} !important;

    margin-top:
        5px;

    margin-bottom:
        18px;
}}


/* ============================================================
   LARGE QUESTION BOX
   ============================================================ */

textarea {{
    min-height:
        240px !important;

    height:
        240px !important;

    background:
        {INPUT_BG} !important;

    color:
        {TEXT} !important;

    -webkit-text-fill-color:
        {TEXT} !important;

    border:
        1px solid {BORDER} !important;

    border-radius:
        16px !important;

    padding:
        18px !important;

    font-size:
        16px !important;

    line-height:
        1.6 !important;

    box-shadow:
        0 5px 20px rgba(0,0,0,0.05) !important;
}}

textarea::placeholder {{
    color:
        {TEXT_MUTED} !important;

    opacity:
        1 !important;
}}

textarea:focus {{
    border:
        2px solid {PRIMARY} !important;

    box-shadow:
        0 0 0 4px rgba(99,102,241,0.12) !important;
}}


/* ============================================================
   ASK BUTTON
   ============================================================ */

.ask-button {{
    margin-top:
        8px;
}}


/* ============================================================
   ANSWER
   ============================================================ */

.answer {{
    background:
        linear-gradient(
            135deg,
            {CARD},
            {CARD_SECONDARY}
        );

    border:
        1px solid {BORDER};

    border-left:
        5px solid {GREEN};

    border-radius:
        20px;

    padding:
        30px;

    margin-top:
        27px;

    box-shadow:
        0 15px 45px rgba(0,0,0,0.09);
}}

.answer-label {{
    color:
        {GREEN};

    font-size:
        11px;

    font-weight:
        850;

    letter-spacing:
        1.2px;

    margin-bottom:
        8px;
}}

.answer-title {{
    font-size:
        23px;

    font-weight:
        800;

    color:
        {TEXT};
}}

.answer-text {{
    margin-top:
        15px;

    color:
        {TEXT_SECONDARY};

    font-size:
        16px;

    line-height:
        1.85;

    white-space:
        pre-wrap;

    word-break:
        break-word;
}}


/* ============================================================
   SOURCES
   ============================================================ */

.sources-title {{
    margin-top:
        30px;

    font-size:
        20px;

    font-weight:
        800;

    color:
        {TEXT};
}}

.sources-description {{
    color:
        {TEXT_MUTED};

    font-size:
        13px;

    margin-top:
        4px;

    margin-bottom:
        15px;
}}

.source-card {{
    background:
        {CARD};

    border:
        1px solid {BORDER};

    border-radius:
        14px;

    padding:
        16px 18px;

    margin-bottom:
        10px;

    box-shadow:
        0 5px 18px rgba(0,0,0,0.04);
}}

.source-number {{
    color:
        {CYAN};

    font-size:
        10px;

    font-weight:
        850;

    letter-spacing:
        1px;

    margin-bottom:
        5px;
}}

.source-text {{
    color:
        {TEXT_SECONDARY};

    font-size:
        13px;

    word-break:
        break-all;
}}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {{
    text-align:
        center;

    margin-top:
        50px;

    padding-top:
        20px;

    border-top:
        1px solid {BORDER};

    color:
        {TEXT_MUTED};

    font-size:
        12px;
}}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {{

    .hero {{
        padding:
            30px;
    }}

    .hero-title {{
        font-size:
            35px;
    }}

    textarea {{
        min-height:
            200px !important;

        height:
            200px !important;
    }}

}}

</style>
"""
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    st.html(
        """
        <div class="brand">

            <div class="brand-icon">
                🔎
            </div>

            <div class="brand-name">
                ResearchAI
            </div>

            <div class="brand-subtitle">
                Intelligent source-grounded
                research assistant
            </div>

        </div>
        """
    )

    st.divider()

    # --------------------------------------------------------
    # THEME
    # --------------------------------------------------------

    theme_text = (
        "☀️ Switch to Light Mode"
        if dark
        else
        "🌙 Switch to Dark Mode"
    )

    if st.button(
        theme_text,
        use_container_width=True
    ):

        st.session_state.theme = (
            "light"
            if dark
            else
            "dark"
        )

        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # SYSTEM OVERVIEW
    # --------------------------------------------------------

    st.html(
        """
        <div class="sidebar-stats-title">
            ⚡ System Overview
        </div>
        """
    )

    # 03

    st.html(
        """
        <div class="sidebar-stat">

            <div class="sidebar-stat-icon sidebar-purple">
                🌐
            </div>

            <div class="sidebar-stat-content">

                <div class="sidebar-stat-number">
                    03
                </div>

                <div class="sidebar-stat-label">
                    Maximum web sources
                </div>

            </div>

        </div>
        """
    )

    # AI

    st.html(
        """
        <div class="sidebar-stat">

            <div class="sidebar-stat-icon sidebar-blue">
                ✦
            </div>

            <div class="sidebar-stat-content">

                <div class="sidebar-stat-number">
                    AI
                </div>

                <div class="sidebar-stat-label">
                    Intelligent answers
                </div>

            </div>

        </div>
        """
    )

    # RAG

    st.html(
        """
        <div class="sidebar-stat">

            <div class="sidebar-stat-icon sidebar-green">
                ◈
            </div>

            <div class="sidebar-stat-content">

                <div class="sidebar-stat-number">
                    RAG
                </div>

                <div class="sidebar-stat-label">
                    Source-grounded research
                </div>

            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if st.session_state.processed:

        st.html(
            """
            <div class="ready">
                ✓ Sources are ready
            </div>
            """
        )

    else:

        st.html(
            """
            <div class="waiting">
                ● Waiting for sources
            </div>
            """
        )


# ============================================================
# MAIN PAGE — HERO
# ============================================================

st.html(
    """
    <div class="hero">

        <div class="hero-content">

            <div class="badge">
                ✦ AI RESEARCH PLATFORM
            </div>

            <div class="hero-title">
                Research smarter.
                <br>
                Get
                <span class="gradient-text">
                    clear answers.
                </span>
            </div>

            <div class="hero-description">
                Add trusted web sources, process their
                information, and ask questions in natural
                language. ResearchAI retrieves relevant
                information and generates source-grounded
                answers.
            </div>

        </div>

    </div>
    """
)


# ============================================================
# MAIN PAGE — URL SOURCES
# ============================================================

st.html(
    """
    <div class="source-section">

        <div class="section-title">
            🌐 Add your research sources
        </div>

        <div class="section-description">
            Add up to three articles or web pages that
            ResearchAI should use as its knowledge base.
        </div>

    </div>
    """
)


# ============================================================
# URL INPUTS
# ============================================================

url_col1, url_col2, url_col3 = st.columns(
    3,
    gap="medium"
)


with url_col1:

    url1 = st.text_input(
        "Source 1",
        placeholder="https://example.com/article",
        key="main_url_1"
    )


with url_col2:

    url2 = st.text_input(
        "Source 2",
        placeholder="https://example.com/article",
        key="main_url_2"
    )


with url_col3:

    url3 = st.text_input(
        "Source 3",
        placeholder="https://example.com/article",
        key="main_url_3"
    )


# ============================================================
# PROCESS SOURCES BUTTON
# ============================================================

st.write("")

process_button = st.button(
    "⚡ Process Sources",
    use_container_width=True
)


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

        st.error(
            "Please enter at least one URL."
        )

        st.session_state.processed = False

    else:

        try:

            with st.spinner(
                "Processing your sources..."
            ):

                process_urls(urls)

            st.session_state.processed = True

            st.session_state.source_count = len(urls)

            st.session_state.answer = ""

            st.session_state.sources = []

            st.success(
                f"✓ {len(urls)} source(s) processed successfully."
            )

        except Exception as e:

            st.session_state.processed = False

            st.error(
                "Source processing failed."
            )

            st.code(
                str(e),
                language="text"
            )


# ============================================================
# QUESTION SECTION
# ============================================================

st.html(
    """
    <div class="question-section">

        <div class="question-title">
            🔎 Ask your research question
        </div>

        <div class="question-description">
            Ask anything about the information contained
            in your processed sources.
        </div>

    </div>
    """
)


# ============================================================
# LARGE QUESTION BOX
# ============================================================

query = st.text_area(
    "Research question",

    placeholder=(
        "What would you like to know about these sources?"
    ),

    height=240,

    label_visibility="collapsed",

    key="research_question"
)


# ============================================================
# ASK BUTTON
# ============================================================

st.html(
    '<div class="ask-button"></div>'
)

ask_button = st.button(
    "🔎 Ask ResearchAI",
    use_container_width=True
)


# ============================================================
# GENERATE ANSWER
# ============================================================

if ask_button:

    if not query.strip():

        st.warning(
            "Please enter a research question."
        )

    elif not st.session_state.processed:

        st.warning(
            "Please process your sources first."
        )

    else:

        try:

            with st.spinner(
                "ResearchAI is analyzing your sources..."
            ):

                answer, sources = generate_answer(
                    query.strip()
                )

            st.session_state.answer = answer

            if sources:

                st.session_state.sources = [
                    source.strip()
                    for source in sources.split("\n")
                    if source.strip()
                ]

            else:

                st.session_state.sources = []

        except Exception as e:

            st.session_state.answer = ""

            st.session_state.sources = []

            st.error(
                "Unable to generate the answer."
            )

            st.code(
                str(e),
                language="text"
            )


# ============================================================
# ANSWER
# ============================================================

if st.session_state.answer:

    safe_answer = html.escape(
        str(st.session_state.answer)
    )

    st.html(
        f"""
        <div class="answer">

            <div class="answer-label">
                AI RESEARCH RESULT
            </div>

            <div class="answer-title">
                Here's what I found
            </div>

            <div class="answer-text">
                {safe_answer}
            </div>

        </div>
        """
    )


# ============================================================
# SOURCES USED
# ============================================================

if st.session_state.sources:

    st.html(
        """
        <div class="sources-title">
            📚 Research Sources
        </div>

        <div class="sources-description">
            These sources were retrieved and used to
            generate the answer.
        </div>
        """
    )

    for i, source in enumerate(
        st.session_state.sources,
        start=1
    ):

        safe_source = html.escape(
            str(source)
        )

        st.html(
            f"""
            <div class="source-card">

                <div class="source-number">
                    SOURCE {i}
                </div>

                <div class="source-text">
                    {safe_source}
                </div>

            </div>
            """
        )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">
        ResearchAI &nbsp;•&nbsp;
        AI-powered source-grounded research
    </div>
    """
)