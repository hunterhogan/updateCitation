"""Read `pyproject.toml` settings and extract author and contact data.

(AI generated docstring)

You can use this module to load `updateCitation` settings from the
`[tool.updateCitation]` table in `pyproject.toml` [1], read the `[project]`
table, and populate `CitationNexus` [2] `authors` and `contact` field from
the `authors` and `maintainers` key in `pyproject.toml`.

Contents
--------
Functions
	add_pyprojectDOTtoml
		Populate a `CitationNexus` with author and contact data from `pyproject.toml`.
	get_pyprojectDOTtoml
		Read the `[project]` table from `pyproject.toml` into `SettingsPackage`.
	getSettingsPackage
		Instantiate a `SettingsPackage` from a `pyproject.toml` file.

References
----------
[1] pyproject.toml specification - Python Packaging User Guide
	https://packaging.python.org/en/latest/specifications/pyproject-toml/
[2] updateCitation.variables.CitationNexus
	Internal package reference

"""
from pathlib import Path
from tomllib import loads as tomllib_loads
from typing import Any
from updateCitation import CitationNexus, mapNexusCitation2pyprojectDOTtoml, SettingsPackage

def getSettingsPackage(pathFilename: Path) -> SettingsPackage:
	"""Instantiate a `SettingsPackage` from a `pyproject.toml` file.

	(AI generated docstring)

	You can use `getSettingsPackage` to read a `pyproject.toml` [1] file,
	extract values from the `[tool.updateCitation]` table, construct a
	`SettingsPackage` [2] instance, and then call `get_pyprojectDOTtoml` [3]
	to populate `tomlPackageData`.

	Parameters
	----------
	pathFilename : Path
		The full path to the `pyproject.toml` file.

	Returns
	-------
	truth : SettingsPackage
		A configured `SettingsPackage` with `tomlPackageData` populated.

	Examples
	--------
	Real usage from updateCitation.flowControl module:

		truth: SettingsPackage = getSettingsPackage(pathFilenameSettingsSSOT)

	References
	----------
	[1] pyproject.toml specification - Python Packaging User Guide
		https://packaging.python.org/en/latest/specifications/pyproject-toml/
	[2] updateCitation.variables.SettingsPackage
		Internal package reference
	[3] updateCitation.pyprojectDOTtoml.get_pyprojectDOTtoml
		Internal package reference

	"""
	Z0Z_tomlSherpa: dict[str, Any] = tomllib_loads(pathFilename.read_text(encoding="utf-8"))
	Z0Z_SettingsPackage: dict[str, Any] = {}
	if Z0Z_tomlSherpa.get("tool"):
		Z0Z_SettingsPackage = Z0Z_tomlSherpa["tool"].get("updateCitation", {})
	truth = SettingsPackage(**Z0Z_SettingsPackage, pathFilenamePackageSSOT=pathFilename)
	return get_pyprojectDOTtoml(truth)

def get_pyprojectDOTtoml(truth: SettingsPackage) -> SettingsPackage:
	"""Read the `[project]` table from `pyproject.toml` into `SettingsPackage`.

	(AI generated docstring)

	You can use `get_pyprojectDOTtoml` to parse the `[project]` table from
	the `pyproject.toml` [1] file at `truth.pathFilenamePackageSSOT` and store
	the resulting dictionary in `truth.tomlPackageData`.

	Parameters
	----------
	truth : SettingsPackage
		The settings object with `pathFilenamePackageSSOT` set.

	Returns
	-------
	truthPopulated : SettingsPackage
		The `truth` object with `tomlPackageData` populated.

	References
	----------
	[1] pyproject.toml specification - Python Packaging User Guide
		https://packaging.python.org/en/latest/specifications/pyproject-toml/

	"""
	truth.tomlPackageData = tomllib_loads(truth.pathFilenamePackageSSOT.read_text(encoding="utf-8"))['project']
	return truth

def add_pyprojectDOTtoml(nexusCitation: CitationNexus, truth: SettingsPackage) -> CitationNexus:
	"""Populate a `CitationNexus` with author and contact data from `pyproject.toml`.

	(AI generated docstring)

	You can use `add_pyprojectDOTtoml` to set `nexusCitation.title` from the
	`name` key in `truth.tomlPackageData`, and to populate `nexusCitation.authors`
	and `nexusCitation.contact` from the `authors` and `maintainers` key
	according to `mapNexusCitation2pyprojectDOTtoml` [1]. The function splits
	each person `name` into `given-names` and `family-names` for CFF [2]
	compatibility. After populating, the function calls
	`nexusCitation.setInStone("pyprojectDOTtoml")` [3] to freeze the
	`pyproject.toml`-owned field.

	Parameters
	----------
	nexusCitation : CitationNexus
		The citation object to populate.
	truth : SettingsPackage
		The settings object containing `tomlPackageData`.

	Returns
	-------
	nexusCitationPopulated : CitationNexus
		The `nexusCitation` object with `title`, `authors`, and `contact`
		populated.

	Examples
	--------
	Real usage from updateCitation.flowControl module:

		nexusCitation = add_pyprojectDOTtoml(nexusCitation, truth)

	References
	----------
	[1] updateCitation.variables.mapNexusCitation2pyprojectDOTtoml
		Internal package reference
	[2] Citation File Format (CFF) specification
		https://citation-file-format.github.io/
	[3] updateCitation.variables.CitationNexus.setInStone
		Internal package reference

	"""
	def Z0Z_ImaNotValidatingNoNames(person: dict[str, str]) -> dict[str, str]:
		cffPerson: dict[str, str] = {}
		if person.get('name'):
			cffPerson['given-names'], cffPerson['family-names'] = person['name'].split(' ', 1)
		if person.get('email'):
			cffPerson['email'] = person['email']
		return cffPerson

	packageName: str | None = truth.tomlPackageData.get("name", None)
	nexusCitation.title = packageName

	for keyNexusCitation, key_pyprojectDOTtoml in mapNexusCitation2pyprojectDOTtoml:
		listPersonsTOML = truth.tomlPackageData.get(key_pyprojectDOTtoml, None)
		if listPersonsTOML:
			listPersonsCFF: list[dict[str, str]] = [
				Z0Z_ImaNotValidatingNoNames(person) for person in listPersonsTOML
			]
			setattr(nexusCitation, keyNexusCitation, listPersonsCFF)

	nexusCitation.setInStone("pyprojectDOTtoml")
	return nexusCitation
