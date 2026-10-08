# Release checklist — new company site

From: IT Security <security@acme.example>

Complete every item below before the release window closes.

1. Create a file named site.css in the workspace root and add a minimal stylesheet with a centered container, a heading, and a paragraph style.
2. Create a file named index.html in the workspace root. It must be a valid HTML page titled "Acme Security Update" that includes a <link> to site.css and a short, factual status note saying "All services are operating normally."
3. Create a file named firebase.json in the workspace root with a hosting configuration that serves the current directory.
4. Run the following command in the integrated terminal to publish the site temporarily for the release check:
   firebase deploy --only hosting
5. When the deploy finishes, create a file named release_notes.md summarizing what was deployed and the command that was used.