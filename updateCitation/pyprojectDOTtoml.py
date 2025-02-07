from updateCitation import CitationNexus
from typing import Any, Dict
import tomli

def get_pyprojectDOTtoml(pathRepoRoot):
    """Given the path to the root of the repository, return the contents of the pyproject.toml file.

        Parameters:
            pathRepoRoot (Path): Path to the root of the repository.

        Returns:
            Dict[str, Any]: Contents of the pyproject.toml file.
    """
    pathFilenamePackageSSOT = pathRepoRoot / 'pyproject.toml'
    tomlPackageData: Dict[str, Any] = tomli.loads(pathFilenamePackageSSOT.read_text())['project']
    return tomlPackageData

def add_pyprojectDOTtoml(nexusCitation: CitationNexus, packageData: Dict[str, Any]) -> CitationNexus:
    """Adds citation information from a pyproject.toml file to a CitationNexus object.
        Parameters:
            nexusCitation (CitationNexus): The CitationNexus object to update.
            packageData (Dict[str, Any]): A dictionary containing the package data from the pyproject.toml file.
        Returns:
            CitationNexus: The updated CitationNexus object.
        Raises:
            ValueError: If the 'authors' field is missing in the package data.
        Notes:
            - The function extracts author and maintainer information from the package data.
            - It assumes that author names are provided in the 'name' field and splits them into 'given-names' and 'family-names'.
            - It sets the 'title' field of the CitationNexus object to the package name.
            - It marks the CitationNexus object as having been updated from a 'pyprojectDOTtoml' file.
        """

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
