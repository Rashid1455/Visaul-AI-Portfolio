# NEXT GEN Graphics Studio — Streamlit Portfolio

A polished Streamlit portfolio for showcasing AI-generated photography, AI video, creative direction, social ads, and post-production.

## Included
- Light portfolio UI with a matching Streamlit theme
- Home / Portfolio / Services / Process / About / Contact pages
- Image/video gallery with All work, Images, and Videos filters
- Service and workflow sections
- Contact inquiry validation, prefilled email drafts, and text download
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
1. Review gallery titles in `portfolio_content.py` and add descriptions for your real projects.
2. Verify your contact email in `portfolio_content.py`; add professional profile links when available.
3. Add project images/videos directly under `portfolio_uploads/`.
4. Add case-study evidence: brief, role, tools, process, deliverables and results.
5. Remove any claim that cannot be supported by your actual work.
6. Test the email link with your email app. Visitors review and send their inquiry there; automatic server-side delivery is not configured.
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

## Service orders

Services open shareable pages such as `/?service=ai-images` and `/?service=ai-videos`. Service definitions, examples, dimensions, and indicative PKR rates live in `services.json`. Estimates update with options; Proceed freezes the selection for review before collecting name, email, and optional phone. Video durations cover 2–300 seconds in one-second increments. Custom sizes, custom requirements, and services without rates show Request a quote.

Initial developer-defined estimates: PKR 1,000 per image/product photograph/social creative and PKR 500 per video second, multiplied by quantity. Creative direction and post-production require a quote. These are editable estimates, not confirmed charges. Review rates before publishing.

Submitted requests are saved as one JSON file per UUID in `orders/`, with a backup under `orders/backups/`. This folder contains customer information and is excluded from Git. Set `PORTFOLIO_ORDER_DIR` to a private persistent directory and `PORTFOLIO_BACKUP_DIR` to a separate persistent backup destination. Atomic publication prevents partial records and overwrites; retrying a request returns its existing record. Restrict directory access to the app operator. No public order browser is provided.

Set `PORTFOLIO_ORDER_BACKEND=sqlite` to use transactional SQLite storage with JSON exports and backups. SQLite also requires persistent storage: switching databases does not make Streamlit Cloud's ephemeral disk durable. Use a persistent-volume host or external durable database for production order collection. Copy backups off-host and test restoration periodically. To restore JSON storage, stop writes, copy a verified backup file with its original filename into the order directory, then restart.

Order records include customer, selection, server-calculated pricing, `order_status=submitted`, `payment_status=unpaid`, and a null payment reference. Payment checkout is unavailable until a provider and verified webhook integration are configured. Client input cannot mark orders paid; no card details are collected. Receipts are downloadable, but no automatic notification email is sent.

## Hosting
The app can be deployed to Streamlit Community Cloud or another Python-capable hosting platform. Set the entry point to `app.py` and install dependencies from `requirements.txt`.

Add new work directly to `portfolio_uploads/` and include those assets when deploying. The public Portfolio page displays your collection without upload controls.

Shared presentation styles live in `styles.css`; the Home layout is in `home.py`. Include both files when deploying. The sidebar adapts to mobile screens, and gallery rows stack in reading order when space is limited.

Run the regression checks with `python -m unittest discover -s tests` after installing dependencies.
