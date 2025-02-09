from typing import Any, Dict, List, Set
import attrs
import inspect
import warnings

cffDASHversionDEFAULT = '1.2.0'
filename_pyprojectDOTtomlDEFAULT = "pyproject.toml"
filenameCitationDOTcffDEFAULT = 'CITATION.cff'
messageDEFAULT = "Cite this software with the metadata in this file."
subPathCitationsDEFAULT = "citations"

projectURLTargets: Set[str] = {"homepage", "license", "repository"}

CitationNexusFieldsRequired: Set[str] = {"authors", "cffDASHversion", "message", "title"}
""" `fieldsRequired` could be dynamically loaded through the following:
from cffconvert.citation import Citation # from cffconvert.lib.citation import Citation # upcoming version 3.0.0
cffstr = "cff-version: 1.2.0"; citationObject = Citation(cffstr); schemaDOTjson = citationObject._get_schema()
# get "required": list of fields; # Convert '-' to 'DASH' in field names """

CitationNexusFieldsFrozen: Set[str] = set()
@attrs.define()
class CitationNexus:
    """
    - one-to-one correlation with `cffconvert.lib.cff_1_2_x.citation` class Citation_1_2_x.cffobj
    """

    abstract: str | None = None
    authors: List[Dict[str, str]] = attrs.field(factory=list)
    cffDASHversion: str = cffDASHversionDEFAULT
    commit: str | None = None
    contact: List[Dict[str, str]] = attrs.field(factory=list)
    dateDASHreleased: str | None = None
    doi: str | None = None
    identifiers: List[str] = attrs.field(factory=list)
    keywords: List[str] = attrs.field(factory=list)
    license: str | None = None
    licenseDASHurl: str | None = None
    message: str = messageDEFAULT
    preferredDASHcitation: str | None = None
    references: List[str] = attrs.field(factory=list)
    repository: str | None = None
    repositoryDASHartifact: str | None = None
    repositoryDASHcode: str | None = None
    title: str | None = None
    type: str | None = None
    url: str | None = None
    version: str | None = None

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent modification of frozen fields."""
        if name in CitationNexusFieldsFrozen:
            context = inspect.stack()[1].code_context[0].strip() # type: ignore
            warnings.warn(f"Field {name} is frozen and cannot be changed.\n{context}", UserWarning)
            return
        super().__setattr__(name, value)

    def setInStone(self, prophet: str) -> "CitationNexus":
        """
        Confirm that required fields are not None and freeze fields specified by the context.
        Parameters:
            prophet (str): The context for freezing fields.
        Returns:
            CitationNexus: The same object with specified fields frozen.
        Raises:
            ValueError: If any required field is None.
        """
        match prophet:
            case "Citation":
                fieldsSSOT = {"abstract", "cffDASHversion", "doi", "message", "preferredDASHcitation", "type"}
            case "GitHub":
                fieldsSSOT = {"commit", "dateDASHreleased", "identifiers", "repositoryDASHcode"}
            case "PyPA":
                fieldsSSOT = {"keywords", "license", "licenseDASHurl", "repository", "url", "version"}
            case "PyPI":
                fieldsSSOT = {"repositoryDASHartifact"}
            case "pyprojectDOTtoml":
                fieldsSSOT = {"authors", "contact", "title"}
            case _:
                fieldsSSOT = set()

        for fieldName in fieldsSSOT:
            if fieldName in CitationNexusFieldsRequired and getattr(self, fieldName) is None:
                raise ValueError(f"Field {fieldName} is required but not provided.")

        CitationNexusFieldsFrozen.update(fieldsSSOT)
        return self
