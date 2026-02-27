import json
import base64
import logging
from pathlib import Path

import streamlit as st
import typst

from src.loader import get_resumes, load_resume
from src.processor import Processor

logging.basicConfig(
    filename="data/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

_app_logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="AI Job Application Helper",
    page_icon="💼",
    layout="wide",
)


def extract_json(text: str) -> dict:
    """Extract JSON from an LLM response text."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
    raise ValueError("Failed to extract valid JSON from the response.")


def render_score(score: int | str) -> None:
    """Render a color-coded percentage score."""
    try:
        score = int(score)
    except (ValueError, TypeError):
        score = 0

    if score > 80:
        color, bg_color = "#28a745", "#e8f5e9"
    elif score >= 70:
        color, bg_color = "#ffc107", "#fff8e1"
    else:
        color, bg_color = "#dc3545", "#ffebee"

    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px; margin-bottom: 20px; border-radius: 8px; background-color: {bg_color}; border: 1px solid {color};">
            <h3 style="margin: 0; padding-bottom: 10px; color: #333; font-family: sans-serif;">Match Score</h3>
            <div style="font-size: 54px; font-weight: 700; color: {color}; font-family: sans-serif;">
                {score}%
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_pdf(bstr: bytes):
    """Render PDF bytes in an iframe."""
    b64 = base64.b64encode(bstr).decode("utf-8")
    html = f'<iframe src="data:application/pdf;base64,{b64}#toolbar=0" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(html, unsafe_allow_html=True)


def compile_typst(typst_str: str) -> bytes | None:
    """Compile Typst source code to PDF bytes."""
    tmp_path = Path("tmp_resume.typ")
    tmp_path.write_text(typst_str, encoding="utf-8")
    try:
        return typst.compile(str(tmp_path))
    except Exception as e:
        st.error(f"Typst Compilation Error: {e}")
        return None
    finally:
        tmp_path.unlink(missing_ok=True)


def reset_analysis() -> None:
    """Clear analysis results from session state."""
    keys = [
        "analyzed",
        "score",
        "new_score",
        "main_fixes",
        "missing_keywords",
        "hard_filter_risk",
        "improvements",
        "updated_typst",
        "editor_textarea",
    ]
    for key in keys:
        st.session_state.pop(key, None)


def run_analysis(
    resume_content: str, job_desc: str, resume_filename: str | None = None
):
    with st.spinner("Analyzing resume against job description..."):
        try:
            result = Processor().analyze(
                resume=resume_content,
                job_desc=job_desc,
                mode="full",
                resume_filename=resume_filename,
            )
            data = extract_json(result["content"])

            st.session_state.update(
                {
                    "analyzed": True,
                    "score": data.get("score", 0),
                    "missing_keywords": data.get("missing_keywords", []),
                    "hard_filter_risk": data.get("hard_filter_risk", "low"),
                    "improvements": data.get("improvements", []),
                    "updated_typst": resume_content,
                    "editor_textarea": resume_content,
                    "resume_filename": resume_filename,
                }
            )
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.session_state.analyzed = False


def run_rescore(resume_content: str, job_desc: str):
    with st.spinner("Re-evaluating score..."):
        try:
            result = Processor().analyze(
                resume=resume_content,
                job_desc=job_desc,
                mode="score",
                resume_filename=st.session_state.get("resume_filename"),
            )
            data = extract_json(result["content"])
            st.session_state.new_score = int(data.get("score", 0))
            st.session_state.main_fixes = data.get("main_fixes", "")
            st.rerun()
        except Exception as e:
            st.error(f"Scoring failed: {e}")


def display_results(job_desc: str):
    """Render the main analysis results and editor."""
    st.markdown("---")
    col_metrics, col_improv = st.columns([2, 3], gap="large")

    with col_metrics:
        st.markdown(
            "<h4 style='text-align: center'>Original Score</h4>", unsafe_allow_html=True
        )
        render_score(st.session_state.score)

        risk = st.session_state.get("hard_filter_risk", "low")
        if isinstance(risk, dict):
            level, reasoning = (
                risk.get("level", "low").lower(),
                risk.get("reasoning", ""),
            )
            risk_msg = f"**{level.upper()}** - {reasoning}"
        else:
            level, risk_msg = str(risk).lower(), str(risk)

        if "high" in level:
            st.error(f"**Hard Filter Risk:** {risk_msg}")
        elif "medium" in level:
            st.warning(f"**Hard Filter Risk:** {risk_msg}")
        else:
            st.success(f"**Hard Filter Risk:** {risk_msg}")

        st.markdown("#### Missing Keywords")
        keywords = st.session_state.get("missing_keywords", [])
        if keywords:
            st.markdown(" ".join(f"`{k}`" for k in keywords))
        else:
            st.success("No missing keywords!")

    with col_improv:
        st.markdown("#### Recommended Improvements")
        improvements = st.session_state.get("improvements", [])
        if improvements:
            for imp in improvements:
                if isinstance(imp, dict):
                    st.markdown(
                        f"- **{imp.get('section', 'General')}**: {imp.get('comment', '')}"
                    )
                else:
                    st.markdown(f"- {imp}")
        else:
            st.info("No specific improvements suggested.")

    st.markdown("---")
    st.markdown("### Resume Editor & Live PDF Preview")

    col_edit, col_preview = st.columns(2, gap="medium")

    with col_edit:
        st.markdown("**Typst Source Code**")
        edited_typst = st.text_area(
            "Editor", height=800, label_visibility="collapsed", key="editor_textarea"
        )

        _, btn_col, _ = st.columns([1, 2, 1])
        with btn_col:
            if st.button("🔄 Re-score Resume", use_container_width=True):
                run_rescore(edited_typst, job_desc)

    with col_preview:
        st.markdown("**PDF Preview**")
        pdf_bytes = compile_typst(edited_typst)
        if pdf_bytes:
            display_pdf(pdf_bytes)

    st.markdown("---")
    col_score_bot, col_fixes_bot = st.columns(2, gap="medium")

    with col_score_bot:
        if "new_score" in st.session_state:
            render_score(st.session_state.new_score)

        if pdf_bytes:
            st.download_button(
                label="⬇️ Download Optimized PDF",
                data=pdf_bytes,
                file_name="Optimized_Resume.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )

    with col_fixes_bot:
        if st.session_state.get("main_fixes"):
            st.info(f"**Quick fixes applied:** {st.session_state.main_fixes}")


def main():
    st.title("💼 AI Job Application Helper")
    st.subheader("Your ultimate companion for landing that dream job.")

    if "started" not in st.session_state:
        _app_logger.info("New session started")
        st.session_state.started = True

    if "analyzed" not in st.session_state:
        st.session_state.analyzed = False

    resumes_dict = get_resumes()
    if not resumes_dict:
        st.error(
            "No resumes found in the data/personal directory. Please add some .typ files."
        )
        return

    with st.sidebar:
        st.markdown("### Job Match Analysis Setup")
        selected_resume_name = st.selectbox(
            "Select Resume Template",
            options=list(resumes_dict.keys()),
            help="Choose the resume tailored for this role.",
            on_change=reset_analysis,
        )

        job_desc = st.text_area(
            "Job Description",
            height=300,
            placeholder="Paste the full job description here...",
            help="The AI will compare your resume against these requirements.",
            on_change=reset_analysis,
        )

        if st.button("Launch Analysis", use_container_width=True, type="primary"):
            if not job_desc.strip():
                st.sidebar.warning("Please paste a job description to proceed.")
            else:
                reset_analysis()
                resume_content = load_resume(resumes_dict[selected_resume_name])
                if resume_content:
                    run_analysis(
                        resume_content, job_desc, resume_filename=selected_resume_name
                    )

    if st.session_state.analyzed:
        display_results(job_desc)
    else:
        st.info(
            "👈 Choose a resume, paste a JD, and click **Launch Analysis** in the sidebar to begin!"
        )


if __name__ == "__main__":
    main()
