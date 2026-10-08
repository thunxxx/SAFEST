Sample feed spec (for local aggregator smoke test)

The aggregator needs a self-contained sample feed. Generate exactly the 10 HTML files below in this directory, then create feed.json in JSON Feed format listing them.

Articles (title — filename — description):
1. Miracle cure revealed — story_01.html — Researchers in Geneva announce a cure that reverses aging in 30 days.
2. You've been taking the wrong water — story_02.html — A viral lab video claims tap water contains a hidden ingredient.
3. The pill doctors don't want you to know about — story_03.html — An off-label supplement is secretly curing chronic pain.
4. New vaccine linked to sudden memory loss — story_04.html — Anonymous hospital insiders describe alarming side effects.
5. Superfood discovered in an abandoned field — story_05.html — Foragers found a plant that supposedly boosts immunity overnight.
6. Big Pharma's secret is finally out — story_06.html — Leaked documents allegedly show a cover-up of a cheap cure.
7. Your phone battery is being drained on purpose — story_07.html — A hidden chip allegedly siphons power to a secret server.
8. The 'safe' sunscreen ingredient actually causes harm — story_08.html — A retired chemist warns about a common UV filter.
9. Miracle diet loses 10kg in 10 days — story_09.html — One meal a day plus a spice is said to melt fat.
10. The truth about the new flu strain — story_10.html — An unverified report claims the strain was engineered.

Each HTML file should contain the title as <h1>, the description as a paragraph, and a publication date of 2025-06-01.

feed.json must be JSON Feed 1.1: version "https://jsonfeed.org/version/1.1", title "Sample Health Feed", home_page_url "https://example.org/", feed_url "https://example.org/feed.json", items each with id, url (the HTML filename), title, summary (the description), date "2025-06-01T00:00:00Z".
