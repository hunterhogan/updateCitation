from pathlib import Path
from tomli import loads as tomli_loads
from typing import Any
from updateCitation import CitationNexus, mapNexusCitation2pyprojectDOTtoml, SettingsPackage

def getSettingsPackage(pathFilename: Path) -> SettingsPackage:
	Z0Z_tomlSherpa = tomli_loads(pathFilename.read_text())
	Z0Z_SettingsPackage: dict[str, Any] = {}
	if Z0Z_tomlSherpa.get("tool", None):
		Z0Z_SettingsPackage = Z0Z_tomlSherpa["tool"].get("updateCitation", {})
	truth = SettingsPackage(**Z0Z_SettingsPackage, pathFilenamePackageSSOT=pathFilename)
	truth = get_pyprojectDOTtoml(truth)
	return truth

def get_pyprojectDOTtoml(truth: SettingsPackage) -> SettingsPackage:
	truth.tomlPackageData = tomli_loads(truth.pathFilenamePackageSSOT.read_text())['project']
	return truth

def add_pyprojectDOTtoml(nexusCitation: CitationNexus, truth: SettingsPackage) -> CitationNexus:
	def Z0Z_ImaNotValidatingNoNames(person: dict[str, str]) -> dict[str, str]:
		cffPerson: dict[str, str] = {}
		if person.get('name', None):
			cffPerson['given-names'], cffPerson['family-names'] = person['name'].split(' ', 1)
		if person.get('email', None):
			cffPerson['email'] = person['email']
		return cffPerson

	packageName: str = truth.tomlPackageData.get("name", None)
	nexusCitation.title = packageName

	for keyNexusCitation, key_pyprojectDOTtoml in mapNexusCitation2pyprojectDOTtoml:
		listPersonsTOML = truth.tomlPackageData.get(key_pyprojectDOTtoml, None)
		if listPersonsTOML:
			listPersonsCFF: list[dict[str, str]] = []
			for person in listPersonsTOML:
				listPersonsCFF.append(Z0Z_ImaNotValidatingNoNames(person))
			setattr(nexusCitation, keyNexusCitation, listPersonsCFF)

	nexusCitation.setInStone("pyprojectDOTtoml")
	return nexusCitation
