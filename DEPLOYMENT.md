# Deployment Checklist

## Streamlit Community Cloud
1. Create a GitHub repository.
2. Upload the portfolio files, including `requirements.txt`, `.streamlit/config.toml`, and your curated `portfolio_uploads/` assets. Exclude `.venv/` and secrets.
3. Open Streamlit Community Cloud.
4. Select the repository and `app.py`.
5. Deploy.
6. Add secrets only if your final contact form/API integration needs them.

## Production checklist
- [ ] Replace placeholder content
- [ ] Compress portfolio images
- [ ] Test mobile layout
- [ ] Test all navigation items
- [ ] Test contact form
- [ ] Test the prefilled email link and download fallback; sending happens in the visitor's email app
- [ ] Include the curated `portfolio_uploads/` folder when deploying
- [ ] Add favicon/logo
- [ ] Add social/profile links
- [ ] Add privacy notice if collecting visitor data
- [ ] Verify commercial usage rights for all showcased work
- [ ] Add analytics only after deciding what visitor data you actually need
