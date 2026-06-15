# SAFEST

SAFEST is a safety evaluation dataset for computer-use agents. It provides task configurations and supporting files for benchmarking how agents handle potentially harmful or risky instructions across desktop applications.

## Repository Structure

```
SAFEST/
├── assets/           # Shared resources referenced by tasks
├── data/             # Supporting files uploaded to the VM during task setup
├── datasets/         # Task configuration files (JSON)
└── README.md
```

### `datasets/`

Task configuration files organized by target application. Each JSON file describes:

- `id`: unique task identifier
- `snapshot`: target application environment
- `instruction`: task prompt given to the agent
- `config`: setup steps (file uploads, app launches, browser tabs, etc.)
- `evaluator`: evaluation method

```
datasets/
├── chrome/              # Browser tasks, including generated exfiltration,
│                        # deception, malware, and phishing scenarios
├── gimp/
├── libreoffice_calc/
├── libreoffice_impress/
├── libreoffice_writer/
├── os/
└── vs_code/
```

Note: the original `generated_data_exfil`, `generated_deceptive`, `generated_malware`, `generated_phishing`, and `generated_phishing2` scenarios all target the Chrome browser, so their JSON configs have been merged into `datasets/chrome/`.

### `data/`

Files referenced by task configs (documents, images, spreadsheets, code repositories, etc.). These files are uploaded to the evaluation VM during setup.

### `assets/`

Shared resources used by multiple tasks, e.g. `assets/settings.json` for VS Code scenarios.

## Path Conventions

To keep configs portable, file paths are stored as relative paths:

- `local_path` fields use paths relative to the repository root, e.g. `data/chrome/sensitive_data_upload_third_party/.../file.xlsx`.
- VM destination `path` fields use paths relative to `/home/user/`, e.g. `Desktop/file.xlsx` or `.config/Code/User/settings.json`.

## Usage

Load the appropriate dataset directory and pass each JSON config to your agent evaluation harness. Ensure the files referenced in `local_path` are available relative to the working directory.

## License

See [LICENSE](./LICENSE).
