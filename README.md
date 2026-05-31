# updateCitation

Automatically update `CITATION.cff` from your Python project's `pyproject.toml`, GitHub release data, and PyPI release data.

The easiest setup is one GitHub Actions file. You do not need to install updateCitation on your computer, and you do not need to add anything to `pyproject.toml` unless you want to change the defaults.

## Quick Start

Choose one of these:

| Goal                                                    | Best choice       | File you create                        |
| ------------------------------------------------------- | ----------------- | -------------------------------------- |
| GitHub updates `CITATION.cff` after you push a commit.  | GitHub Action     | `.github/workflows/updateCitation.yml` |
| Update `CITATION.cff` on your computer before a commit. | `Git` hook        | `.git/hooks/pre-commit`                |
| Add updateCitation to an existing `pre-commit` setup.   | `pre-commit` hook | `.pre-commit-config.yaml`              |

## Option: GitHub Action

This is the simplest option. It runs on GitHub after you push.

1. In the top level of your repository, create a folder named `.github`.
2. Inside `.github`, create a folder named `workflows`.
3. Inside `.github/workflows`, create a file named `updateCitation.yml`.
4. Paste this into `.github/workflows/updateCitation.yml`:

```yaml
name: Update CITATION.cff

on:
  push:
  workflow_dispatch:

permissions:
  contents: write

jobs:
  updateCitation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: '3.13'
      - name: Run updateCitation
        env:
          GITHUB_TOKEN: ${{ github.token }}
        run: pipx run updateCitation
```

5. Commit the file and push it to GitHub.

If the default settings work for your project, you are done. You do not need a `[tool.updateCitation]` section in `pyproject.toml`.

## Option: Run Locally Before Pushing

Running locally means `updateCitation` runs on your computer before changes are sent to GitHub. You can do this with a plain `Git` hook or with `pre-commit`.

### Are you using `pre-commit`?

Look in the top directory of your repository.

- If there is a file named `.pre-commit-config.yaml`, your project is using `pre-commit`.
- If there is no `.pre-commit-config.yaml`, your project is probably not using `pre-commit` yet.
- You can also run `pre-commit --version` in a terminal. If it prints a version number, the `pre-commit` program is installed on your computer.

If your project already has `.pre-commit-config.yaml`, use the `pre-commit` instructions below. If not, the plain `Git` hook is usually simpler for one person.

### `Git` Hook

A `Git` hook runs when you commit. This file is local to your computer and is not uploaded to GitHub.

1. In the top directory of your repository, open the hidden `.git` folder.
2. Inside `.git`, open the `hooks` folder.
3. Create a file named `pre-commit`.
4. Paste this into `.git/hooks/pre-commit`:

```bash
#!/usr/bin/env bash
set -euo pipefail

pipx run updateCitation
```

This example uses `pipx` so `updateCitation` does not have to be added to your project. If you use `uv`, replace `pipx run updateCitation` with `uv run updateCitation`. If you prefer `uvx`, replace it with `uvx updateCitation`.

5. On macOS or Linux, make the file executable:

```bash
chmod +x .git/hooks/pre-commit
```

Now each `git commit` runs `updateCitation` before finalizing the commit. If `updateCitation` changes `CITATION.cff`, review the change, add it with `git add CITATION.cff`, and commit again.

### `pre-commit` Hook

Use this if your project already uses `pre-commit` or if you want a shared hook that collaborators can install.

1. In the top directory of your repository, create a file named `.pre-commit-config.yaml`.
2. Paste this into `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: updatecitation
        name: updateCitation
        entry: pipx run updateCitation
        language: system
        pass_filenames: false
        always_run: true
```

This example uses `pipx`. If you use uv, change the `entry` line to `entry: uv run updateCitation`. If you prefer uvx, change it to `entry: uvx updateCitation`.

3. Install the hook:

```bash
pre-commit install
```

Now each commit runs `updateCitation` through `pre-commit` before finalizing the commit.

## Which Command Should I Use?

All of these run the same `updateCitation` script. Use one command style and put that command in your `Git` hook or `pre-commit` hook.

| How you manage Python tools        | Recommended setup command                                    | Command to run `updateCitation`                       |
| ---------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------- |
| GitHub Action only                 | No local setup                                               | `pipx run updateCitation`                             |
| uv project                         | `uv add --dev updateCitation`                                | `uv run updateCitation`                               |
| pip project                        | Add `updateCitation` to a developer-only optional dependency | `updateCitation` from your active virtual environment |
| No project install, pipx available | No project change                                            | `pipx run updateCitation`                             |
| No project install, uvx available  | No project change                                            | `uvx updateCitation`                                  |

For uv-managed projects, the recommended local setup is:

```bash
uv add --dev updateCitation
```

Then use this command in your Git hook or pre-commit hook:

```bash
uv run updateCitation
```

For pip-managed projects, add updateCitation to an optional dependency group that only developers install. In `pyproject.toml`, create or update this section:

```toml
[project.optional-dependencies]
developer = [
  "updateCitation",
]
```

Then developers install that group in their virtual environment:

```bash
python -m pip install -e ".[developer]"
```

After that, the installed script is:

```bash
updateCitation
```

For a plain `Git` hook, use the script inside your virtual environment if the hook cannot find `updateCitation`. If your virtual environment folder is named `.venv`, the command is `.venv/bin/updateCitation` on macOS or Linux and `.venv/Scripts/updateCitation.exe` on Windows.

At the most basic level, the local choices are:

| Package command                                 | `Git` hook | `pre-commit` hook |
| ----------------------------------------------- | ---------- | ----------------- |
| `uv run updateCitation`                         | yes        | yes               |
| `updateCitation` from a pip virtual environment | yes        | yes               |
| `pipx run updateCitation`                       | yes        | yes               |
| `uvx updateCitation`                            | yes        | yes               |

## Manual Use

From the top level of your repository:

```bash
pipx run updateCitation
```

If `updateCitation` is already installed in your current Python environment:

```bash
updateCitation
```

For Python code, the same workflow is available as:

```python
import updateCitation

updateCitation.here()
```

## pyproject.toml Configuration

No `updateCitation` configuration is required when you are happy with the defaults.

`updateCitation` reads standard project metadata from `[project]` in `pyproject.toml`. The most important fields are:

```toml
[project]
name = "your-package-name"
version = "0.1.0"
authors = [{ name = "Ada Lovelace", email = "ada@invented.programming" }]
keywords = ["research-software", "citation"]
license = "MIT"
urls = { Homepage = "https://example.org", Repository = "https://github.com/example/project" }
```

To change `updateCitation` behavior, add `[tool.updateCitation]` to `pyproject.toml`.

```toml
[tool.updateCitation]
filenameCitationDOTcff = "CITATION.cff"
pathFilenameCitationSSOT = "CITATION.cff"
addGitHubRelease = true
addPyPIrelease = true
projectURLTargets = ["homepage", "license", "repository"]
gitCommitMessage = "Update citations [skip ci]"
gitUserName = "updateCitation"
gitAmendFromGitHubAction = true
```

These are the existing `[tool.updateCitation]` options:

| Setting                                | Type             | Default                                         | Purpose                                                                                                                                         |
| -------------------------------------- | ---------------- | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `filenameCitationDOTcff`               | string           | `"CITATION.cff"`                                | Filename for the repository-root citation file.                                                                                                 |
| `pathFilenameCitationSSOT`             | string           | same path as the repository-root `CITATION.cff` | Authoritative source citation file. Use this if your editable citation file lives somewhere like `citations/CITATION.cff`.                      |
| `addGitHubRelease`                     | boolean          | `true`                                          | Add GitHub release metadata when available.                                                                                                     |
| `addPyPIrelease`                       | boolean          | `true`                                          | Add a PyPI artifact URL when available. Set this to `false` for packages not published on PyPI.                                                 |
| `projectURLTargets`                    | array of strings | `["homepage", "license", "repository"]`         | Choose which keys from `[project.urls]` are copied into `CITATION.cff`. Supported values are `homepage`, `license`, and `repository`.           |
| `gitCommitMessage`                     | string           | `"Update citations [skip ci]"`                  | Commit message used when updateCitation commits from GitHub Actions.                                                                            |
| `gitUserName`                          | string           | `"updateCitation"`                              | Git username used for commits from GitHub Actions.                                                                                              |
| `gitUserEmail`                         | string           | empty string                                    | Git email used for commits. If omitted, updateCitation tries GitHub-derived noreply addresses first and then falls back to `action@github.com`. |
| `gitAmendFromGitHubAction`             | boolean          | `true`                                          | If `true`, updateCitation commits and pushes the updated citation file when running in GitHub Actions.                                          |
| `pathFilenameCitationDOTcffRepository` | string           | repository root `CITATION.cff` path             | Advanced full-path override for the repository-root citation file.                                                                              |
| `pathRepository`                       | string           | current working directory                       | Advanced override for the repository root. Usually you should run updateCitation from the repository root instead.                              |
| `filename_pyprojectDOTtoml`            | string           | `"pyproject.toml"`                              | Advanced override for the settings filename after settings are loaded.                                                                          |
| `pathReferences`                       | string           | `citations/` under the repository root          | Accepted by the settings object, but not currently used by the main workflow.                                                                   |
| `GITHUB_TOKEN`                         | string or `null` | `null`                                          | GitHub API token. Prefer the `GITHUB_TOKEN` environment variable instead of putting secrets in `pyproject.toml`.                                |

Do not set these internal fields in `[tool.updateCitation]`:

- `pathFilenamePackageSSOT`
- `tomlPackageData`

### Configuration Notes

- `addPyPIrelease = false` prevents updateCitation from generating a new `repository-artifact` URL, but it does not delete an existing `repository-artifact` already present in your source citation file.
- `projectURLTargets` only maps `homepage`, `license`, and `repository`.
- If you override a path-related setting such as `filenameCitationDOTcff` or `pathRepository`, also override any dependent full-path setting you rely on.

For example, a repository that keeps its editable citation file under `citations/` and is not published on PyPI can use:

```toml
[tool.updateCitation]
pathFilenameCitationSSOT = "citations/CITATION.cff"
addPyPIrelease = false
```

## Contributing

Contributions are welcome. Please feel free to submit pull requests.

## Design Goals

1. 100% Python.
2. Dynamic self-configuration whenever possible.
3. 100% of the `updateCitation` settings in `pyproject.toml`.
4. All settings for external services, such as GitHub and PyPI, use the configuration from those services instead of creating new configuration for `updateCitation`.
5. Highly extensible for current and future services.

## My Recovery

[![Static Badge](https://img.shields.io/badge/2011_August-Homeless_since-blue?style=flat)](https://HunterThinks.com/support)
[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC3Gx7kz61009NbhpRtPP7tw)](https://www.youtube.com/@HunterHogan)

[![CC-BY-NC-4.0](https://raw.githubusercontent.com/hunterhogan/updateCitation/refs/heads/main/.github/CC-BY-NC-4.0.png)](https://creativecommons.org/licenses/by-nc/4.0/)
