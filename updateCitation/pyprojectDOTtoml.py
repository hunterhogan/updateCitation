from typing import Any, Dict, Tuple
from updateCitation import (
	CitationNexus,
	mapNexusCitation2pyprojectDOTtoml,
	SettingsPackage,
	)
import pathlib
import tomli

def getSettingsPackage(pathFilename: pathlib.Path) -> SettingsPackage:
	Z0Z_tomlSherpa = tomli.loads(pathFilename.read_text())
	Z0Z_SettingsPackage: Dict[str, Any] = {}
	if Z0Z_tomlSherpa.get("tool", None):
		Z0Z_SettingsPackage = Z0Z_tomlSherpa["tool"].get("updateCitation", {})
	truth = SettingsPackage(**Z0Z_SettingsPackage, pathFilenamePackageSSOT=pathFilename)
	return truth

def get_pyprojectDOTtoml(truth: SettingsPackage) -> SettingsPackage:
	truth.tomlPackageData = tomli.loads(truth.pathFilenamePackageSSOT.read_text())['project']
	return truth

def add_pyprojectDOTtoml(nexusCitation: CitationNexus, truth: SettingsPackage) -> Tuple[CitationNexus, SettingsPackage]:
	def Z0Z_ImaNotValidatingNoNames(person: Dict[str, str]) -> Dict[str, str]:
		cffPerson: Dict[str, str] = {}
		if person.get('name', None):
			cffPerson['given-names'], cffPerson['family-names'] = person['name'].split(' ', 1)
		if person.get('email', None):
			cffPerson['email'] = person['email']
		return cffPerson

	truth = get_pyprojectDOTtoml(truth)

	packageName: str = truth.tomlPackageData.get("name", None)
	nexusCitation.title = packageName

	for keyNexusCitation, key_pyprojectDOTtoml in mapNexusCitation2pyprojectDOTtoml:
		listPersonsTOML = truth.tomlPackageData.get(key_pyprojectDOTtoml, None)
		if listPersonsTOML:
			listPersonsCFF = []
			for person in listPersonsTOML:
				listPersonsCFF.append(Z0Z_ImaNotValidatingNoNames(person))
			setattr(nexusCitation, keyNexusCitation, listPersonsCFF)

	# nexusCitation.setInStone("pyprojectDOTtoml")
	return nexusCitation, truth
