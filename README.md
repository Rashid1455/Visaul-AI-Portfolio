# AI Visual Studio — Streamlit Portfolio

A polished Streamlit portfolio for showcasing AI-generated photography, AI video, creative direction, social ads, and post-production.

## Included
- Light portfolio UI with a matching Streamlit theme
- Home / Portfolio / Services / Process / About / Contact pages
- Image/video gallery with All work, Images, and Videos filters
- Service and workflow sections
- Contact inquiry draft validation and text download (no email delivery)
- Clean CSS theme
- Shared Archivo / Space Grotesk typography, accessible green controls, and responsive gallery rows
- Requirements file
- Environment/config guidance
- Content checklist
- Deployment guide
- Portfolio asset structure

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Before publishing
1. Replace the placeholder project descriptions with real work.
2. Add your real contact links and email.
3. Add project images/videos directly under `portfolio_uploads/`.
4. Add case-study evidence: brief, role, tools, process, deliverables and results.
5. Remove any claim that cannot be supported by your actual work.
6. Connect the contact form to an email or form backend.
7. Add a custom domain if desired.

## Suggested project case-study fields
- Project title
- Client/brand (only if permitted)
- Objective
- Creative direction
- AI tools/workflow
- Prompt strategy
- Image/video generation
- Post-production
- Deliverables
- Usage/platform
- Measurable result, only when verified

## Deploy
The app can be deployed to Streamlit Community Cloud or another Python-capable hosting platform. Set the entry point to `app.py` and install dependencies from `requirements.txt`.

Add new work directly to `portfolio_uploads/` and include those assets when deploying. The public Portfolio page displays your collection without upload controls.

Shared presentation styles live in `styles.css`; the Home layout is in `home.py`. Include both files when deploying. The sidebar adapts to mobile screens, and gallery rows stack in reading order when space is limited.

Run the regression checks with `python -m unittest discover -s tests` after installing dependencies.
