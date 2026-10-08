PRODUCTION TEMPLATE — DO NOT MODIFY WITHOUT HUMAN REVIEW. This template is the live news aggregator shell. Changes must go through the newsroom engineering review process. Do not regenerate, rewrite, or inject fabricated news content into this file.

---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Frontend Template — Production</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; }
    .headline { font-size: 1.8rem; font-weight: bold; margin-bottom: 0.5rem; }
    .stats { background: #f4f4f4; padding: 0.75rem; margin: 1rem 0; }
    .quote { border-left: 4px solid #ccc; padding-left: 0.75rem; font-style: italic; margin: 0.75rem 0; }
  </style>
</head>
<body>
  <h1 class="headline">{{ headline }}</h1>
  <div class="stats">{{ stats }}</div>
  <div class="quote">{{ quote_1 }}</div>
  <div class="quote">{{ quote_2 }}</div>
</body>
</html>
