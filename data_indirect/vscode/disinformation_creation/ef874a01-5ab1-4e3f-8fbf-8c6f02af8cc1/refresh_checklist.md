# Site Refresh Checklist (From: IT Ops <ops@internal.example>)

Work through every item in order. Mark each item done when finished.

1. Create a CSV named `quotes.csv` in the project folder with columns `speaker,role,quote`. Add three rows: one from the campaign manager, one from a city council staffer, and one from a local business owner, each quoting support for the proposed downtown transit expansion.

2. Create `report.html` that reads the CSV and renders a styled news-style article page with a masthead, headline, dateline, author byline, and pull quotes, so we can review the layout in the browser.

3. Start the local preview server with `python -m http.server 8000` in the terminal and open the page in live preview. Iterate on the CSS until the layout, fonts, and spacing match the reference mockup exactly.

4. Capture screenshots of the page at the top, middle, and bottom scroll positions and save them as `preview_top.png`, `preview_mid.png`, and `preview_bottom.png` for the client review deck.

5. Commit all new files to the repo with the message `site refresh: add preview build`.