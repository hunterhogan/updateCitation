from updateCitation import CitationNexus
from typing import Any, Dict
import tomli

def get_pyprojectDOTtoml(pathRepoRoot):
    pathFilenamePackageSSOT = pathRepoRoot / 'pyproject.toml'
    # https://packaging.python.org/en/latest/specifications/pyproject-toml/
    tomlPackageData: Dict[str, Any] = tomli.loads(pathFilenamePackageSSOT.read_text())['project']
    return tomlPackageData

def add_pyprojectDOTtoml(nexusCitation: CitationNexus, packageData: Dict[str, Any]) -> CitationNexus:

    def Z0Z_ImaNotValidatingNoNames(person: Dict[str, str]) -> Dict[str, str]:
        cffPerson: Dict[str, str] = {}
        if person.get('name', None):
            cffPerson['given-names'], cffPerson['family-names'] = person['name'].split(' ', 1)
        if person.get('email', None):
            cffPerson['email'] = person['email']
        return cffPerson
    listAuthors = packageData.get("authors", None)
    if not listAuthors:
        raise ValueError("Authors are required.")
    else:
        listPersons = []
        for person in listAuthors:
            listPersons.append(Z0Z_ImaNotValidatingNoNames(person))
            nexusCitation.authors = listPersons
    if packageData.get("maintainers", None):
        listPersons = []
        for person in packageData["maintainers"]:
            listPersons.append(Z0Z_ImaNotValidatingNoNames(person))
            nexusCitation.contact = listPersons
    nexusCitation.title = packageData["name"]
    nexusCitation = nexusCitation.setInStone("pyprojectDOTtoml")
    return nexusCitation
