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

You can customize updateCitation's behavior in the `[tool.updateCitation]` section of pyproject.toml.

## Documentation

For detailed documentation, examples, and best practices, visit our [GitHub repository](https://github.com/hunterhogan/updateCitation).

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under CC-BY-NC-4.0. See the LICENSE file for details.

[![CC-BY-NC-4.0](https://github.com/hunterhogan/updateCitation/blob/main/CC-BY-NC-4.0.png)](https://creativecommons.org/licenses/by-nc/4.0/)
