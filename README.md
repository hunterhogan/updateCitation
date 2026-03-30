# updateCitation

updateCitation is a Python tool that automates the maintenance of citation metadata in software projects. It helps researchers and developers ensure their work is properly citeable while maintaining consistent metadata across different platforms.

## Key Features

- Automatic generation and updates of CITATION.cff files
- Seamless integration with Python package metadata from pyproject.toml
- Synchronization with GitHub release information
- Integration with PyPI package metadata
- Validation of citation metadata format
- GitHub Actions support for automated updates

## Installation

```bash
pip install updateCitation
```

## Usage

The simplest way to use updateCitation is to run it from your repository root:

```python
import updateCitation
updateCitation.here()
```

For custom pyproject.toml locations:

```python
updateCitation.here("path/to/pyproject.toml")
```

## GitHub Actions Integration

updateCitation provides a GitHub Action that automatically updates your citation metadata on each push. To enable this:

1. Create `.github/workflows/updateCitation.yml` in your repository
2. Copy the provided workflow configuration
3. Commit and push to activate automated citation updates

## Configuration

updateCitation primarily uses your project's `pyproject.toml` file for configuration. Essential fields include:

### Required Fields

- `name`: Package name
- `version`: Current version
- `authors`: List of authors with names and emails

### Recommended Fields

- `description`: Project description
- `keywords`: Search keywords
- `license`: License information
- `urls`: Project URLs (homepage, repository, etc.)

### Optional Tool Settings

You can customize updateCitation's behavior in the `[tool.updateCitation]` section of `pyproject.toml`.

The most common configuration looks like this:

```toml
[tool.updateCitation]
filenameCitationDOTcff = "CITATION.cff"
pathFilenameCitationSSOT = "citations/CITATION.cff"
Z0Z_addGitHubRelease = true
Z0Z_addPyPIrelease = true
projectURLTargets = ["homepage", "license", "repository"]
gitCommitMessage = "Update citations [skip ci]"
gitUserName = "updateCitation"
# gitUserEmail = "123456+your-user@users.noreply.github.com"
# gitAmendFromGitHubAction = true
```

These are the current user-facing settings:

| Setting | Type | Default | Purpose |
| --- | --- | --- | --- |
| `filenameCitationDOTcff` | string | `"CITATION.cff"` | Filename for the repository-root copy of the citation file. |
| `pathFilenameCitationSSOT` | string | same path as the repository-root CFF | Authoritative source-of-truth CFF file to read from and write to. Use this when your real source file lives somewhere like `citations/CITATION.cff`. |
| `Z0Z_addGitHubRelease` | boolean | `true` | Enable GitHub release lookup for `commit`, `date-released`, `identifiers`, and `repository-code`. |
| `Z0Z_addPyPIrelease` | boolean | `true` | Enable PyPI URL generation for `repository-artifact`. Set this to `false` for packages that are not published on PyPI. |
| `projectURLTargets` | array of strings | `["homepage", "license", "repository"]` | Choose which keys from `[project.urls]` should be copied into the CFF. The currently supported values are `homepage`, `license`, and `repository`. |
| `gitCommitMessage` | string | `"Update citations [skip ci]"` | Commit message used when updateCitation auto-commits from GitHub Actions. |
| `gitUserName` | string | `"updateCitation"` | Git username used for auto-commits from GitHub Actions. |
| `gitUserEmail` | string | empty string | Git email used for auto-commits. If omitted, updateCitation tries GitHub-derived noreply addresses first and then falls back to `action@github.com`. |
| `gitAmendFromGitHubAction` | boolean | `true` | If `true`, updateCitation will auto-commit and push the updated CFF after successful validation when running in GitHub Actions. |

Advanced settings are also accepted because `[tool.updateCitation]` is loaded directly into `SettingsPackage`:

| Setting | Type | Default | Notes |
| --- | --- | --- | --- |
| `pathFilenameCitationDOTcffRepository` | string | repository root `CITATION.cff` path | Full path for the repository-root copy of `CITATION.cff`. Usually you do not need this unless you want to override the full path explicitly. |
| `pathRepository` | string | current working directory | Advanced override for the repository root. In normal usage, `updateCitation.here()` already determines this from where you run it. |
| `filename_pyprojectDOTtoml` | string | `"pyproject.toml"` | Advanced override for the settings filename. This does not change how `updateCitation.here()` initially finds the file unless you pass a path directly to `updateCitation.here(...)`. |
| `pathReferences` | string | `citations/` under the repository root | Accepted by the settings object, but currently not used by the main workflow. |
| `GITHUB_TOKEN` | string or `null` | `null` | GitHub API token. If omitted, updateCitation falls back to the `GITHUB_TOKEN` or `GH_TOKEN` environment variables. Avoid committing secrets to `pyproject.toml`. |

There are also two internal `SettingsPackage` fields that are **not** meant to be set in `[tool.updateCitation]`:

- `pathFilenamePackageSSOT`
  - Set internally from the `pyproject.toml` file being read.
- `tomlPackageData`
  - Populated internally from the `[project]` table.

### Configuration notes and caveats

- `Z0Z_addPyPIrelease = false` prevents updateCitation from generating a new `repository-artifact` URL, but it does not automatically delete an existing `repository-artifact` already present in your source CFF.
- `projectURLTargets` only maps `homepage`, `license`, and `repository` today.
- Some path defaults are effectively precomputed. If you override an upstream path-related setting such as `filenameCitationDOTcff` or `pathRepository`, also override the dependent full path fields explicitly.
  - Example: if you change `filenameCitationDOTcff`, also set `pathFilenameCitationDOTcffRepository`.
  - Example: if you change `pathRepository`, also set any full path settings you rely on.

For example, a repository that keeps its authoritative CFF under `citations/` and does not publish releases on PyPI can use:

```toml
[tool.updateCitation]
filenameCitationDOTcff = "CITATION.cff"
pathFilenameCitationSSOT = "citations/CITATION.cff"
Z0Z_addPyPIrelease = false
```

## Documentation

For detailed documentation, examples, and best practices, visit our [GitHub repository](https://github.com/hunterhogan/updateCitation).

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## Design goals

1. 100% Python.
2. Dynamic self-configuration whenever possible.
3. 100% of the updateCitation settings in pyproject.toml.
   1. No command line arguments.
   2. No environment variables.
   3. No separate configuration files.
4. All settings for external services, such as GitHub and PyPI, use the configuration from those services instead of creating new configuration for updateCitation.
5. Highly extensible for current and future services.

## My recovery

[![Static Badge](https://img.shields.io/badge/2011_August-Homeless_since-blue?style=flat)](https://HunterThinks.com/support)
[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC3Gx7kz61009NbhpRtPP7tw)](https://www.youtube.com/@HunterHogan)

[![CC-BY-NC-4.0](https://raw.githubusercontent.com/hunterhogan/updateCitation/refs/heads/main/.github/CC-BY-NC-4.0.png)](https://creativecommons.org/licenses/by-nc/4.0/)
