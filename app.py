import streamlit as st
from pathlib import Path
import sys


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORT AGRICULTURE ASSISTANT
# ============================================================

from pipeline.rag_pipeline import AgricultureRAGPipeline


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Tamil Nadu Agriculture Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# IMPORTANT:
# Only CSS is injected.
# No visible HTML <div> elements are used.
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       MAIN BACKGROUND
    ------------------------------------------------------- */

    .stApp {
        background-color: #eaf6ea;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }


    /* -------------------------------------------------------
       HEADER
    ------------------------------------------------------- */

    .header-box {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px 24px;
        border: 1px solid #d4e6d4;
        margin-bottom: 15px;
    }


    /* -------------------------------------------------------
       SEARCH
    ------------------------------------------------------- */

    div[data-testid="stTextInput"] input {
        height: 48px;
        border: 2px solid #76a97d;
        border-radius: 10px;
        background-color: white;
        font-size: 16px;
        color: #244d2e;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #176b3a;
        box-shadow: 0 0 0 1px #176b3a;
    }


    /* -------------------------------------------------------
       BUTTONS
    ------------------------------------------------------- */

    div.stButton > button {
        width: 100%;
        min-height: 46px;
        border-radius: 9px;
        border: 1px solid #c8ddc9;
        background-color: #ffffff;
        color: #245c38;
        font-weight: 600;
        font-size: 15px;
    }

    div.stButton > button:hover {
        background-color: #e7f5e8;
        border-color: #176b3a;
        color: #176b3a;
    }


    /* Search button */

    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #176b3a;
        color: white;
        border: none;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        background-color: #12552d;
        color: white;
    }


    /* -------------------------------------------------------
       ANSWER BOX
    ------------------------------------------------------- */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* -------------------------------------------------------
       SIDEBAR
    ------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background-color: #f4fbf4;
        border-right: 1px solid #d4e6d4;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #176b3a;
    }


    /* -------------------------------------------------------
       EXPANDER
    ------------------------------------------------------- */

    details {
        background-color: #ffffff;
        border: 1px solid #d5e5d5;
        border-radius: 8px;
    }


    /* -------------------------------------------------------
       FOOTER
    ------------------------------------------------------- */

    .footer-text {
        text-align: center;
        color: #718074;
        font-size: 12px;
        padding-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

with st.container():

    st.markdown(
        "### 🌾 Department of Agriculture & Farmers Welfare"
    )

    st.caption(
        "Tamil Nadu Agriculture Information Portal"
    )

    st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🌾 Agriculture Services")

    st.divider()

    st.markdown("### 📚 Agriculture Schemes")
    st.caption(
        "Government schemes and subsidies"
    )

    st.markdown("### 👨‍🌾 Farmers Corner")
    st.caption(
        "Useful information for farmers"
    )

    st.markdown("### 🌱 Crop Information")
    st.caption(
        "Crop-related information"
    )

    st.markdown("### 💧 Irrigation")
    st.caption(
        "Irrigation schemes and assistance"
    )

    st.divider()

    st.markdown("### ℹ️ Help")

    st.caption(
        "Enter your agriculture question "
        "and click Search."
    )

    st.caption(
        "You can also use the Agriculture "
        "Services buttons."
    )


# ============================================================
# LOAD AGRICULTURE ASSISTANT
# ============================================================

@st.cache_resource(show_spinner=False)
def load_agriculture_assistant():

    return AgricultureRAGPipeline()


try:

    assistant = load_agriculture_assistant()

except Exception as error:

    st.error(
        "🌾 Agriculture information service "
        "could not be started."
    )

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "question" not in st.session_state:

    st.session_state.question = ""


if "answer" not in st.session_state:

    st.session_state.answer = ""


if "sources" not in st.session_state:

    st.session_state.sources = []


if "search_clicked" not in st.session_state:

    st.session_state.search_clicked = False


# ============================================================
# SEARCH SECTION
# ============================================================

st.subheader("🔎 Search Agriculture Information")

st.caption(
    "Ask about Tamil Nadu agriculture schemes, "
    "subsidies, crops or irrigation."
)


# ------------------------------------------------------------
# Search input
# ------------------------------------------------------------

question = st.text_input(
    "Agriculture Question",
    value=st.session_state.question,
    placeholder=(
        "Example: What subsidy is available "
        "for micro irrigation?"
    ),
    label_visibility="collapsed",
)


# ============================================================
# SEARCH BUTTON
# ============================================================

search_col1, search_col2, search_col3 = st.columns(
    [1, 2, 1]
)

with search_col2:

    search_clicked = st.button(
        "🔎 Search Agriculture Information",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# AGRICULTURE SERVICES
# ============================================================

st.subheader("🌱 Agriculture Services")

c1, c2, c3, c4 = st.columns(
    4,
    gap="medium"
)


# ------------------------------------------------------------
# Agriculture Schemes
# ------------------------------------------------------------

with c1:

    scheme_clicked = st.button(
        "📚 Agriculture Schemes",
        use_container_width=True,
    )


# ------------------------------------------------------------
# Farmers Corner
# ------------------------------------------------------------

with c2:

    farmer_clicked = st.button(
        "👨‍🌾 Farmers Corner",
        use_container_width=True,
    )


# ------------------------------------------------------------
# Crop Information
# ------------------------------------------------------------

with c3:

    crop_clicked = st.button(
        "🌱 Crop Information",
        use_container_width=True,
    )


# ------------------------------------------------------------
# Irrigation
# ------------------------------------------------------------

with c4:

    irrigation_clicked = st.button(
        "💧 Irrigation",
        use_container_width=True,
    )


# ============================================================
# QUICK QUESTION HANDLING
# ============================================================

quick_question = None


if scheme_clicked:

    quick_question = (
        "What agriculture schemes and subsidies "
        "are available for farmers in Tamil Nadu?"
    )


elif farmer_clicked:

    quick_question = (
        "What government assistance and benefits "
        "are available for farmers in Tamil Nadu?"
    )


elif crop_clicked:

    quick_question = (
        "What crop related schemes, assistance "
        "and information are available for farmers?"
    )


elif irrigation_clicked:

    quick_question = (
        "What irrigation subsidies and assistance "
        "are available for farmers in Tamil Nadu?"
    )


# ============================================================
# DETERMINE WHETHER TO SEARCH
# ============================================================

final_question = None


# Search button clicked

if search_clicked:

    if question.strip():

        final_question = question.strip()

    else:

        st.warning(
            "🌾 Please enter an agriculture question "
            "before searching."
        )


# Quick service button clicked

elif quick_question:

    final_question = quick_question

    st.session_state.question = quick_question


# ============================================================
# RUN AGRICULTURE ASSISTANT
# ============================================================

if final_question:

    st.divider()

    st.subheader("🌾 Agriculture Information")

    with st.spinner(
        "Finding relevant agriculture information..."
    ):

        try:

            # ------------------------------------------------
            # Call existing pipeline
            # ------------------------------------------------

            if hasattr(assistant, "ask"):

                result = assistant.ask(
                    final_question
                )

            elif hasattr(assistant, "run"):

                result = assistant.run(
                    final_question
                )

            elif hasattr(assistant, "query"):

                result = assistant.query(
                    final_question
                )

            elif hasattr(assistant, "self_rag"):

                result = assistant.self_rag(
                    final_question
                )

            else:

                raise AttributeError(
                    "AgricultureRAGPipeline must contain "
                    "ask(), run(), query(), or self_rag()."
                )


            # =================================================
            # HANDLE PIPELINE RESULT
            # =================================================

            answer = ""
            sources = []


            # -------------------------------------------------
            # CASE 1: String
            # -------------------------------------------------

            if isinstance(result, str):

                answer = result


            # -------------------------------------------------
            # CASE 2: Tuple
            # -------------------------------------------------

            elif isinstance(result, tuple):

                if len(result) >= 1:

                    answer = result[0]

                if len(result) >= 2:

                    sources = result[1]


            # -------------------------------------------------
            # CASE 3: Dictionary
            # -------------------------------------------------

            elif isinstance(result, dict):

                answer = (
                    result.get("answer")
                    or result.get("response")
                    or result.get("result")
                    or result.get("output")
                    or ""
                )

                sources = (
                    result.get("sources")
                    or result.get("documents")
                    or []
                )


            # -------------------------------------------------
            # CASE 4: Other object
            # -------------------------------------------------

            else:

                answer = str(result)


            # =================================================
            # CLEAN ANSWER
            # =================================================

            if not answer:

                answer = (
                    "I could not find enough information "
                    "in the available Tamil Nadu agriculture "
                    "data to answer this question."
                )


            # =================================================
            # DISPLAY ANSWER
            # =================================================

            st.success(answer)


            # =================================================
            # SOURCES
            # =================================================

            if sources:

                with st.expander(
                    "📄 Information Sources"
                ):

                    for source in sources:

                        if isinstance(
                            source,
                            dict
                        ):

                            source_name = (
                                source.get("source")
                                or source.get("file")
                                or source.get(
                                    "metadata",
                                    {}
                                ).get(
                                    "source"
                                )
                                or "Tamil Nadu Agriculture"
                            )

                        else:

                            source_name = str(
                                source
                            )


                        st.write(
                            f"📄 {Path(source_name).name}"
                        )


        except Exception as error:

            st.error(
                "Sorry, I could not process your "
                "agriculture question right now."
            )

            # Technical error only in terminal,
            # NOT shown to the farmer.
            print(
                f"Agriculture application error: {error}"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🌾 Tamil Nadu Agriculture Information Portal "
    "• Farmer Support"
)