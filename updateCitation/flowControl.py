from typing import Any, Union
from updateCitation import (
    add_pyprojectDOTtoml,
    addCitation,
    addGitHubRelease,
    addPyPAMetadata,
    addPyPIrelease,
    CitationNexus,
    filename_pyprojectDOTtomlDEFAULT,
    getSettingsPackage,
    SettingsPackage,
    writeCitation,
)
import os
import pathlib

"""
How to automate citation updates:
- The `pyproject.toml` file is the source of truth for settings.
    - read from it
    - create a `SettingsPackage` object with the toml values or the default values
- Create an installable package for updateCitation.
- Create a GitHub Action that runs updateCitation.

Projected flow during a GitHub action to update a citation:
- Commit and push all to GitHub
- GitHub action:
    - pip install updateCitation # i need to make a PyPI package first, of course
    - import updateCitation
    - `updateCitation.here()`
    ? Can/should the following logic (or some parts of it) be a function in `updateCitation`?
    - updateCitation will compare the toml version to the github and the pypi versions
        - if the toml version is newer
            - if python tests pass,
                - updateCitation will update everything, including not yet existing versions on GitHub and/or PyPI
                - updateCitation will make a special git commit with the updated citation so that the updated versions are in the releases
                - after that special commit, the workflows for GitHub and PyPI are allowed to run
            - if python tests do NOT pass, updateCitation will update everything but NOT anticipate new versions numbers on GitHub and PyPI
        - I don't have logic for updating the `commit` field yet, but when I figure out how to implement the logic, I guess I will use the hash from the commit just before the special commit.
"""

def here(pathFilename_pyprojectDOTtoml: Union[str, os.PathLike[Any], None] = None) -> None:
    """Updates citation files based on package metadata and release information.

        This function orchestrates the update of citation files within a repository.
        It gathers metadata from the pyproject.toml file, adds information from
        GitHub and PyPI releases, and writes the updated citation data to both
        the single-source-of-truth (SSOT) citation file and the repository-level
        citation file.
        Parameters:
            pathRoot (Union[str, os.PathLike[Any]]): The root path of the repository.
        Raises:
            ValueError: If the package name cannot be found in the pyproject.toml file.
        """
    pathFilenameSettingsSSOT = pathlib.Path(pathFilename_pyprojectDOTtoml) if pathFilename_pyprojectDOTtoml else pathlib.Path.cwd() / filename_pyprojectDOTtomlDEFAULT
    truth: SettingsPackage = getSettingsPackage(pathFilenameSettingsSSOT)

    nexusCitation = CitationNexus()

    nexusCitation, truth = add_pyprojectDOTtoml(nexusCitation, truth)

    if not nexusCitation.title:
        # TODO learn how to change the field from `str | None` to `str` after the field is populated
        # especially for a required field
        raise ValueError("Package name is required.")

    # pathCitations = truth.pathRepository / "citations"
    pathCitations = truth.pathRepository / nexusCitation.title / "citations"
    pathFilenameCitationSSOT = pathCitations / truth.filenameCitationDOTcff
    pathFilenameCitationDOTcffRepository = truth.pathRepository / truth.filenameCitationDOTcff

    nexusCitation = addCitation(nexusCitation, pathFilenameCitationSSOT)
    nexusCitation = addPyPAMetadata(nexusCitation, truth.tomlPackageData)
    nexusCitation = addGitHubRelease(nexusCitation)
    nexusCitation = addPyPIrelease(nexusCitation)

    writeCitation(nexusCitation, pathFilenameCitationSSOT, pathFilenameCitationDOTcffRepository)
