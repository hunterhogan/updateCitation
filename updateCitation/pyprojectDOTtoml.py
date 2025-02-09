from typing import Any, Dict
from updateCitation import CitationNexus, filename_pyprojectDOTtomlDEFAULT
import pathlib
import tomli

def get_pyprojectDOTtoml(pathRepoRoot: pathlib.Path) -> Dict[str, Any]:
    """Given the path to the root of the repository, return the contents of the pyproject.toml file.

        Parameters:
            pathRepoRoot (Path): Path to the root of the repository.

        Returns:
            Dict[str, Any]: Contents of the pyproject.toml file.
    """
    pathFilenamePackageSSOT = pathRepoRoot / filename_pyprojectDOTtomlDEFAULT
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
    nexusCitation.title = packageName

    mapNexusCitation2pyprojectDOTtoml = [("authors", "authors"), ("contact", "maintainers")]
    for keyNexusCitation, key_pyprojectDOTtoml in mapNexusCitation2pyprojectDOTtoml:
        listPersonsTOML = tomlPackageData.get(key_pyprojectDOTtoml, None)
        if listPersonsTOML:
            listPersonsCFF = []
            for person in listPersonsTOML:
                listPersonsCFF.append(Z0Z_ImaNotValidatingNoNames(person))
            setattr(nexusCitation, keyNexusCitation, listPersonsCFF)

    nexusCitation = nexusCitation.setInStone("pyprojectDOTtoml")
    return nexusCitation, tomlPackageData
