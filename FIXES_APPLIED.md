# Fixes Applied

## Project review — September 21, 2026

- Corrected gallery titles for the updated `me.png` portrait and `me12.png` double exposure.
- Restored submitted contact fields when returning to Contact, keeping the form consistent with its prepared draft.
- Added stable contact widget keys and regression coverage for draft restoration, Home inquiry navigation, and gallery filters.
- Removed unused placeholder project data and made the footer year automatic.
- All six regression tests pass; all 11 local image files pass Pillow integrity verification.
- Browser/mobile visual checks and video playback verification remain outstanding. No changes were pushed during this review.

## Contact and collection details

- Added Rashidhussain473888@gmail.com to Contact, the sidebar, and the footer.
- Validated inquiries now open a prefilled email draft, with a text download fallback. Visitors send through their own email app.
- Added descriptive titles for existing artwork and identifiable video filenames without adding client results or social profiles.
- All five existing regression tests pass.

- Corrected Home/Portfolio `elif` structure.
- Corrected Portfolio loop indentation.
- Corrected Contact form `else` indentation.
- Kept the Home CTA inside the Home branch.
- Ran Python AST syntax validation successfully.

## Project review — September 19, 2026

- Added missing `requirements.txt`, a matching light theme, and ignore rules for local environments and secrets.
- Uploads now require an explicit save action and preserve existing files when names collide.
- Added portable filename handling, extension/empty-file checks, and per-file save error messages.
- The contact form validates required fields and email format, then offers a downloadable inquiry draft. It does not claim to send email.
- Updated README and deployment instructions to match the actual asset folder and upload behavior.
- Replaced the deprecated image sizing argument with `width="stretch"`.
- Verified all six pages and inquiry behavior with Streamlit AppTest; five regression tests cover app and storage behavior.

## Gallery presentation update

- Added lift and shadow hover effects to Home cards, with reduced-motion support.
- Replaced the Portfolio upload interface with a gallery of existing pictures and videos.
- Added All work / Images / Videos filters, image columns preserving original proportions, framed video players, and clean numbered captions.
- Removed upload and deployment instructions from the public page. Add new assets directly to `portfolio_uploads/`.
- Existing five regression tests pass after the update.

## Home redesign with UI UX Pro Max

- Applied the skill's portfolio-first structure and Archivo / Space Grotesk typography, retaining a green accent.
- Added a split hero with an existing portrait study and working Portfolio / Contact navigation buttons.
- Replaced placeholder project cards on Home with actual artwork from the collection.
- Kept three service cards with hover lift and reduced-motion support.
- Added a project inquiry call to action, mobile stacking, and higher-contrast Home text and buttons.
- All five regression tests and all four Home navigation button checks pass. Browser visual verification remains unavailable in this session.

## Portfolio-wide design refinement

- Unified typography, green accents, card spacing, buttons, and form styling in `styles.css`.
- Preserved existing copy and media, with larger two-column image previews and row-by-row gallery ordering.
- Added narrow-gallery stacking, responsive page padding, automatic mobile sidebar behavior, visible keyboard focus, and reduced-motion styling.
- Kept images at their original proportions and video players bounded without cropping.
- Verified all six pages with the existing regression suite. Browser visual checks remain unavailable; mobile styling is implemented but not visually verified.
