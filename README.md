# updateCitation

Automatically update `CITATION.cff` from your Python project's `pyproject.toml`, GitHub release data when enabled, and PyPI release data when enabled.

This README gives `updateCitation` specific commands and settings. For the surrounding tools, follow the tool maintainers' documentation: GitHub explains how [`CITATION.cff` files appear on GitHub](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files), Git explains [Git hooks](https://git-scm.com/docs/githooks), uv explains [`uv tool`](https://docs.astral.sh/uv/guides/tools/), `pre-commit` explains [`pre-commit`](https://pre-commit.com/), and PyPA explains [`pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).

## Quick Start

Choose one of these:

| Goal                                                                  | Good fit          | File you create                        |
| --------------------------------------------------------------------- | ----------------- | -------------------------------------- |
| GitHub updates `CITATION.cff` after pushes to a GitHub repository.    | GitHub Action     | `.github/workflows/updateCitation.yml` |
| One computer updates `CITATION.cff` before local commits, using uv.   | `Git` hook        | `.git/hooks/pre-commit`                |
| A shared local hook is configured in the repository for contributors. | `pre-commit` hook | `.pre-commit-config.yaml`              |

## Option: GitHub Action

This is usually the most portable option for a GitHub-hosted repository. The workflow file is committed to the repository, so the update runs on GitHub after pushes and collaborators do not need `updateCitation` installed on their computers. GitHub's [Actions quickstart](https://docs.github.com/en/actions/get-started/quickstart) explains GitHub Actions; the workflow below is the `updateCitation`-specific part.

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

1. Commit the file and push it to GitHub.

If the default settings work for your project, you are done. You do not need a `[tool.updateCitation]` section in `pyproject.toml`.

## Option: Run Locally Before Pushing

Running locally means `updateCitation` runs on your computer before changes are sent to GitHub, GitLab, Codeberg, or another Git host. You can do this with a plain `Git` hook or with `pre-commit`.

A plain `Git` hook is local to one clone on one computer. The hook file lives inside `.git`, so it is not committed or shared with collaborators. The plain hook below uses [`uv tool`](https://docs.astral.sh/uv/guides/tools/), so you need [uv](https://docs.astral.sh/uv/) installed before using it. uv's own docs cover [uv installation](https://docs.astral.sh/uv/getting-started/installation/) and the details of managing tools with `uv tool`.

For a shared local setup, `pre-commit` is often the practical option. The `.pre-commit-config.yaml` file is committed to the repository, and each collaborator runs `pre-commit install` once after cloning. That makes `pre-commit` the local-hook option in this README that can be shared across users and across Git hosting services.

### Are you using `pre-commit`?

Look in the top directory of your repository.

- If there is a file named `.pre-commit-config.yaml`, your project is using `pre-commit`.
- If there is no `.pre-commit-config.yaml`, your project is probably not using `pre-commit` yet.
- You can also run `pre-commit --version` in a terminal. If it prints a version number, the `pre-commit` program is installed on your computer.

If your project already has `.pre-commit-config.yaml`, use the `pre-commit` instructions below. If not, the plain `Git` hook may be enough for one user on one machine.

### `Git` Hook

A `Git` hook runs when you commit. This file is local to your computer and is not uploaded to GitHub or another Git host.

1. Install `updateCitation` as a uv-managed tool:

```bash
uv tool install updateCitation
```

This installs `updateCitation` outside your project virtual environment. You do not need to add `updateCitation` to the repository's own dependencies for this plain Git hook.

1. In the top directory of your repository, find or create the hidden `.git/hooks` folder, and find or create a file named `pre-commit`.
2. Paste this into `.git/hooks/pre-commit`:

```bash
#!/usr/bin/env bash
set -euo pipefail

updateCitation
```

1. On macOS or Linux, make the file executable:

```bash
chmod +x .git/hooks/pre-commit
```

Now each `git commit` runs `updateCitation`. If `updateCitation` changes `CITATION.cff`, review the change, add the changed citation file or files with `git add`, and commit again.

### `pre-commit` Hook

Use this if your project already uses `pre-commit` or if you want a shared local hook that collaborators can install. The `pre-commit` documentation explains [repository-local hooks](https://pre-commit.com/#repository-local-hooks) and [`pre-commit install`](https://pre-commit.com/#pre-commit-install); the configuration below is the `updateCitation`-specific part.

1. In the top directory of your repository, create a file named `.pre-commit-config.yaml`.
2. Paste this into `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: updatecitation
        name: updateCitation
        entry: updateCitation
        language: python
        additional_dependencies:
          - updateCitation
        files: ^$
        pass_filenames: false
        always_run: true
```

This lets `pre-commit` install `updateCitation` in its own hook environment. It does not require `updateCitation` to be installed in the project's virtual environment.

1. Install the hook:

```bash
pre-commit install
```

Now each commit runs `updateCitation` through `pre-commit` before finalizing the commit.

### Non-GitHub Repositories

The local options are not tied to GitHub. For GitLab, Codeberg, or another Git host, disable GitHub release metadata so `updateCitation` does not try to read GitHub releases:

```toml
[tool.updateCitation]
addGitHubRelease = false
```

If the package is not published on PyPI, also set:

```toml
[tool.updateCitation]
addPyPIrelease = false
```

With those settings, `updateCitation` can still use `[project]` metadata from `pyproject.toml` and the existing citation file.

## Manually running `updateCitation`

### Install `updateCitation` as a uv-managed tool

```bash
uv tool install updateCitation
```

### Install `updateCitation` with `pip`

From your project's virtual environment:

```bash
pip install updateCitation
```

### Install `updateCitation` with `uv`

Only for people who develop your project:

```bash
uv add --dev updateCitation
```

### When `updateCitation` is installed in your current Python environment

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

`updateCitation` reads standard project metadata from `[project]` in `pyproject.toml`. PyPA's guide explains [writing `pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/), and the PyPA specification explains why tool-specific settings belong under [the `[tool]` table](https://packaging.python.org/en/latest/specifications/pyproject-toml/#arbitrary-tool-configuration-the-tool-table). The most important `[project]` fields for `updateCitation` are:

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

| Setting                                | Type             | Default                                         | Purpose                                                                                                                                           |
| -------------------------------------- | ---------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `filenameCitationDOTcff`               | string           | `"CITATION.cff"`                                | Filename for the repository-root citation file.                                                                                                   |
| `pathFilenameCitationSSOT`             | string           | same path as the repository-root `CITATION.cff` | Authoritative source citation file. Use this if your editable citation file lives somewhere like `citations/CITATION.cff`.                        |
| `addGitHubRelease`                     | boolean          | `true`                                          | Add GitHub release metadata when available.                                                                                                       |
| `addPyPIrelease`                       | boolean          | `true`                                          | Add a PyPI artifact URL when available. Set this to `false` for packages not published on PyPI.                                                   |
| `projectURLTargets`                    | array of strings | `["homepage", "license", "repository"]`         | Choose which keys from `[project.urls]` are copied into `CITATION.cff`. Supported values are `homepage`, `license`, and `repository`.             |
| `gitCommitMessage`                     | string           | `"Update citations [skip ci]"`                  | Commit message used when `updateCitation` commits from GitHub Actions.                                                                            |
| `gitUserName`                          | string           | `"updateCitation"`                              | Git username used for commits from GitHub Actions.                                                                                                |
| `gitUserEmail`                         | string           | empty string                                    | Git email used for commits. If omitted, `updateCitation` tries GitHub-derived noreply addresses first and then falls back to `action@github.com`. |
| `gitAmendFromGitHubAction`             | boolean          | `true`                                          | If `true`, `updateCitation` commits and pushes the updated citation file when running in GitHub Actions.                                          |
| `pathFilenameCitationDOTcffRepository` | string           | repository root `CITATION.cff` path             | Advanced full-path override for the repository-root citation file.                                                                                |
| `pathRepository`                       | string           | current working directory                       | Advanced override for the repository root. Usually you should run `updateCitation` from the repository root instead.                              |
| `filename_pyprojectDOTtoml`            | string           | `"pyproject.toml"`                              | Advanced override for the settings filename after settings are loaded.                                                                            |
| `pathReferences`                       | string           | `citations/` under the repository root          | Accepted by the settings object, but not currently used by the main workflow.                                                                     |
| `GITHUB_TOKEN`                         | string or `null` | `null`                                          | GitHub API token. Prefer the `GITHUB_TOKEN` environment variable instead of putting secrets in `pyproject.toml`.                                  |

Do not set these internal fields in `[tool.updateCitation]`:

- `pathFilenamePackageSSOT`
- `tomlPackageData`

### Configuration Notes

- `addPyPIrelease = false` prevents `updateCitation` from generating a new `repository-artifact` URL, but it does not delete an existing `repository-artifact` already present in your source citation file.
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
