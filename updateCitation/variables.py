from typing import Set
import attrs

cffDASHversionDEFAULT = '1.2.0'

filenameCitationDOTcffDEFAULT = 'CITATION.cff'
filename_pyprojectDOTtomlDEFAULT = "pyproject.toml" # I can't decide if this is a HARDCODED value (which I want to avoid)
# or implementing the specification https://packaging.python.org/en/latest/specifications/pyproject-toml/
# If implementing, I might still provide a way to override the filename, but the approach is different than
# declaring HARDCODED! BAD! BOO! HISS!
subPathCitationsDEFAULT = "citations"
messageDEFAULT = "Cite this software with the metadata in this file."

projectURLTargets: Set[str] = {"homepage", "license", "repository"}

fieldsRequired = {"authors", "cffDASHversion", "message", "title"}
"""
`fieldsRequired` could be dynamically loaded through the following:
from cffconvert.citation import Citation
# from cffconvert.lib.citation import Citation # upcoming version 3.0.0
cffstr = "cff-version: 1.2.0"
citationObject = Citation(cffstr)
schemaDOTjson = citationObject._get_schema()
    "required": [
        "authors",
        "cff-version",
        "message",
        "title"
    ],
# Convert '-' to 'DASH'
"""

@attrs.define
class CitationNexus:
    """
    - one-to-one correlation with `cffconvert.lib.cff_1_2_x.citation` class Citation_1_2_x.cffobj
    """
    abstract: str | None = None
    authors: list[dict[str,str]] = attrs.field(factory=list)
    cffDASHversion: str = cffDASHversionDEFAULT
    commit: str | None = None # GitHub TODO
    contact: list[dict[str,str]] = attrs.field(factory=list)
    dateDASHreleased: str | None = None
    doi: str | None = None
    identifiers: list[str] = attrs.field(factory=list)
    keywords: list[str] = attrs.field(factory=list)
    license: str | None = None
    licenseDASHurl: str | None = None
    message: str = messageDEFAULT
    preferredDASHcitation: str | None = None
    references: list[str] = attrs.field(factory=list) # TODO bibtex files in pathCitationSSOT. Conversion method and timing TBD.
    repository: str | None = None
    repositoryDASHartifact: str | None = None
    repositoryDASHcode: str | None = None
    title: str | None = None
    type: str | None = None
    url: str | None = None
    version: str | None = None

    def setInStone(self, prophet: str) -> "CitationNexus":
        """I would like this method to accomplish the following:
        - if a field in the case is in `fieldsRequired`, confirm the field is not None
        - for each field listed in the case, protect the field from being changed

        Validation of the `CitationNexus` object will be done in the `writeCitation` function
        by the appropriate package and function."""
        match prophet:
            case "Citation":
                pass
                # "freeze" these items
                # setattr(self.cffDASHversion, 'type', Final[str])
                # setattr(self.doi, 'type', Final[str])
                # cffDASHversion: str
                # message: str
                # abstract: str | None = None
                # doi: str | None = None
                # preferredDASHcitation: str | None = None
                # type: str | None = None
            case "GitHub":
                pass
                # "freeze" these items
                # setattr(self.commit, 'type', Final[str])
                # setattr(self.dateDASHreleased, 'type', Final[str])
                # setattr(self.identifiers, 'type', Final[list[str]])
                # setattr(self.repositoryDASHcode, 'type', Final[str])
            case "PyPA":
                pass
                # "freeze" these items
                # setattr(self.keywords, 'type', Final[list[str]])
                # setattr(self.license, 'type', Final[str])
                # setattr(self.licenseDASHurl, 'type', Final[str])
                # setattr(self.repository, 'type', Final[str])
                # setattr(self.url, 'type', Final[str])
                # setattr(self.version, 'type', Final[str])
            case "PyPI":
                pass
                # "freeze" these items
                # setattr(self.repositoryDASHartifact, 'type', Final[str])
            case "pyprojectDOTtoml":
                pass
                # "freeze" these items
                # setattr(self.authors, 'type', Final[list[dict[str,str]]])
                # setattr(self.contact, 'type', Final[list[dict[str,str]]])
                # setattr(self.title, 'type', Final[str])
        return self
