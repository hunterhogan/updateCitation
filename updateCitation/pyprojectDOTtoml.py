from typing import Any, Dict
from updateCitation import CitationNexus
import pathlib
import tomli

def get_pyprojectDOTtoml(pathRepoRoot: pathlib.Path) -> Dict[str, Any]:
    """Given the path to the root of the repository, return the contents of the pyproject.toml file.

        Parameters:
            pathRepoRoot (Path): Path to the root of the repository.

        Returns:
            Dict[str, Any]: Contents of the pyproject.toml file.
    """
    tomlHARDCODED = "pyproject.toml" # I can't decide if this is a HARDCODED value (which I want to avoid)
    # or implementing the specification https://packaging.python.org/en/latest/specifications/pyproject-toml/
    # If implementing, I might still provide a way to override the filename, but the approach is different than
    # declaring HARDCODED! BAD! BOO! HISS!
    pathFilenamePackageSSOT = pathRepoRoot / tomlHARDCODED
    tomlPackageData: Dict[str, Any] = tomli.loads(pathFilenamePackageSSOT.read_text())['project']
    return tomlPackageData

def add_pyprojectDOTtoml(nexusCitation: CitationNexus, pathRepoRoot: pathlib.Path) -> tuple[CitationNexus, Dict[str, Any]]:
    def Z0Z_ImaNotValidatingNoNames(person: Dict[str, str]) -> Dict[str, str]:
        cffPerson: Dict[str, str] = {}
        if person.get('name', None):
            cffPerson['given-names'], cffPerson['family-names'] = person['name'].split(' ', 1)
        if person.get('email', None):
            cffPerson['email'] = person['email']
        return cffPerson

    tomlPackageData = get_pyprojectDOTtoml(pathRepoRoot)

    packageName: str = tomlPackageData.get("name", None)
    if not packageName:
        raise ValueError("Package name is required.")
    nexusCitation.title = packageName

    listAuthors = tomlPackageData.get("authors", None)
    if not listAuthors:
        raise ValueError("Authors are required.")
    else:
        listPersons = []
        for person in listAuthors:
            listPersons.append(Z0Z_ImaNotValidatingNoNames(person))
            nexusCitation.authors = listPersons

    if tomlPackageData.get("maintainers", None):
        listPersons = []
        for person in tomlPackageData["maintainers"]:
            listPersons.append(Z0Z_ImaNotValidatingNoNames(person))
            nexusCitation.contact = listPersons

    nexusCitation = nexusCitation.setInStone("pyprojectDOTtoml")
    return nexusCitation, tomlPackageData
