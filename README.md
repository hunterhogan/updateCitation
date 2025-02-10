# updateCitation

A tool to automatically update citation files (CITATION.cff) in a repository based on metadata from `pyproject.toml`, GitHub releases, and PyPI releases.

## Features

- Automatically updates `CITATION.cff` files.
- Extracts metadata from `pyproject.toml`.
- Retrieves release information from GitHub.
- Fetches package information from PyPI.
- Ensures citation files are up-to-date with the latest project information.

## Installation

```bash
pip install updateCitation
```

## Usage

Run `updateCitation` from the root of your repository:

```python
from updateCitation import updateHere
updateHere(path/to/repo)
```

This will:

1. Read the `pyproject.toml` file for project metadata.
2. Fetch the latest release information from GitHub.
3. Retrieve package information from PyPI.
4. Update the `CITATION.cff` file in your repository.

## Configuration

Configuration is managed through the `pyproject.toml` file. Ensure that the `[project]` section contains accurate and up-to-date information about your project, including:

- `name`: The name of the package.
- `version`: The current version of the package.
- `authors`: A list of authors and their associated email addresses.
- `description`: A short description of the package.
- `keywords`: A list of keywords associated with the package.
- `license`: The license information for the package.
- `urls`: Links to the project homepage, repository, and other relevant URLs.

[![CC-BY-NC-4.0](https://github.com/hunterhogan/updateCitation/blob/main/CC-BY-NC-4.0.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
