from cffconvert.cli.create_citation import create_citation
from typing import Any, Union
from updateCitation import add_pyprojectDOTtoml
from updateCitation import addCitation
from updateCitation import addGitHubRelease
from updateCitation import addPyPAMetadata
from updateCitation import addPyPIrelease
from updateCitation import CitationNexus
from updateCitation import filenameCitationDOTcffDEFAULT
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

def updateHere(pathRoot: Union[str, os.PathLike[Any], None] = None) -> None:
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

    """
    Idea that just popped into my head:
    I tend to separate getData and addData into different functions.
    I don't have a consistent mechanism for "enforceRequiredData", however.
    I could create an abstract function that enforces all required data.
    Parameters include:
        the identifier/path of the required data field
        the current data state
        perhaps: the SSOT for that data
    The function would enforce the data requirement.
    The flow of this package consistently returns to a central function (this one).
    So, if the SSOT of packageName is tomlPackageData, immediately after tomlPackageData
    is populated, I call `enforceRequiredData` and it will fail or not.
    If I change the SSOT for packageName, then I would call `enforceRequiredData` at a different time.
    Ok, I see a potential problem: I must move the call to `enforceRequiredData` depending on the SSOT,
    but if i want the SSOT to be a user-configurable option, I can't redesign the flow. I might, however,
    call `enforceRequiredData` after each step that loads data. `enforceRequiredData` would have access to
    the table that specifies the SSOT for each data field. It would know which step just completed and it would
    enforce the appropriate requirements.
    That might work but it requires a bunch of infrastructure that I don't have.

    Deepseek: essentially suggested modifying my "addData" step to a "schema-driven validation" paradigm.
    Don't just add the data to a data structure, but add it to a schema. The schema includes required fields
    and schema-driven seems to mean that enforcement is baked into the process. `Pydantic` specifically mentioned
    and I've been running across that package a lot lately.

    I think `attrs`, which I am using for the first time, and Pydantic are similar tools. I think `attrs` has
    mechanisms for implementing this scheme-driven idea.

    I could add a `enforceRequiredData` method to the class. Actually, the currently unsuccessful `setInStone`
    method has half of the information necessary for the `enforceRequiredData` method: it lists the SSOT for each
    field. If I added information about which fields are required, then my idea for `enforceRequiredData` would be
    realized. I added the `setInStone` call to the end of each "addData" step.

    AH! and because `get_pyprojectDOTtoml` and `add_pyprojectDOTtoml` are currently separated, that is why
    I am testing packageName here instead of in `add_pyprojectDOTtoml`.

    I segregated the two steps during creation because I wasn't sure what information I would get from `addPyPAMetadata`,
    so I waited to design/run `add_pyprojectDOTtoml`, but now that I know, I can change the flow so get and add are the same
    step.

    Ok, this idea might not be the best idea, but it fits with my current style and it fits very well with my current code,
    so it is easy to implement. I will try it and see how it goes.
    """
    nexusCitation = CitationNexus()

    nexusCitation, tomlPackageData = add_pyprojectDOTtoml(nexusCitation, pathRepoRoot)

    if not nexusCitation.title:
        # TODO learn how to change the field from `str | None` to `str` after the field is populated
        # especially for a required field
        raise ValueError("Package name is required.")
    pathCitations = pathRepoRoot / nexusCitation.title / 'citations'
    pathFilenameCitationSSOT = pathCitations / filenameCitationDOTcffDEFAULT
    pathFilenameCitationDOTcffRepo = pathRepoRoot / filenameCitationDOTcffDEFAULT

    nexusCitation = addCitation(nexusCitation, pathFilenameCitationSSOT)
    nexusCitation = addPyPAMetadata(nexusCitation, tomlPackageData)
    nexusCitation = addGitHubRelease(nexusCitation)
    nexusCitation = addPyPIrelease(nexusCitation)

    writeCitation(nexusCitation, pathFilenameCitationSSOT, pathFilenameCitationDOTcffRepo)
