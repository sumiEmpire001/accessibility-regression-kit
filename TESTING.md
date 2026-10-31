# Testing this HTML & CSS project

On GitHub: Actions → HTML CSS and browser tests → Run workflow → main → Run workflow. Open the resulting run and read the markup tests and browser checks. Download the artifact to inspect real screenshots at 320, 390, 768 and 1280 pixels.

Extract the artifact and open `dist/index.html` to try the static page. Keep styles.css beside it. Color controls, disclosures, checkboxes and native form validation need no JavaScript or backend.

Local static checks: `python3 -m unittest discover -s tests -v`. Browser checks: `npm install`, `npx playwright install chromium`, then `npm run test:browser`. Build: `npm run build`.

Manual checks still required: screen-reader announcements, high-contrast/forced-color modes, browser zoom and your intended browser/device. Automated tests cover a defined subset, not an accessibility certification. Use synthetic form data; no application backend or storage is provided.
