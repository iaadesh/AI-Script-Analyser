import streamlit as st
from models.schemas import ScriptAnalysis


# Emotion → emoji mapping for visual flair
EMOTION_ICONS = {
    "love": "❤️", "dread": "😰", "fear": "😨", "hope": "🌟", "anger": "🔥",
    "sadness": "💧", "joy": "✨", "surprise": "⚡", "longing": "🌙",
    "unease": "🌀", "tension": "⚙️", "guilt": "🪢", "grief": "🖤",
    "relief": "🌿", "betrayal": "🗡️", "confusion": "❓", "warmth": "🌞",
}


def _emotion_icon(emotion: str) -> str:
    return EMOTION_ICONS.get(emotion.lower(), "🎭")


def render_header():
    st.markdown(
        """
        <div style='text-align:center; padding: 2rem 0 1rem 0;'>
            <h1 style='font-size:2.8rem; font-weight:800; letter-spacing:-1px; margin:0;'>
                🎬 Bullet Script Intelligence
            </h1>
            <p style='color:#888; font-size:1.05rem; margin-top:0.5rem;'>
                Paste your script. Get story analysis, emotional arcs, and engagement scores — instantly.
            </p>
        </div>
        <hr style='border:none; border-top:1px solid #2a2a2a; margin-bottom:2rem;'/>
        """,
        unsafe_allow_html=True,
    )


def render_summary(analysis: ScriptAnalysis):
    st.subheader("📖 Story Summary")
    st.info(analysis.summary)


def render_emotional_analysis(analysis: ScriptAnalysis):
    ea = analysis.emotional_analysis
    st.subheader("🎭 Emotional Analysis")

    # Dominant emotions as chips
    st.markdown("**Dominant Emotions**")
    cols = st.columns(len(ea.dominant_emotions))
    for col, emotion in zip(cols, ea.dominant_emotions):
        col.markdown(
            f"<div style='background:#1e1e2e; border-radius:20px; padding:6px 14px; "
            f"text-align:center; font-size:0.9rem; border:1px solid #333;'>"
            f"{_emotion_icon(emotion)} {emotion}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # Emotional arc
    st.markdown("**Emotional Arc**")
    arc = ea.arc
    arc_cols = st.columns(3)
    arc_data = [
        ("🟢 Opening", arc.opening),
        ("🟡 Middle", arc.middle),
        ("🔴 Closing", arc.closing),
    ]
    for col, (label, text) in zip(arc_cols, arc_data):
        col.markdown(
            f"<div style='background:#111; border:1px solid #2a2a2a; border-radius:10px; "
            f"padding:14px; min-height:90px;'>"
            f"<strong style='font-size:0.8rem; color:#888;'>{label}</strong>"
            f"<p style='margin:6px 0 0 0; font-size:0.92rem;'>{text}</p></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)
    st.caption(f"**Tone:** {ea.tone_summary}")


def render_engagement(analysis: ScriptAnalysis):
    eng = analysis.engagement
    st.subheader("📊 Engagement Potential")

    # Overall score gauge
    score = eng.overall_score
    score_color = "#22c55e" if score >= 7 else "#f59e0b" if score >= 4 else "#ef4444"
    st.markdown(
        f"""
        <div style='display:flex; align-items:center; gap:1.5rem; margin-bottom:1.2rem;'>
            <div style='background:{score_color}22; border:2px solid {score_color};
                        border-radius:50%; width:80px; height:80px; display:flex;
                        align-items:center; justify-content:center; flex-shrink:0;'>
                <span style='font-size:1.8rem; font-weight:800; color:{score_color};'>{score}</span>
            </div>
            <div>
                <div style='font-size:1rem; font-weight:600;'>Overall Engagement Score</div>
                <div style='color:#888; font-size:0.9rem; margin-top:4px;'>{eng.verdict}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Factor breakdown
    for factor in eng.factors:
        bar_pct = factor.score * 10
        bar_color = "#22c55e" if factor.score >= 7 else "#f59e0b" if factor.score >= 4 else "#ef4444"
        st.markdown(
            f"""
            <div style='margin-bottom:12px;'>
                <div style='display:flex; justify-content:space-between; margin-bottom:4px;'>
                    <span style='font-size:0.9rem; font-weight:600;'>{factor.name}</span>
                    <span style='font-size:0.9rem; color:{bar_color}; font-weight:700;'>{factor.score}/10</span>
                </div>
                <div style='background:#1e1e1e; border-radius:6px; height:8px; overflow:hidden;'>
                    <div style='width:{bar_pct}%; height:100%; background:{bar_color}; border-radius:6px;
                                transition:width 0.5s ease;'></div>
                </div>
                <div style='color:#777; font-size:0.82rem; margin-top:4px;'>{factor.reasoning}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_improvements(analysis: ScriptAnalysis):
    st.subheader("🛠️ Improvement Suggestions")
    for i, suggestion in enumerate(analysis.improvement_suggestions, 1):
        with st.expander(f"{i}. {suggestion.area}", expanded=(i == 1)):
            st.write(suggestion.suggestion)


def render_cliffhanger(analysis: ScriptAnalysis):
    if not analysis.cliffhanger:
        return
    ch = analysis.cliffhanger
    st.subheader("⚡ Cliffhanger Moment")
    st.markdown(
        f"""
        <div style='background:linear-gradient(135deg,#1a0a2e,#0d0d1f); border:1px solid #7c3aed;
                    border-radius:12px; padding:20px; margin-bottom:1rem;'>
            <div style='font-size:1.1rem; font-style:italic; color:#e0d0ff; margin-bottom:10px;'>
                "{ch.moment}"
            </div>
            <div style='color:#a78bfa; font-size:0.9rem;'>{ch.explanation}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_analysis(analysis: ScriptAnalysis):
    """Master renderer — calls all section renderers in order."""
    render_summary(analysis)
    st.divider()
    render_emotional_analysis(analysis)
    st.divider()
    render_engagement(analysis)
    st.divider()
    render_improvements(analysis)
    st.divider()
    render_cliffhanger(analysis)
