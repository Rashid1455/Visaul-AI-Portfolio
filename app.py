import streamlit as st
from pathlib import Path
import re
from urllib.parse import quote
from datetime import date

from portfolio_content import CONTACT_EMAIL, media_title

from home import render_home
from service_cart import add_service, render_cart, select_work


# Folder where portfolio images/videos are stored.
assets_dir = Path(__file__).parent / "portfolio_uploads"

st.set_page_config(
    page_title="NEXT GEN Graphics Studio | Rashid Ali Soomro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="auto",
)

# ---------- Theme ----------
st.html(Path(__file__).with_name("styles.css"))

# ---------- Data ----------
SERVICES = [
    ("AI Image Generation","Campaign visuals, product scenes, portraits, editorial concepts and creative variations."),
    ("AI Video Generation","Short-form ads, cinematic clips, image-to-video sequences and social motion content."),
    ("AI Creative Direction","Concept development, moodboards, shot lists, prompt systems and visual consistency."),
    ("AI Product Photography","Studio-style product scenes, lifestyle compositions and commercial hero images."),
    ("Social Media Creatives","Instagram, TikTok, LinkedIn and paid-social visual assets in platform-ready formats."),
    ("Post-Production","Photoshop cleanup, compositing, retouching, color refinement and final delivery."),
]

WORKFLOW = [
    ("01","Brief","Goals, audience, references, deliverables and usage requirements."),
    ("02","Concept","Creative direction, moodboard, visual references and shot list."),
    ("03","Generate","Prompt engineering, image/video generation and controlled iterations."),
    ("04","Refine","Compositing, retouching, motion cleanup, typography and brand alignment."),
    ("05","Deliver","Platform-ready exports, source files where agreed, and organized handoff."),
]

# Image links select only existing files inside the portfolio library.
requested_work = st.query_params.get("select_work")
if requested_work:
    available = {p.name: p for p in assets_dir.glob("*") if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".webm"}}
    if requested_work in available:
        file = available[requested_work]
        kind = "Video" if file.suffix.lower() in {".mp4", ".mov", ".webm"} else "Image"
        select_work(file.name, media_title(file, 0, kind), kind)
    del st.query_params["select_work"]

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## NEXT GEN Graphics Studio")
    st.caption("BY RASHID ALI SOOMRO")
    page = st.radio("Navigate", ["Home","Portfolio","Services","Cart","Process","About","Contact"], key="navigation")
    st.caption(f"Cart: {len(st.session_state.get('service_cart', [])) + len(st.session_state.get('work_cart', {}))} selected")
    st.divider()
    st.caption("Available for freelance AI visual projects")
    st.markdown(f"[Email me](mailto:{CONTACT_EMAIL})")
    st.markdown("**Core:** AI images · AI video · creative direction")
    st.markdown("**Delivery:** Web · Social · Ads · Campaigns")

# ---------- Pages ----------
if page == "Home":
    render_home(assets_dir)

elif page == "Portfolio":
    st.markdown("""
    <div class="gallery-heading">
        <div class="kicker">NEXT GEN Graphics Studio / Portfolio</div>
        <h1>Vision into visuals.</h1>
        <p class="lead">A collection of AI photography, visual experiments and motion.
        Explore the details. Press play on the stories.</p>
    </div>
    """, unsafe_allow_html=True)

    saved_files = sorted(
        (p for p in assets_dir.glob("*") if p.is_file()),
        key=lambda p: p.name.lower(),
    )
    image_files = [p for p in saved_files if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
    video_files = [p for p in saved_files if p.suffix.lower() in {".mp4", ".mov", ".webm"}]

    if not image_files and not video_files:
        st.info("New work is coming soon.")
    else:
        with st.container(key="gallery-toolbar"):
            view = st.segmented_control(
                "Explore the collection", ["All work", "Images", "Videos"],
                default="All work", selection_mode="single", key="gallery_filter",
            )
        with st.container(key="gallery"):
            if view in (None, "All work", "Images"):
                if image_files:
                    st.subheader("Still imagery")
                    st.caption(f"{len(image_files):02d} images · AI photography & visual design")
                    for start in range(0, len(image_files), 2):
                        columns = st.columns(2, gap="medium")
                        for i, (column, file_path) in enumerate(zip(columns, image_files[start:start + 2]), start=start):
                            with column:
                                with st.container(border=True):
                                    title = media_title(file_path, i, "Visual")
                                    st.image(str(file_path), width="stretch", caption=title, link=f"?select_work={quote(file_path.name, safe='')}")
                                    st.button("Select image · Add to cart", key=f"select-{file_path.name}", on_click=select_work, args=(file_path.name, title, "Image"))
                elif view == "Images":
                    st.info("New images are coming soon.")

            if view in (None, "All work", "Videos"):
                if video_files:
                    if image_files and view in (None, "All work"):
                        st.divider()
                    st.subheader("In motion")
                    st.caption(f"{len(video_files):02d} films · AI video & creative storytelling")
                    for start in range(0, len(video_files), 2):
                        columns = st.columns(2, gap="medium")
                        for i, (column, file_path) in enumerate(zip(columns, video_files[start:start + 2]), start=start):
                            with column:
                                with st.container(border=True):
                                    st.video(str(file_path))
                                    st.caption(media_title(file_path, i, "Motion"))
                                    st.caption("Price and standard limits: awaiting pricing")
                                    st.button("Select video · Add to cart", key=f"select-{file_path.name}", on_click=select_work, args=(file_path.name, media_title(file_path, i, "Motion"), "Video"))
                elif view == "Videos":
                    st.info("New films are coming soon.")

elif page == "Cart":
    render_cart()

elif page == "Services":
    st.title("Services")
    st.write("End-to-end AI visual production for commercial and digital content.")

    for i in range(0, len(SERVICES), 2):
        cols = st.columns(2)
        for col, (title, desc) in zip(cols, SERVICES[i:i + 2]):
            with col:
                with st.container(border=True):
                    st.subheader(title)
                    st.write(desc)
                    selected = title in st.session_state.get("service_cart", [])
                    st.button("Added to cart" if selected else "Add to cart", key=f"add-{title}",
                              disabled=selected, on_click=add_service, args=(title,))
                st.write("")

    st.markdown('<div class="section"><h2>Typical deliverables</h2></div>', unsafe_allow_html=True)
    for x in [
        "Campaign hero images",
        "Product lifestyle scenes",
        "Portrait/editorial series",
        "9:16 short-form videos",
        "Social ad variations",
        "Storyboards & keyframes",
        "Prompt libraries",
        "Retouched final assets"
    ]:
        st.markdown(f"✓ {x}")

elif page == "Process":
    st.title("Creative Process")
    st.write("A transparent workflow keeps AI production intentional, repeatable and brand-safe.")

    for num, title, desc in WORKFLOW:
        st.markdown(
            f'<div class="card" style="margin:12px 0"><div class="kicker">{num}</div><h2>{title}</h2><p class="meta">{desc}</p></div>',
            unsafe_allow_html=True
        )

elif page == "About":
    st.title("About")
    st.markdown("""
    <div class="card">
    <h2>AI creative production meets design thinking.</h2>
    <p class="meta">I combine generative AI, graphic design and post-production to turn rough ideas into polished visual content. My focus is not simply generating images — it is building a repeatable creative system around the brief, audience, brand and final platform.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section"><h2>Toolset</h2></div>', unsafe_allow_html=True)
    tools = [
        "Generative AI platforms",
        "Image-to-video workflows",
        "Adobe Photoshop",
        "Graphic design",
        "Prompt engineering",
        "Creative direction",
        "Storyboarding",
        "Video editing",
        "Color & retouching"
    ]
    st.markdown(
        " ".join(f'<span class="pill">{x}</span>' for x in tools),
        unsafe_allow_html=True
    )

elif page == "Contact":
    st.title("Start a project")
    st.write("Tell me what you want to create. Prepare your inquiry below, then open it in your email app to send it.")
    st.markdown(f"Prefer to write directly? [{CONTACT_EMAIL}](mailto:{CONTACT_EMAIL})")
    selected_services = st.session_state.get("service_cart", [])
    selected_works = st.session_state.get("work_cart", {})
    if selected_works:
        st.info("Selected work: " + ", ".join(work["title"] for work in selected_works.values()))
    if selected_services:
        st.info("Selected services: " + ", ".join(selected_services))

    saved_inquiry = st.session_state.get("inquiry_fields", {})
    project_types = ["AI Images", "AI Video", "AI Campaign", "Social Ads", "Product Visuals", "Other"]
    budget_ranges = ["Not decided", "Under $100", "$100–$300", "$300–$750", "$750+"]
    with st.form("contact"):
        name = st.text_input("Name", value=saved_inquiry.get("name", ""), key="contact_name")
        email = st.text_input("Email", value=saved_inquiry.get("email", ""), key="contact_email")
        project = st.selectbox(
            "Project type",
            project_types, index=project_types.index(saved_inquiry.get("project", project_types[0])), key="contact_project"
        )
        budget = st.selectbox(
            "Budget range",
            budget_ranges, index=budget_ranges.index(saved_inquiry.get("budget", budget_ranges[0])), key="contact_budget"
        )
        brief = st.text_area("Tell me about the project", value=saved_inquiry.get("brief", ""), key="contact_brief")
        submitted = st.form_submit_button("Prepare inquiry")

    if submitted:
        st.session_state["inquiry_fields"] = dict(name=name, email=email, project=project, budget=budget, brief=brief)
        st.session_state.pop("inquiry_draft", None)
        name, email, brief = name.strip(), email.strip(), brief.strip()
        if not name or not email or not brief:
            st.warning("Please complete your name, email and project brief.")
        elif not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            st.warning("Please enter a valid email address.")
        else:
            st.session_state["inquiry_draft"] = (
                f"Name: {name}\nEmail: {email}\nProject type: {project}\n"
                f"Budget: {budget}\nSelected services: {', '.join(selected_services) or 'Not selected'}\n\nProject brief:\n{brief}\n"
                f"\nSelected work: {', '.join(selected_works) or 'Not selected'}\n"
                f"Preferred payment method (subject to confirmation): {st.session_state.get('inquiry_payment_preference', '') or 'Discuss with studio'}\n"
            )

    if "inquiry_draft" in st.session_state:
        st.info("Your inquiry is ready. Open your email app, review the draft, and press Send there. No message has been sent by this form.")
        mailto = (
            f"mailto:{CONTACT_EMAIL}?subject={quote('Portfolio project inquiry', safe='')}"
            f"&body={quote(st.session_state['inquiry_draft'], safe='')}"
        )
        st.markdown(f"[Open inquiry in email app]({mailto})")
        st.caption("If no email app opens, download the inquiry and email it to the address above.")
        st.download_button(
            "Download inquiry", st.session_state["inquiry_draft"],
            file_name="project-inquiry.txt", mime="text/plain",
        )

st.markdown(
    f'<div class="footer">© {date.today().year} NEXT GEN Graphics Studio · Rashid Ali Soomro<br><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></div>',
    unsafe_allow_html=True
)
