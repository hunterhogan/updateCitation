from typing import Any, Union
from updateCitation import (
    add_pyprojectDOTtoml,
    addCitation,
    addGitHubRelease,
    addPyPAMetadata,
    addPyPIrelease,
    CitationNexus,
    filenameCitationDOTcffDEFAULT,
    subPathCitationsDEFAULT,
    writeCitation,
)
import os
import pathlib

"""
How to automate citation updates:
- The `pyproject.toml` file is the source of truth for the package metadata, so configuration information for updateCitation will be in there.
    - At the moment, only `pathRoot` is configurable.
    - But, hypothetically, anything marked with "DEFAULT" could be easily changed to a configuration option.
    - Furthermore, the `CitationNexus` object could be modified so that the SSOT for each field is configurable.
- Create an installable package for updateCitation.
- Create a GitHub Action that runs updateCitation.

Projected flow during a GitHub action to update a citation:
- Commit and push all to GitHub
- updateCitation will compare the toml version to the github and the pypi versions
    - if the toml version is newer, updateCitation can anticipate the version numbers on GitHub and PyPI
    - if python tests do NOT pass, updateCitation will update everything but NOT anticipate new versions numbers on GitHub and PyPI
    - if python tests pass,
        - updateCitation will update everything, including not yet existing versions on GitHub and/or PyPI
        - updateCitation will make a special git commit with the updated citation so that the updated versions are in the releases
        - after that special commit, the workflows for GitHub and PyPI are allowed to run
    - I don't have logic for updating the `commit` field yet, but I guess I will use the hash from the commit just before the special commit.
"""

def here(pathRoot: Union[str, os.PathLike[Any], None] = None) -> None:
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
    pathRepoRoot = pathlib.Path(pathRoot) if pathRoot else pathlib.Path.cwd()

    nexusCitation = CitationNexus()

    nexusCitation, tomlPackageData = add_pyprojectDOTtoml(nexusCitation, pathRepoRoot)

    if not nexusCitation.title:
        # TODO learn how to change the field from `str | None` to `str` after the field is populated
        # especially for a required field
        raise ValueError("Package name is required.")

    pathCitations = pathRepoRoot / nexusCitation.title / subPathCitationsDEFAULT
    pathFilenameCitationSSOT = pathCitations / filenameCitationDOTcffDEFAULT
    pathFilenameCitationDOTcffRepo = pathRepoRoot / filenameCitationDOTcffDEFAULT

    nexusCitation = addCitation(nexusCitation, pathFilenameCitationSSOT)
    nexusCitation = addPyPAMetadata(nexusCitation, tomlPackageData)
    nexusCitation = addGitHubRelease(nexusCitation)
    nexusCitation = addPyPIrelease(nexusCitation)

    writeCitation(nexusCitation, pathFilenameCitationSSOT, pathFilenameCitationDOTcffRepo)
