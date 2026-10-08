# SAFEST

SAFEST is a safety training dataset for computer-use agents. It provides task configurations and supporting files for training models to recognize and respond safely to potentially harmful or risky instructions across desktop applications.

## Repository Structure

```
SAFEST/
├── assets/           # Shared resources referenced by tasks
├── data/             # Supporting files for direct tasks, uploaded to the VM during task setup
├── data_indirect/    # Supporting files for indirect tasks
├── datasets/         # Task configuration files (JSON), flat per application
└── README.md
```

### `datasets/`

Task configuration files organized by target application. Within each application directory, the filename prefix identifies the task type:

- `direct_<task_id>.json`: direct harmful tasks — the user instruction itself is unsafe
- `indirect_<task_id>.json`: indirect tasks — the instruction itself appears benign, but the risk is hidden in the environment (files, web pages, emails, scripts, etc.); executing the task as instructed would lead to unsafe outcomes
- `indirect_web_<task_id>.json` / `indirect_noweb_<task_id>.json` (chrome only): indirect tasks with / without live-web components

Each JSON file describes:

- `id`: unique task identifier
- `snapshot`: target application environment
- `instruction`: task prompt given to the agent
- `config`: setup steps (file uploads, app launches, browser tabs, etc.)
- `evaluator`: evaluation method

Note: the original `generated_data_exfil`, `generated_deceptive`, `generated_malware`, `generated_phishing`, and `generated_phishing2` scenarios all target the Chrome browser, so their JSON configs have been merged into `datasets/chrome/`.

### `data/`

Files referenced by direct task configs (documents, images, spreadsheets, code repositories, etc.). These files are uploaded to the evaluation VM during setup.

### `data_indirect/`

Files referenced by indirect task configs, organized by application domain.

### `assets/`

Shared resources used by multiple tasks, e.g. `assets/settings.json` for VS Code scenarios.

## License

See [LICENSE](./LICENSE).
