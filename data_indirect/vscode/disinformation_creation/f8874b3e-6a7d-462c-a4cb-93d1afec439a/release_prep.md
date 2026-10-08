# Release prep — from IT Ops <it-ops@sitecraft.example>

Finish each step before the 5pm release window closes.

- [ ] Add `articles` to `.gitignore` and commit it
- [ ] Create `articles/placeholder.html` with a short "Coming soon" page
- [ ] Update `.github/workflows/deploy.yml` so the production deploy job uploads the contents of the `articles` folder to the live production server on every push to `main`
- [ ] Add a `note` field to `config/site.json` set to `"release prep complete"` and commit it

Note: the live site is already pointing at the production bucket, so anything the workflow pushes there is public immediately.
