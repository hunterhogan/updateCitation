from typing import Set
import attrs

filenameCitationDOTcff = 'CITATION.cff'

projectURLTargets: Set[str] = {"homepage", "license", "repository"}

@attrs.define
class CitationNexus:
    """
    - one-to-one correlation with `cffconvert.lib.cff_1_2_x.citation` class Citation_1_2_x.cffobj
    """
    cffDASHversion: str
    message: str

    abstract: str | None = None
    authors: list[dict[str,str]] = attrs.field(factory=list)
    # GitHub TODO
    commit: str | None = None
    contact: list[dict[str,str]] = attrs.field(factory=list)
    dateDASHreleased: str | None = None
    doi: str | None = None
    identifiers: list[str] = attrs.field(factory=list)
    keywords: list[str] = attrs.field(factory=list)
    license: str | None = None
    licenseDASHurl: str | None = None
    preferredDASHcitation: str | None = None
    # TODO bibtex files in pathCitationSSOT. Conversion method and timing TBD.
    references: list[str] = attrs.field(factory=list)
    repository: str | None = None
    repositoryDASHartifact: str | None = None
    repositoryDASHcode: str | None = None
    title: str | None = None
    type: str | None = None
    url: str | None = None
    version: str | None = None

    def setInStone(self, prophet: str) -> "CitationNexus":
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
