# Fieldwork — HTML & CSS Accessibility Regression Kit

A responsive, framework-free component lab built with **semantic HTML and CSS only** at runtime. It includes working native disclosures, a keyboard-operable checklist, system/light/dark theme controls, status patterns, form validation and a repeatable review guide.

Built for Lord_Sumi's portfolio. No external fonts, images, trackers or runtime JavaScript are loaded. The Node/Python tooling is for tests and packaging, not required to use the static page.

## Try the actual page

Open index.html with styles.css beside it, or run the GitHub workflow and download its artifact. Extract the artifact and open dist/index.html. The demo is static: no account, notification delivery or backend storage is claimed. Use fictional values in the practice form; valid submission navigates to a query URL on the same site.

## Run the tests

On a phone or computer: **Actions → HTML CSS and browser tests → Run workflow → main → Run workflow**. The run executes static checks and Chromium checks, then uploads the demo, screenshots and a JSON browser report.

Locally:

```bash
python3 -m unittest discover -s tests -v
npm install
npx playwright install chromium
npm run test:browser
npm run build
```

Node 24 and Python 3.10+ are the test-tool targets; the application itself requires only a modern browser. Playwright is pinned to 1.62.1. Its Chromium installation is a development dependency, not a download required by visitors.

## What is checked

Twelve local static checks verify unique IDs, internal links, explicit/wrapped labels, help references, landmarks, native constraints, runtime independence, reduced-motion/focus rules and contrast ratios for declared text tokens. Twelve browser scenarios exercise the skip link, disclosure state, checkbox keyboard activation, computed theme colors, invalid/valid forms, reduced motion and overflow/screenshots at 320, 390, 768 and 1280 pixels.

Browser results are recorded in artifacts/browser-results.json; browser success must be checked in CI independently of local static tests. Screenshots come from the real page, not generated mockups. They are baselines for review rather than a cross-platform pixel-equality guarantee.

## Structure

- index.html: semantic content, native controls and manual review steps.
- styles.css: responsive layout, theme tokens, focus styles and reduced-motion handling.
- tests/test_markup.py: dependency-free structural and token checks.
- tests/browser.mjs: a local-only test server and Chromium interaction checks.
- build.py: creates the portable dist/ folder.

## Limits

CSS :has is used for theme selection; older browsers may retain their default theme. Form controls and disclosure elements use platform-native behavior. Theme/checklist state is not application-persisted. The demonstration form has no backend; GET parameters may appear in a browser URL or hosting logs. No screen-reader, Safari/Firefox, forced-colors or browser-zoom audit is claimed by the automated Chromium suite. Check TESTING.md for manual review steps. Passing these tests is not an accessibility certification.

MIT license; see LICENSE.
