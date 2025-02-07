from cffconvert.cli.create_citation import create_citation
from updateCitation import CitationNexus
from updateCitation import filenameCitationDOTcff
from updateCitation import addGitHubRelease
from updateCitation import addPyPIrelease
from updateCitation import addPyPAMetadata
from updateCitation import getNexusCitation
from updateCitation import get_pyprojectDOTtoml, add_pyprojectDOTtoml
from typing import Any, Union
import attrs
import cffconvert
import os
import pathlib
import ruamel.yaml

"""
How to automate citation updates:
- The `pyproject.toml` file is the source of truth for the package metadata, so configuration information for updateCitation will be in there.
- Create an installable package for updateCitation.
- Create a GitHub Action that runs updateCitation.

How to update a citation:
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

def writeCitation(nexusCitation: CitationNexus, pathFilenameCitationSSOT: pathlib.Path, pathFilenameCitationDOTcffRepo: pathlib.Path):
    """Writes citation information to YAML files.
        This function takes a CitationNexus object and writes its data to two YAML files:
        one for single source of truth (SSOT) and another for a repository's .cff file.
        It performs data conversion, validation, and file writing using the ruamel.yaml library.
        Parameters:
            nexusCitation (CitationNexus): An object containing citation metadata.
            pathFilenameCitationSSOT (pathlib.Path): Path to the SSOT YAML file.
            pathFilenameCitationDOTcffRepo (pathlib.Path): Path to the .cff YAML file in the repository.
        Raises:
            ValidationError: If the generated citation object fails validation.
        Notes:
            - The function uses a temporary validation file.
            - It replaces "DASH" with "-" in dictionary keys.
            - It filters out empty lists from the citation data.
        """

    # NOTE embarrassingly hacky process to follow
    parameterIndent= 2
    parameterLineWidth = 60
    yamlWorkhorse = ruamel.yaml.YAML()

    def srsly(Z0Z_filed, Z0Z_value):
        if Z0Z_value: # empty lists
            return True
        else:
            return False

    dictionaryCitation = attrs.asdict(nexusCitation, filter=srsly)
    for keyName in list(dictionaryCitation.keys()):
        dictionaryCitation[keyName.replace("DASH", "-")] = dictionaryCitation.pop(keyName)

    pathFilenameForValidation = pathFilenameCitationSSOT.with_stem('validation')

    def writeStream(pathFilename):
        with open(pathFilename, 'w') as pathlibIsAStealthContextManagerThatRuamelCannotDetectAndRefusesToWorkWith:
            yamlWorkhorse.dump(dictionaryCitation, pathlibIsAStealthContextManagerThatRuamelCannotDetectAndRefusesToWorkWith)

    writeStream(pathFilenameForValidation)

    citationObject: cffconvert.Citation = create_citation(infile=pathFilenameForValidation, url=None)
    if citationObject.validate() is None:
        writeStream(pathFilenameCitationSSOT)
        writeStream(pathFilenameCitationDOTcffRepo)

    pathFilenameForValidation.unlink()

def updateHere(pathRoot: Union[str, os.PathLike[Any]]):
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
    pathRepoRoot = pathlib.Path(pathRoot)

    tomlPackageData = get_pyprojectDOTtoml(pathRepoRoot)

    packageName: str = tomlPackageData.get("name", None)
    if not packageName:
        raise ValueError("Package name is required.")

    pathCitations = pathRepoRoot / packageName / 'citations'
    pathFilenameCitationSSOT = pathCitations / filenameCitationDOTcff
    pathFilenameCitationDOTcffRepo = pathRepoRoot / filenameCitationDOTcff

    nexusCitation = getNexusCitation(pathFilenameCitationSSOT)
    nexusCitation = addPyPAMetadata(nexusCitation, tomlPackageData)
    nexusCitation = add_pyprojectDOTtoml(nexusCitation, tomlPackageData)
    nexusCitation = addGitHubRelease(nexusCitation)
    nexusCitation = addPyPIrelease(nexusCitation)

    writeCitation(nexusCitation, pathFilenameCitationSSOT, pathFilenameCitationDOTcffRepo)
