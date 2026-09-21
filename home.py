"""Portfolio-first Home page for Rashid Ali's visual studio."""

from pathlib import Path

import streamlit as st


def navigate(page: str) -> None:
    st.session_state["navigation"] = page


def render_home(assets: Path) -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    .st-key-home { --home-green: #296b35; }
    .st-key-home h1, .st-key-home h2, .st-key-home h3 {
        font-family: 'Archivo', sans-serif;
        color: #17291d;
    }
    .st-key-home p, .st-key-home button {
        font-family: 'Space Grotesk', sans-serif;
    }
    .home-intro { padding: 34px 0 18px; }
    .home-eyebrow { color: #296b35; font-size: .76rem; font-weight: 700;
        letter-spacing: .13em; text-transform: uppercase; }
    .home-brand { display: flex; flex-wrap: wrap; align-items: baseline;
        gap: .35rem .65rem; line-height: 1.6; }
    .home-brand span { white-space: normal; overflow-wrap: break-word; max-width: 100%; }
    .home-brand .studio-name { text-transform: none; letter-spacing: .025em; }
    .home-intro h1 { font-size: clamp(2.7rem, 4.8vw, 4.8rem);
        line-height: 1.05; letter-spacing: -.055em; margin: 22px 0; }
    .home-intro h1 span { color: #296b35; }
    .home-intro p { max-width: 520px; font-size: 1.06rem; line-height: 1.75; color: #4c5e52; }
    .home-section { padding: 46px 0 12px; }
    .home-section h2 { font-size: clamp(1.8rem, 3vw, 2.5rem); margin: 10px 0; letter-spacing: -.04em; }
    .home-section p { color: #4c5e52; max-width: 650px; line-height: 1.7; }
    .home-card { min-height: 245px; padding: 28px; border: 1px solid #d2ddd3;
        border-radius: 20px; background: #fff; box-shadow: 0 4px 16px #17291d05; }
    .home-card .number { color: #296b35; font-size: .8rem; letter-spacing: .12em; }
    .home-card h3 { font-size: 1.35rem; margin: 28px 0 12px; }
    .home-card p { color: #4c5e52; line-height: 1.7; font-size: 1rem; margin: 0; }
    .st-key-home img { border-radius: 20px; }
    .st-key-home-portrait img { max-height: 470px; object-fit: contain; background: #e6e9e3; }
    .st-key-home button { background: #296b35; border: 1px solid #296b35;
        color: #fff; box-shadow: none; border-radius: 999px; padding: .65rem 1.4rem;
        min-height: 48px; transition: background .2s ease; }
    .st-key-home button p { color: inherit; }
    .st-key-home button:hover { background: #1c4e27; border-color: #1c4e27; }
    .st-key-home button:focus-visible { outline: 3px solid #17291d; outline-offset: 4px; }
    .st-key-home-contact button { background: transparent; color: #296b35; }
    .st-key-home-contact button:hover { color: white; }
    .home-note { border-top: 1px solid #d2ddd3; border-bottom: 1px solid #d2ddd3;
        padding: 19px 0; margin: 24px 0 4px; display: flex; flex-wrap: wrap;
        gap: 12px 30px; font-size: .85rem; color: #4c5e52; }
    .st-key-home-closing { margin-top: 44px; padding: 32px; border-radius: 22px;
        background: #e9f2e6; border: 1px solid #d2ddd3; }
    .home-closing h2 { font-size: clamp(1.8rem, 3vw, 2.6rem); margin: 8px 0 14px; }
    .home-closing p { color: #4c5e52; max-width: 650px; line-height: 1.7; }
    .st-key-home-inquiry { max-width: 100%; }
    .st-key-home-inquiry button { max-width: 100%; height: auto; }
    .st-key-home-inquiry button p { white-space: normal; overflow-wrap: break-word; line-height: 1.5; }
    @media(max-width: 640px) {
        .home-intro { padding-top: 12px; }
        .home-brand { flex-direction: column; gap: .2rem; letter-spacing: .08em; }
        .home-brand .home-brand-divider { display: none; }
        .st-key-home .home-intro h1 {
            font-size: clamp(2rem, 8.5vw, 3rem); line-height: 1.15;
            letter-spacing: -.035em; margin: 18px 0;
            overflow-wrap: normal; word-break: normal;
        }
        .st-key-home-actions { flex-direction: column; align-items: stretch; }
        .st-key-home-actions .stButton, .st-key-home-actions button { width: 100%; }
        .home-card { min-height: auto; }
        .home-section { padding-top: 30px; }
        .st-key-home-closing { padding: 24px; }
        .st-key-home-inquiry, .st-key-home-inquiry button { width: 100%; }
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container(key="home"):
        left, right = st.columns([1.25, 1], gap="large", vertical_alignment="center")
        with left:
            st.markdown("""
            <div class="home-intro">
                <div class="home-eyebrow home-brand"><span>Rashid Ali</span><span class="home-brand-divider" aria-hidden="true">/</span><span class="studio-name">NEXT GEN Graphics Studio</span></div>
                <h1>Creative vision.<br><span>Memorable visuals.</span></h1>
                <p>I bring ideas to life through AI photography, video and creative direction.
                Thoughtfully crafted for brands, products and the stories they tell.</p>
            </div>
            """, unsafe_allow_html=True)
            with st.container(horizontal=True, key="home-actions"):
                st.button("Explore my work", key="home-work", on_click=navigate, args=("Portfolio",))
                st.button("Start a project", key="home-contact", on_click=navigate, args=("Contact",))
            st.caption("Available for freelance projects")
        with right:
            portrait = assets / "me.png"
            with st.container(key="home-portrait"):
                if portrait.is_file():
                    st.image(str(portrait), caption="Rashid Ali soomro", width="stretch")

        st.markdown('<div class="home-note"><span>AI photography</span><span>Short-form video</span><span>Creative direction</span><span>Post-production</span></div>', unsafe_allow_html=True)

        st.markdown("""<div class="home-section"><div class="home-eyebrow">01 / Selected work</div>
        <h2>A glimpse of the possibilities.</h2><p>Visual concepts from my collection, from bold campaign imagery to brand storytelling.</p></div>""", unsafe_allow_html=True)
        featured = [
            ("attention.png", "Attention, by design", "Campaign visual / AI & graphic design"),
            ("design changes what people see.png", "A different perspective", "Brand storytelling / Visual concept"),
        ]
        columns = st.columns(2, gap="large")
        for column, (filename, title, caption) in zip(columns, featured):
            with column:
                if (assets / filename).is_file():
                    st.image(str(assets / filename), width="stretch", caption=title)
                    st.caption(caption)
        st.button("View the full portfolio", key="home-full-portfolio", on_click=navigate, args=("Portfolio",))

        st.markdown("""<div class="home-section"><div class="home-eyebrow">02 / What I create</div>
        <h2>One idea. Many ways to stand out.</h2></div>""", unsafe_allow_html=True)
        services = [
            ("01", "AI imagery", "Product scenes, editorial portraits and campaign visuals with a clear creative point of view."),
            ("02", "AI video", "Short-form stories, image-to-video sequences and motion concepts for social and digital campaigns."),
            ("03", "Creative direction", "From the first moodboard to the final edit: concepts, visual consistency and polished delivery."),
        ]
        for column, (number, title, description) in zip(st.columns(3, gap="medium"), services):
            with column:
                st.markdown(f'<div class="home-card"><span class="number">{number} /</span><h3>{title}</h3><p>{description}</p></div>', unsafe_allow_html=True)

        with st.container(key="home-closing"):
            st.markdown("""<div class="home-closing"><div class="home-eyebrow">From brief to final frame</div>
            <h2>Have something in mind?</h2><p>Share the idea, the audience and what you want to create.
            Let’s give your next project a visual direction.</p></div>""", unsafe_allow_html=True)
            st.button("Prepare a project inquiry", key="home-inquiry", on_click=navigate, args=("Contact",))
